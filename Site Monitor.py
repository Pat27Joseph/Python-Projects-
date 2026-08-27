"""
Site Monitor - a small defensive security tool for websites you own or
have explicit permission to monitor.

Checks performed on each run:
  1. Uptime / HTTP status      - is the site reachable and responding OK?
  2. TLS certificate expiry    - warn if the cert is expired or expiring soon.
  3. Security headers          - flag common security headers that are missing.
  4. Content drift             - detect unexpected changes to page content
                                  by comparing a hash against the last run.

Usage:
    python "Site Monitor.py" https://example.com
    python "Site Monitor.py" https://example.com --cert-warn-days 14
    python "Site Monitor.py" https://example.com --interval 300   # loop every 5 min

Only use this against sites you own or are authorized to test.
"""

import argparse
import hashlib
import json
import socket
import ssl
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

STATE_FILE = Path(__file__).with_name(".site_monitor_state.json")

RECOMMENDED_HEADERS = [
    "Strict-Transport-Security",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Content-Security-Policy",
    "Referrer-Policy",
]


def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def check_uptime(url, timeout=10):
    """Return (ok, status_code_or_error, response_or_None)."""
    try:
        response = requests.get(url, timeout=timeout)
        ok = response.status_code < 400
        return ok, response.status_code, response
    except requests.exceptions.RequestException as e:
        return False, str(e), None


def check_tls_certificate(hostname, port=443, timeout=10):
    """Return (days_remaining, expiry_datetime) or (None, None) on failure."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
        expiry = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        expiry = expiry.replace(tzinfo=timezone.utc)
        days_remaining = (expiry - datetime.now(timezone.utc)).days
        return days_remaining, expiry
    except (ssl.SSLError, socket.error, socket.timeout, ValueError, KeyError):
        return None, None


def check_security_headers(response):
    """Return a list of recommended headers that are missing."""
    if response is None:
        return RECOMMENDED_HEADERS
    return [h for h in RECOMMENDED_HEADERS if h not in response.headers]


def check_content_drift(url, response, state):
    """Compare a hash of the response body against the last saved hash."""
    if response is None:
        return None
    current_hash = hashlib.sha256(response.content).hexdigest()
    previous_hash = state.get(url, {}).get("content_hash")
    state.setdefault(url, {})["content_hash"] = current_hash
    if previous_hash is None:
        return None  # first run, nothing to compare against
    return current_hash != previous_hash


def run_check(url, cert_warn_days, timeout):
    print(f"\n=== Checking {url} @ {datetime.now().isoformat(timespec='seconds')} ===")
    state = load_state()

    ok, status, response = check_uptime(url, timeout=timeout)
    if ok:
        print(f"[OK]   Site is up (HTTP {status})")
    else:
        print(f"[FAIL] Site unreachable or erroring: {status}")

    hostname = urlparse(url).hostname
    if urlparse(url).scheme == "https" and hostname:
        days_remaining, expiry = check_tls_certificate(hostname)
        if days_remaining is None:
            print("[WARN] Could not verify TLS certificate")
        elif days_remaining < 0:
            print(f"[FAIL] TLS certificate EXPIRED on {expiry.date()}")
        elif days_remaining <= cert_warn_days:
            print(f"[WARN] TLS certificate expires in {days_remaining} day(s) ({expiry.date()})")
        else:
            print(f"[OK]   TLS certificate valid for {days_remaining} more day(s)")

    missing_headers = check_security_headers(response)
    if missing_headers:
        print(f"[WARN] Missing security headers: {', '.join(missing_headers)}")
    else:
        print("[OK]   All recommended security headers present")

    drifted = check_content_drift(url, response, state)
    if drifted is None:
        print("[INFO] Content hash recorded as baseline")
    elif drifted:
        print("[WARN] Page content changed since last check")
    else:
        print("[OK]   Page content unchanged since last check")

    save_state(state)


def main():
    parser = argparse.ArgumentParser(description="Monitor a website for uptime, TLS, header, and content issues.")
    parser.add_argument("url", help="Full URL of the site to monitor, e.g. https://example.com")
    parser.add_argument("--cert-warn-days", type=int, default=30, help="Warn if the TLS cert expires within this many days (default: 30)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--interval", type=int, default=0, help="Repeat the check every N seconds (default: run once)")
    args = parser.parse_args()

    if not urlparse(args.url).scheme:
        print("Error: URL must include a scheme, e.g. https://example.com", file=sys.stderr)
        sys.exit(1)

    if args.interval > 0:
        try:
            while True:
                run_check(args.url, args.cert_warn_days, args.timeout)
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nStopped monitoring.")
    else:
        run_check(args.url, args.cert_warn_days, args.timeout)


if __name__ == "__main__":
    main()
