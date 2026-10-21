#!/usr/bin/env python3
"""Owner-driven one-time Google Search Console OAuth enrollment (local Mac only).

Not a proxy, server-side Google web login, or credentials-forwarding service.
Upload the Google-issued Desktop OAuth client JSON from the SAME Mac browser.
No token or client secret is accepted in ChatGPT and nothing is published to GitHub.
"""
import argparse
import base64
from datetime import date, timedelta, datetime, timezone
from email import policy as mail_policy
from email.parser import BytesParser
import hashlib
from html import escape
from http.server import HTTPServer, BaseHTTPRequestHandler
import hmac
import json
import os
from pathlib import Path
import secrets
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, parse_qs, urlsplit, quote
from urllib.request import Request, urlopen

import gsc_metrics

HOST, PORT = "127.0.0.1", 18765
ROOT = Path(__file__).resolve().parent
SECRETS = ROOT / "secrets"
TOKEN_FILE = SECRETS / "gsc-onetime-enrollment.json"
TARGET_SITE = "https://mokshagoa.com/"
SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SITES_URL = "https://www.googleapis.com/webmasters/v3/sites"
CALLBACK = f"http://{HOST}:{PORT}/oauth2callback"
MAX_UPLOAD = 32768
ENROLL_MAX_SECONDS = 20 * 60


def private_write(path, obj):
    path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    path.parent.chmod(0o700)
    if path.exists() or path.is_symlink():
        raise RuntimeError("Existing OAuth enrollment or credential file; refusing to overwrite")
    payload = (json.dumps(obj, separators=(",", ":")) + "\n").encode()
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())


def issue():
    if gsc_metrics.SECRETS.exists():
        raise RuntimeError("Search Console already enrolled; read status before changing account")
    if TOKEN_FILE.exists():
        raise RuntimeError("Enrollment already issued. Check existing local enrollment service")
    token = secrets.token_urlsafe(28)
    private_write(TOKEN_FILE, {"key": token, "expires": int(time.time()) + ENROLL_MAX_SECONDS})
    # Temporary one-time local-only onboarding link. NOT a Google OAuth token.
    return f"http://{HOST}:{PORT}/setup/{token}"


def valid_client(raw):
    if len(raw) > MAX_UPLOAD:
        raise ValueError("OAuth JSON is oversized")
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, dict) or set(data) != {"installed"}:
        raise ValueError("Create an OAuth client with application type Desktop app")
    info = data["installed"]
    client_id = info.get("client_id")
    client_secret = info.get("client_secret")
    if not isinstance(client_id, str) or not client_id.endswith(".apps.googleusercontent.com"):
        raise ValueError("Invalid Google desktop client ID")
    if not isinstance(client_secret, str) or not 8 <= len(client_secret) <= 300:
        raise ValueError("Google desktop client secret missing")
    if info.get("auth_uri") not in (None, AUTH_URL, "https://accounts.google.com/o/oauth2/auth"):
        raise ValueError("Unexpected OAuth authorization endpoint")
    if info.get("token_uri") != TOKEN_URL:
        raise ValueError("Unexpected OAuth token endpoint")
    return {"client_id": client_id, "client_secret": client_secret}


def parse_form_upload(ctype, raw):
    if not ctype.startswith("multipart/form-data;") or len(raw) > MAX_UPLOAD:
        raise ValueError("Upload a small Google Desktop OAuth JSON client file")
    obj = BytesParser(policy=mail_policy.default).parsebytes(
        b"Content-Type: " + ctype.encode("ascii") +
        b"\r\nMIME-Version: 1.0\r\n\r\n" + raw)
    if not obj.is_multipart():
        raise ValueError("Expected multipart client upload")
    for part in obj.iter_parts():
        if part.get_param("name", header="content-disposition") == "oauth_client":
            content = part.get_payload(decode=True)
            if content is None:
                break
            return valid_client(content)
    raise ValueError("Google Desktop OAuth JSON client file not found")


