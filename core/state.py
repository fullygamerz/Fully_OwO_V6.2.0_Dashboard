"""
Fully OwO - State Manager
Writes live bot state to state.json and logs.json
so the web dashboard can read real data.
"""

import json
import os
from datetime import datetime
from collections import deque

STATE_FILE = "state.json"
LOGS_FILE  = "logs.json"
MAX_LOGS   = 150

_log_cache = deque(maxlen=MAX_LOGS)
_log_loaded = False

def _load_logs():
    global _log_loaded
    if _log_loaded:
        return
    _log_loaded = True
    try:
        if os.path.exists(LOGS_FILE):
            with open(LOGS_FILE, "r") as f:
                data = json.load(f)
                for entry in reversed(data):
                    _log_cache.appendleft(entry)
    except:
        pass

def write_state(
    running=False,
    has_started=False,
    sleep_mode=False,
    speed_mode="durable",
    commands_sent=0,
    gems_used=0,
    hb_active=False,
    lifetime_cycles=0,
    lifetime_day_skip=False,
    start_time=None,
    farming_start=None,
    captcha_solver_ok=True,
    **kwargs
):
    try:
        uptime_str = ""
        if start_time:
            elapsed = (datetime.now() - start_time).total_seconds()
            h, rem = divmod(int(elapsed), 3600)
            m, s   = divmod(rem, 60)
            uptime_str = f"{h}h {m}m {s}s"

        state = {
            "running":           running,
            "has_started":       has_started,
            "sleep_mode":        sleep_mode,
            "speed_mode":        speed_mode,
            "commands_sent":     commands_sent,
            "gems_used":         gems_used,
            "hb_active":         hb_active,
            "lifetime_cycles":   lifetime_cycles,
            "lifetime_day_skip": lifetime_day_skip,
            "uptime":            uptime_str,
            "start_time":        start_time.isoformat() if start_time else None,
            "captcha_solver":    captcha_solver_ok,
            "updated_at":        datetime.now().isoformat(),
        }
        with open(STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)
    except:
        pass


def add_log(icon, message, log_type="info"):
    _load_logs()
    entry = {
        "time":  datetime.now().strftime("%H:%M:%S"),
        "icon":  icon,
        "msg":   message,
        "type":  log_type,
    }
    _log_cache.appendleft(entry)
    try:
        with open(LOGS_FILE, "w") as f:
            json.dump(list(_log_cache), f)
    except:
        pass


def read_state():
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE) as f:
                return json.load(f)
    except:
        pass
    return {}


def read_logs(limit=80):
    _load_logs()
    return list(_log_cache)[:limit]
