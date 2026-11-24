# Commit plan — 5+ meaningful commits + v1.0.0 tag

Run from the repo folder after `git init`. Use your own git identity.

```bash
git init
git config user.name  "Your Name"
git config user.email "you@student.unikl.edu.my"

# 1 — license + ignore rules
git add LICENSE .gitignore
git commit -m "chore: add MIT license and .gitignore"

# 2 — dependencies
git add requirements.txt
git commit -m "chore: add scapy dependency"

# 3 — core tool
git add arpspoof.py
git commit -m "feat: ARP spoofing MITM tool with consent gate and scope prompt"

# 4 — (make a small real improvement, then commit — e.g. add a comment block
#      or tidy output — so this is a genuine change)
git add arpspoof.py
git commit -m "feat: full-duplex poisoning and Ctrl+C kill switch restore"

# 5 — documentation
git add README.md
git commit -m "docs: README with usage, RoE and Computer Crimes Act disclaimer"

# tag the release
git tag -a v1.0.0 -m "arpspoof v1.0.0"

# push (create the PUBLIC repo on GitHub first, then:)
git remote add origin https://github.com/<your-group>/arpspoof.git
git branch -M main
git push -u origin main --tags
```

Tip: to make commit #4 genuine, split the tool build — commit the basic
version at #3, then add the restore/kill-switch section and commit at #4.