def http_json(url, *, body=None, token=None):
    headers = {"Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    if body is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded" if isinstance(body, bytes) else "application/json"
    data = body if isinstance(body, bytes) else (json.dumps(body).encode() if body is not None else None)
    req = Request(url, data=data, headers=headers, method="POST" if data is not None else "GET")
    with urlopen(req, timeout=20) as r:
        blob = r.read(1024*1024 + 1)
    if len(blob) > 1024*1024:
        raise RuntimeError("Oversized Google API response")
    return json.loads(blob)


def complete(client, code, verifier):
    exchange = urlencode({
        "code": code, "client_id": client["client_id"], "client_secret": client["client_secret"],
        "redirect_uri": CALLBACK, "grant_type": "authorization_code",
        "code_verifier": verifier
    }).encode()
    tokens = http_json(TOKEN_URL, body=exchange)
    if SCOPE not in str(tokens.get("scope", "")).split():
        raise RuntimeError("Google did not grant the requested read-only Search Console scope")
    if "https://www.googleapis.com/auth/webmasters" in str(tokens.get("scope", "")).split():
        raise RuntimeError("Google granted an undesired read/write scope")
    access, refresh = tokens.get("access_token"), tokens.get("refresh_token")
    if not isinstance(access, str) or not isinstance(refresh, str) or not refresh:
        raise RuntimeError("Offline Google refresh token absent; retry with OAuth consent")
    sites = http_json(SITES_URL, token=access).get("siteEntry", [])
    allowed = {"siteOwner", "siteFullUser", "siteRestrictedUser"}
    chosen = next((r for r in sites if isinstance(r, dict) and
                   r.get("siteUrl") == TARGET_SITE and r.get("permissionLevel") in allowed), None)
    if chosen is None:
        chosen = next((r for r in sites if isinstance(r, dict) and
                       r.get("siteUrl") == "sc-domain:mokshagoa.com" and
                       r.get("permissionLevel") in allowed), None)
    if chosen is None:
        raise RuntimeError("The authorized Google account cannot read the Moksha Search Console property")
    site = gsc_metrics.property_id(chosen["siteUrl"])
    end = date.today() - timedelta(days=4)
    start = end - timedelta(days=27)
    body = {
        "startDate": start.isoformat(), "endDate": end.isoformat(),
        "dimensions": ["query"], "rowLimit": 250, "dataState": "final"
    }
    endpoint = "https://www.googleapis.com/webmasters/v3/sites/" + quote(site, safe="") + "/searchAnalytics/query"
    req = Request(endpoint, data=json.dumps(body).encode(),
                  headers={"Content-Type": "application/json", "Authorization": "Bearer " + access},
                  method="POST")
    with urlopen(req, timeout=25) as response:
        obj = json.load(response)
    rows = [{**r, "query": r["keys"][0]} for r in obj.get("rows", [])[:250]
            if isinstance(r, dict) and isinstance(r.get("keys"), list) and len(r["keys"]) == 1]
    if gsc_metrics.SECRETS.exists():
        raise RuntimeError("Local GSC secret file appeared concurrently; refusing overwrite")
    # A successful first-party Search Analytics API response establishes the
    # user's actual property access. Private local records are written only now.
    state = {"site_url": site, "scope": SCOPE, "client_id": client["client_id"],
             "client_secret": client["client_secret"], "refresh_token": refresh}
    private_write(gsc_metrics.SECRETS, state)
    digest = hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()
    stored = gsc_metrics.save_rows(rows, site=site, start=body["startDate"], end=body["endDate"],
                                   source="google_gsc_searchanalytics_api", digest=digest)
    return {"site": site, "query_rows": stored["rows"],
            "period": f'{body["startDate"]} to {body["endDate"]}',
            "read_only": True, "credential_permissions": "0600"}


def build_handler(server_state):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            # Do not log OAuth codes, app client data, state, or enrollment tokens.
            return

        def respond(self, status, content, *, location=None):
            payload = content.encode("utf-8")
            self.send_response(status)
            self.send_header("Cache-Control", "no-store")
            self.send_header("Pragma", "no-cache")
            self.send_header("Referrer-Policy", "no-referrer")
            self.send_header("X-Frame-Options", "DENY")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'none'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'; style-src 'unsafe-inline'")
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(payload)))
            if location: self.send_header("Location", location)
            self.end_headers()
            self.wfile.write(payload)

        def check(self, path):
            if self.headers.get("Host") != f"{HOST}:{PORT}":
                return False
            token = server_state["key"]
            return hmac.compare_digest(path, "/setup/" + token) or hmac.compare_digest(path, "/upload/" + token)

        def do_GET(self):
            parsed = urlsplit(self.path)
            if self.headers.get("Host") != f"{HOST}:{PORT}":
                return self.respond(403, "<h2>Forbidden</h2>")
            if hmac.compare_digest(parsed.path, "/setup/" + server_state["key"]):
                if server_state.get("client"):
                    return self.respond(409, "<h2>Google OAuth consent already started.</h2>")
                page = f"""<!doctype html><meta charset="utf-8"><title>Matrix GSC read-only</title>
                <style>body{{font:16px sans-serif;max-width:680px;margin:60px auto;padding:18px;line-height:1.6}}
                button{{padding:10px 22px}}</style>
                <h2>Business House Matrix · Connect Search Console</h2>
                <p>This private page runs only on <b>127.0.0.1</b> on the Mac. It will use
                the existing Marketing Brain and request <b>Search Console read-only</b> access.</p>
                <ol><li><a href="https://console.cloud.google.com/apis/library/searchconsole.googleapis.com">Enable Google Search Console API</a> in your Google Cloud project.</li>
                <li><a href="https://console.cloud.google.com/auth/clients">Create OAuth client</a> of type
                <b>Desktop application</b> (add your Google account as test user if necessary).</li>
                <li>Download its JSON file and upload below. You'll be redirected to Google's consent page.</li></ol>
                <form enctype="multipart/form-data" method="POST" action="/upload/{escape(server_state["key"])}">
                <input name="oauth_client" type="file" accept=".json,application/json" required>
                <button type="submit">Continue to Google authorization</button></form>
                <p>Property requested: <code>https://mokshagoa.com/</code> or
                <code>sc-domain:mokshagoa.com</code>. No passwords or refresh tokens go to ChatGPT.</p>"""
                return self.respond(200, page)
            if parsed.path == "/oauth2callback":
                if not server_state.get("client") or not server_state.get("oauth_state"):
                    return self.respond(400, "<h2>No OAuth session started.</h2>")
                args = parse_qs(parsed.query)
                if not args.get("state") or not hmac.compare_digest(args["state"][0], server_state["oauth_state"]):
                    return self.respond(403, "<h2>Invalid OAuth state.</h2>")
                if "error" in args:
                    return self.respond(400, "<h2>Google consent denied.</h2>")
                code = args.get("code", [None])[0]
                if not isinstance(code, str) or len(code) > 2048:
                    return self.respond(400, "<h2>Google authorization code missing.</h2>")
                if server_state.get("exchanging"):
                    return self.respond(409, "<h2>OAuth already processed.</h2>")
                server_state["exchanging"] = True
                try:
                    result = complete(server_state["client"], code, server_state["verifier"])
                except (RuntimeError, ValueError, OSError, HTTPError, URLError) as exc:
                    # No sensitive raw exception or Google returned payload in the page.
                    server_state["done"] = True
                    return self.respond(502, "<h2>Search Console authorization could not be verified.</h2><p>Check Google Cloud API enablement and whether the signed-in Google account can read the selected property. See the Mac diagnostic receipt for the error category.</p>")
                server_state["done"] = True
                return self.respond(200, f"<h2>Search Console connected securely</h2><p>Property: <b>{escape(result['site'])}</b></p><p>Verified read-only API data imported: <b>{result['query_rows']}</b> rows for <b>{escape(result['period'])}</b>.</p><p>Return to ChatGPT to verify the Marketing Brain integration.</p>")
            return self.respond(404, "<h2>Not found.</h2>")

        def do_POST(self):
            if not self.check(urlsplit(self.path).path) or not self.path.startswith("/upload/"):
                return self.respond(403, "<h2>Forbidden</h2>")
            if server_state.get("client"):
                return self.respond(409, "<h2>Authorization already started.</h2>")
            if self.headers.get("Origin") not in (None, f"http://{HOST}:{PORT}"):
                return self.respond(403, "<h2>Origin mismatch.</h2>")
            try:
                n = int(self.headers.get("Content-Length", "0"))
                if not 0 < n <= MAX_UPLOAD: raise ValueError("Upload exceeds bound")
                client = parse_form_upload(self.headers.get("Content-Type", ""), self.rfile.read(n))
                verifier = secrets.token_urlsafe(72)
                state = secrets.token_urlsafe(32)
                challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
                auth = AUTH_URL + "?" + urlencode({
                    "client_id": client["client_id"], "redirect_uri": CALLBACK,
                    "response_type": "code", "scope": SCOPE, "access_type": "offline",
                    "prompt": "consent", "state": state,
                    "code_challenge": challenge, "code_challenge_method": "S256"
                })
                server_state.update({"client":client, "verifier":verifier, "oauth_state":state})
            except (ValueError, KeyError, TypeError, UnicodeError, json.JSONDecodeError):
                return self.respond(400, "<h2>Invalid Google Desktop OAuth client JSON.</h2>")
            return self.respond(303, "Redirecting to Google…", location=auth)
    return Handler


