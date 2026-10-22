"""Fail-closed static HTML policy for the public synthetic Dev Operator.

No active elements, event attributes, cross-origin resource loading or dynamic
CSS. Run it before accepting a model proposal AND independently inside Bwrap.
"""
from html.parser import HTMLParser
import re

class StaticHTMLViolation(ValueError):
    pass

TAGS=frozenset({
    "html","head","body","meta","title","style","main",
    "header","footer","section","article","nav","aside","div","span",
    "h1","h2","h3","h4","h5","h6","p","ul","ol","li","small",
    "strong","em","b","i","code","pre","blockquote","hr","br",
    "table","thead","tbody","tfoot","tr","th","td",
})
VOID=frozenset({"meta","hr","br"})
CSS_UNSAFE=re.compile(
    r"(?is)\\|@import\b|@font-face\b|@namespace\b|url\s*\(|"
    r"image-set\s*\(|expression\s*\(|-moz-binding\b|behavior\s*:|"
    r"javascript\s*:|data\s*:|https?\s*:|//|@\\x69mport\b"
)
SAFE_CLASS=re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,60}(?:\s+[a-zA-Z][a-zA-Z0-9_-]{0,60}){0,10}$")
SAFE_ID=re.compile(r"^[a-zA-Z][a-zA-Z0-9_-]{0,70}$")
SAFE_VIEWPORT=re.compile(r"^width=device-width(?:\s*,\s*initial-scale=(?:1|1\.0))?$")
DOCTYPE=re.compile(r"(?is)^\s*<!doctype\s+html\s*>")
MAX_DOCUMENT_BYTES=32000

def css_safe(text):
    if not isinstance(text,str) or CSS_UNSAFE.search(text):
        raise StaticHTMLViolation("css_active_content")
    # External fetch via HTML entity, or hidden stylesheet escape syntax,
    # is not needed in the intentionally offline/synthetic static profile.
    if "\x00" in text or "<" in text or ">" in text:
        raise StaticHTMLViolation("css_malformed")
    return True

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack=[]
        self.visited=[]
        self.doctype=False
        self.viewport=False
        self.lang=False
        self.main_count=0
        self.errors=[]
    def handle_decl(self,decl):
        if self.doctype or decl.lower().strip()!="doctype html":
            raise StaticHTMLViolation("doctype_not_html5")
        self.doctype=True
    def unknown_decl(self,decl):
        raise StaticHTMLViolation("unknown_declaration")
    def handle_comment(self,data):
        raise StaticHTMLViolation("comments_not_allowed")
    def handle_pi(self,data):
        raise StaticHTMLViolation("processing_instruction")
    def handle_startendtag(self,tag,attrs):
        if tag not in VOID: raise StaticHTMLViolation("unexpected_self_closing_tag")
        self.handle_starttag(tag,attrs)
    def handle_starttag(self,tag,attrs):
        if not self.doctype or tag not in TAGS:
            raise StaticHTMLViolation("active_or_unknown_element")
        if not self.stack and tag!="html":
            raise StaticHTMLViolation("root_not_html")
        if self.stack and self.stack[0]!="html":
            raise StaticHTMLViolation("invalid_root")
        if tag=="html" and self.stack:
            raise StaticHTMLViolation("nested_html")
        if tag=="head" and self.stack!=["html"]:
            raise StaticHTMLViolation("head_placement")
        if tag=="body" and self.stack!=["html"]:
            raise StaticHTMLViolation("body_placement")
        if tag in ("meta","title","style") and (not self.stack or self.stack[-1]!="head"):
            raise StaticHTMLViolation("metadata_outside_head")
        if tag=="main" and "body" not in self.stack:
            raise StaticHTMLViolation("main_outside_body")
        names=[name.lower() if isinstance(name,str) else "" for name,_ in attrs]
        if len(set(names))!=len(names):
            raise StaticHTMLViolation("duplicate_attribute")
        values={name.lower():value for name,value in attrs}
        if tag=="meta":
            if set(values)=={"charset"} and str(values["charset"]).lower()=="utf-8":
                pass
            elif set(values)=={"name","content"} and str(values["name"]).lower()=="viewport" and SAFE_VIEWPORT.fullmatch(str(values["content"]).replace(" ","")):
                self.viewport=True
            else:
                raise StaticHTMLViolation("meta_not_allowlisted")
        elif tag=="html":
            if set(values)!={"lang"} or not re.fullmatch(r"[a-z]{2}(?:-[A-Z]{2})?",str(values["lang"])):
                raise StaticHTMLViolation("language_required")
            self.lang=True
        elif tag in ("head","body","title","style"):
            if values:raise StaticHTMLViolation("metadata_attribute_not_allowed")
        else:
            for name,value in values.items():
                if value is None:raise StaticHTMLViolation("null_attribute")
                if name=="class":
                    if not SAFE_CLASS.fullmatch(value):raise StaticHTMLViolation("bad_class")
                elif name=="id":
                    if not SAFE_ID.fullmatch(value):raise StaticHTMLViolation("bad_id")
                elif name=="style":
                    css_safe(value)
                elif name=="role":
                    if not re.fullmatch(r"[a-z-]{1,30}",value):raise StaticHTMLViolation("bad_role")
                elif name=="title":
                    if len(value)>180:raise StaticHTMLViolation("title_too_long")
                elif name=="tabindex":
                    if value not in ("0","-1"):raise StaticHTMLViolation("bad_tabindex")
                elif name.startswith("aria-"):
                    if not re.fullmatch(r"aria-[a-z-]{2,35}",name) or len(value)>180:
                        raise StaticHTMLViolation("bad_aria_attribute")
                else:
                    # Denies on*, href/src, style/script URLs, srcdoc, data-*,
                    # form actions, remote assets, hidden DOM events, etc.
                    raise StaticHTMLViolation("attribute_not_allowlisted")
        self.visited.append(tag)
        if tag=="main":self.main_count+=1
        if tag not in VOID:self.stack.append(tag)
    def handle_endtag(self,tag):
        if not self.stack or self.stack[-1]!=tag:
            raise StaticHTMLViolation("unbalanced_html")
        self.stack.pop()
    def handle_data(self,data):
        if self.stack and self.stack[-1]=="style":
            css_safe(data)
        if not self.stack and data.strip():
            raise StaticHTMLViolation("text_outside_html")

def validate_static_html(text):
    if not isinstance(text,str) or len(text.encode("utf-8"))>MAX_DOCUMENT_BYTES:
        raise StaticHTMLViolation("document_size_or_type")
    if not DOCTYPE.match(text):
        raise StaticHTMLViolation("missing_html5_doctype")
    parser=Inspector()
    try:
        parser.feed(text)
        parser.close()
    except StaticHTMLViolation:
        raise
    except Exception as exc:
        raise StaticHTMLViolation("html_parser_failure") from exc
    if parser.stack or not parser.doctype or parser.main_count!=1 or not parser.lang or not parser.viewport:
        raise StaticHTMLViolation("incomplete_static_document")
    if parser.visited.count("html")!=1 or parser.visited.count("head")!=1 or parser.visited.count("body")!=1:
        raise StaticHTMLViolation("structural_landmarks_missing")
    return True
