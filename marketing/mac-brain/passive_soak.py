#!/usr/bin/env python3
"""Passive 24h gate-4 telemetry; never applies CPU load or modifies safety policy.

The passive health observer CANNOT by itself certify load/reboot/fault resilience.
"""
import argparse
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

import reel_bridge

ROOT = Path(__file__).resolve().parent / "data" / "gate4"
SAFE_ID = re.compile(r"^passive-[0-9]{8}-[a-z0-9]{1,24}$")
SERVICES = ("generic-linux-automator.service", "cron.service", "mbpfan.service", "thermald.service")


def stamp():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def fan_rpm():
    for hw in Path("/sys/class/hwmon").glob("hwmon*"):
        try:
            name = (hw/"name").read_text().strip().lower()
            if "applesmc" not in name:
                continue
            values = [int(p.read_text()) for p in hw.glob("fan*_input")]
            return max(values) if values else None
        except (ValueError, OSError):
            pass
    return None


def sample():
    t = reel_bridge.mac_temperature_c()
    if t is None or not 0 < t < 150:
        raise RuntimeError("No trustworthy Mac thermal sensor")
    try:
        load_1 = os.getloadavg()[0]
    except OSError:
        load_1 = None
    services = {}
    for unit in SERVICES:
        r = subprocess.run(["/usr/bin/systemctl", "is-active", unit],
                           timeout=3, capture_output=True, text=True)
        services[unit] = r.returncode == 0 and r.stdout.strip() == "active"
    return {"utc": stamp(), "max_sensor_c": t, "fan_rpm": fan_rpm(),
            "load1": load_1, "services": services}


def save_status(dst, state):
    temp = dst.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(state, f, separators=(",", ":"), sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, dst)
    dst.chmod(0o600)


def prepare(run_id):
    if not SAFE_ID.fullmatch(run_id):
        raise ValueError("Invalid passive run ID")
    path = ROOT/run_id
    path.mkdir(parents=True, mode=0o700, exist_ok=False)
    path.chmod(0o700)
    csv_path = path/"samples.csv"
    with csv_path.open("x", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["utc","max_sensor_c","fan_rpm","load1",
                    *SERVICES])
    csv_path.chmod(0o600)
    return path


def append_sample(path, record):
    with (path/"samples.csv").open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([record["utc"],record["max_sensor_c"],record["fan_rpm"],
                         record["load1"],*[record["services"][x] for x in SERVICES]])
        f.flush()
        os.fsync(f.fileno())


def run(run_id, duration_seconds=86400, interval_seconds=300):
    if not (60 <= interval_seconds <= 3600 and 3600 <= duration_seconds <= 86400):
        raise ValueError("Passive soak bounded at 1-24h and 1-60min intervals")
    path = prepare(run_id)
    start = time.monotonic()
    state={"run_id":run_id,"state":"running","start_utc":stamp(),"last_utc":None,
           "samples":0,"max_observed_c":None,"min_observed_c":None,
           "service_failures":0,"thermal_emergency":False,
           "result":"NOT_CERTIFIED","kind":"passive_no_load"}
    save_status(path/"status.json",state)
    deadline=start+duration_seconds
    try:
        while True:
            record=sample()
            append_sample(path,record)
            t=record["max_sensor_c"]
            state["samples"]+=1
            state["last_utc"]=record["utc"]
            state["max_observed_c"]=max(t, state["max_observed_c"] or t)
            state["min_observed_c"]=min(t, state["min_observed_c"] or t)
            if not all(record["services"].values()):
                state["service_failures"]+=1
            if t >= 92:
                state["thermal_emergency"]=True
                state["state"]="stopped_thermal_emergency"
                break
            save_status(path/"status.json",state)
            if time.monotonic() >= deadline:
                state["state"]="completed_passive_window"
                break
            time.sleep(min(interval_seconds,max(0,deadline-time.monotonic())))
    except Exception as e:
        state["state"]="failed"
        state["failure_class"]=type(e).__name__
        raise
    finally:
        state["end_utc"]=stamp()
        state["duration_seconds"]=round(time.monotonic()-start,2)
        state["result"]="NOT_CERTIFIED"  # Passive log never certifies active soak / reboot.
        save_status(path/"status.json",state)
    return state


def main():
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="command",required=True)
    x=sub.add_parser("run")
    x.add_argument("run_id");x.add_argument("--interval",type=int,default=300)
    x.add_argument("--duration",type=int,default=86400)
    x=sub.add_parser("status");x.add_argument("run_id")
    a=p.parse_args()
    if a.command=="run": print(json.dumps(run(a.run_id,a.duration,a.interval)))
    else:
        if not SAFE_ID.fullmatch(a.run_id): raise ValueError("Invalid run ID")
        print((ROOT/a.run_id/"status.json").read_text())


if __name__=="__main__":
    main()
