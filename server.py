"""
Fully OwO — Web Dashboard Server  |  Fully Development
Double-click start_dashboard.bat to launch.
Then open: http://localhost:5000
"""

import os, json, threading, subprocess, sys
from datetime import datetime
from flask import Flask, jsonify, send_file, request

app = Flask(__name__)

# ─── Helpers ──────────────────────────────────────────────────────────────────
def _bot_dir():
    return os.path.dirname(os.path.abspath(__file__))

def _path(filename):
    return os.path.join(_bot_dir(), filename)

def _read_json(path, fallback=None):
    try:
        if os.path.exists(path):
            with open(path, "r") as f:
                return json.load(f)
    except:
        pass
    return fallback if fallback is not None else {}

def _write_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def _venv_python():
    """Find the venv Python executable (Windows first, then Linux/Mac)."""
    candidates = [
        _path(os.path.join("venv", "Scripts", "python.exe")),
        _path(os.path.join("venv", "bin",     "python")),
        _path(os.path.join("venv", "bin",     "python3")),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return sys.executable

# ─── Token helpers ────────────────────────────────────────────────────────────
CONFIG_PATH = _path("config.json")

def _get_token():
    return _read_json(CONFIG_PATH, {}).get("TOKEN", "")

def _has_token():
    t = _get_token()
    return bool(t and t.strip())

# ─── Bot Process Manager ──────────────────────────────────────────────────────
_bot_proc  = None
_proc_lock = threading.Lock()

def _is_running():
    with _proc_lock:
        return _bot_proc is not None and _bot_proc.poll() is None

# ─── State / Logs ─────────────────────────────────────────────────────────────
def _read_state():
    s = _read_json(_path("state.json"))
    s["process_alive"] = _is_running()
    s["has_token"]     = _has_token()
    return s

def _read_logs(limit=80):
    return _read_json(_path("logs.json"), [])[:limit]

def _read_hb():
    return _read_json(_path("fullygamerzhbtps.json"))

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    p = _path("owo-dashboard.html")
    if os.path.exists(p):
        return send_file(p)
    return "<h2>owo-dashboard.html not found</h2>", 404


# ── Token ──────────────────────────────────────────────────────────────────────

@app.route("/api/token", methods=["GET"])
def api_get_token():
    t = _get_token()
    masked = ("*" * (len(t) - 6) + t[-6:]) if len(t) > 6 else ("*" * len(t))
    return jsonify({"has_token": _has_token(), "masked": masked if _has_token() else ""})


@app.route("/api/token", methods=["POST"])
def api_set_token():
    body  = request.get_json(silent=True) or {}
    token = (body.get("token") or "").strip()
    if not token:
        return jsonify({"ok": False, "msg": "Token cannot be empty"})
    parts = token.split(".")
    if len(parts) != 3:
        return jsonify({"ok": False, "msg": "Doesn't look like a valid Discord token (need 3 parts separated by dots)"})
    _write_json(CONFIG_PATH, {"TOKEN": token})
    return jsonify({"ok": True, "msg": "Token saved!"})


@app.route("/api/token", methods=["DELETE"])
def api_delete_token():
    _write_json(CONFIG_PATH, {"TOKEN": ""})
    return jsonify({"ok": True, "msg": "Token removed"})


# ── Status / Logs ──────────────────────────────────────────────────────────────

@app.route("/api/status")
def api_status():
    state = _read_state()
    state["hb_data"] = _read_hb()
    return jsonify(state)


@app.route("/api/logs")
def api_logs():
    limit = int(request.args.get("limit", 80))
    return jsonify(_read_logs(limit))


# ── Bot Control ────────────────────────────────────────────────────────────────

@app.route("/api/start", methods=["POST"])
def api_start():
    global _bot_proc
    if not _has_token():
        return jsonify({"ok": False, "msg": "No token set — go to Settings first!"})
    if _is_running():
        return jsonify({"ok": False, "msg": "Bot is already running"})
    python = _venv_python()
    with _proc_lock:
        try:
            import os as _os
            env = _os.environ.copy()
            env["PYTHONIOENCODING"] = "utf-8"
            env["PYTHONUTF8"] = "1"
            _bot_proc = subprocess.Popen(
                [python, "-u", "main.py"],
                cwd=_bot_dir(),
                stdout=open("bot.log", "w", encoding="utf-8"),
                stderr=subprocess.STDOUT,
                env=env,
            )
            return jsonify({"ok": True, "msg": f"Bot started! (PID {_bot_proc.pid})"})
        except Exception as e:
            return jsonify({"ok": False, "msg": str(e)})


@app.route("/api/stop", methods=["POST"])
def api_stop():
    global _bot_proc
    with _proc_lock:
        if _bot_proc and _bot_proc.poll() is None:
            _bot_proc.terminate()
            try:
                _bot_proc.wait(timeout=5)
            except:
                _bot_proc.kill()
        _bot_proc = None
    return jsonify({"ok": True, "msg": "Bot stopped"})


@app.route("/api/ping")
def api_ping():
    return jsonify({"ok": True, "time": datetime.now().isoformat()})



@app.route("/api/botlog")
def api_botlog():
    try:
        p = _path("bot.log")
        if os.path.exists(p):
            with open(p, "r", errors="replace") as f:
                lines = f.readlines()
            return jsonify({"ok": True, "lines": lines[-50:]})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})
    return jsonify({"ok": False, "lines": []})


# ─── Entry ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print()
    print("=" * 58)
    print("   🐾  Fully OwO Dashboard  |  Fully Development")
    print("   🌐  Open: http://localhost:5000")
    print("=" * 58)
    print()
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
