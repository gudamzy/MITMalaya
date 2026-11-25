# MITMalaya

**IKB31603 — Ethical Hacking Tool Development · Category 3: Network Attack**
Group: **Haker Malaya**

> ⚠️ **EDUCATIONAL / LAB USE ONLY.** This tool performs an active ARP cache
> poisoning attack. Run it **only** inside an isolated lab you own or have
> **explicit written authorisation** to test. See the
> [Legal Disclaimer](#legal-disclaimer) and [Rules of Engagement](#rules-of-engagement-roe).

---

## What it does

`mitmalaya.py` demonstrates a Layer-2 **Man-in-the-Middle** attack. It sends
forged ARP replies so a victim associates the gateway's IP with the attacker's
MAC address (and the gateway associates the victim's IP with the attacker's
MAC). All traffic between victim and gateway is then relayed through the
attacker, who can observe it.

The tool is intentionally wrapped in safety controls so it can be used as a
teaching aid without becoming a ready-to-deploy weapon.

## Features / Ethical guardrails

| Requirement | How it is met |
|---|---|
| Startup legal disclaimer | Computer Crimes Act 1997 notice on every run |
| Explicit authorisation | Must type `I HAVE AUTHORIZATION` to proceed |
| Safe defaults | Target/gateway default to `127.0.0.1` |
| Scope enforcement | Refuses public IPs unless the operator types `OVERRIDE` |
| Bidirectional poisoning | Poisons both victim and gateway (full-duplex) |
| Kill switch | `Ctrl+C` restores both ARP tables and disables IP forwarding |
| Local-only output | Session log written to `./output/session.log` |

## Requirements

- Linux (raw sockets), Python 3.9+
- Run as **root** (writes `ip_forward`, sends raw frames)

```bash
pip install -r requirements.txt
```

## Usage

```bash
sudo python3 mitmalaya.py
```

You will be prompted for:
1. The authorisation phrase `I HAVE AUTHORIZATION`
2. **Target IP** — the victim (e.g. `192.168.251.129`)
3. **Gateway IP** — the router/gateway (e.g. `192.168.251.2`)
4. **Interface** — e.g. `eth0`

Press **Ctrl+C** to stop; the tool restores the ARP tables automatically.

## Lab setup used for testing

- **Attacker:** Kali Linux — interface `eth0`
- **Victim:** Windows 10
- **Network:** VMware, `192.168.251.0/24` (isolated — host-only / NAT)

### How success was verified
On the victim (`arp -a`), the gateway's MAC changes to the attacker's MAC
during the attack and is restored after the kill switch. `tcpdump` on the
attacker shows the victim's relayed traffic and the forged ARP replies.
Screenshots are in the project report.

## Rules of Engagement (RoE)

1. Run only against hosts you own or are authorised to test, inside an isolated lab.
2. Never run on a production, campus, or any real network you do not control.
3. Do not capture, store, or exfiltrate third-party data.
4. Always let the kill switch restore the network before leaving.

## Legal Disclaimer

This tool is provided for authorised security education only. Unauthorised use
against networks or devices you do not own or have explicit permission to test
is **illegal**. In Malaysia this may constitute an offence under the **Computer
Crimes Act 1997 (Act 563)**, including s.3 (unauthorised access), s.4, and s.5
(unauthorised modification), with penalties of fines and/or imprisonment. The
authors accept **no liability** for misuse.

## Team — Haker Malaya

| # | Name | Student ID |
|---|------|-----------|
| 1 | Muhammad Adam Danish bin Mohd Anis | 52215125900 |
| 2 | Muhammad Afiq Izzuddin bin Saifullizan | 52215125428 |
| 3 | Mohamad Syahmi Amrin bin Mursham | 52215125622 |
| 4 | Nurul Elysya Elina binti Zamri | 52215125032 |

## License

[MIT](LICENSE) © 2026 Haker Malaya