def serve():
    token_data = json.loads(TOKEN_FILE.read_text())
    if TOKEN_FILE.stat().st_mode & 0o077:
        raise RuntimeError("Enrollment token file permissions not private")
    if int(token_data["expires"]) <= time.time():
        raise RuntimeError("Enrollment token expired; obtain new one")
    state = {"key": token_data["key"], "done": False}
    end = min(int(token_data["expires"]), int(time.time()) + ENROLL_MAX_SECONDS)
    httpd = HTTPServer((HOST, PORT), build_handler(state))
    httpd.timeout = 2
    try:
        while time.time() < end and not state["done"]:
            httpd.handle_request()
    finally:
        httpd.server_close()
        TOKEN_FILE.unlink(missing_ok=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=("issue", "serve", "status"))
    a = p.parse_args()
    if a.command == "issue":
        print(issue())
    elif a.command == "serve":
        serve()
    else:
        print(json.dumps({"running_setup": TOKEN_FILE.exists(),
                          "gsc_oauth_configured": gsc_metrics.status()["oauth_configured"],
                          "listener": f"{HOST}:{PORT}"}))


if __name__ == "__main__":
    try: main()
    except (RuntimeError, ValueError, OSError) as exc:
        # No token or OAuth body should leak via exception.
        print("GSC_ENROLL_ERROR:", type(exc).__name__, file=sys.stderr)
        sys.exit(2)
