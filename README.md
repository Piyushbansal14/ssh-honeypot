````markdown
# SSH Honeypot – Fake Linux Shell in Python

This project is a Python-based SSH honeypot that simulates a real Linux shell environment. It is designed to capture attacker behavior in a controlled setup by allowing them to log in and execute familiar shell commands, while all activity is monitored and logged.

## Features

- Simulated Linux shell with interactive prompt
- Realistic fake command outputs (`id`, `whoami`, `uname -a`, etc.)
- Logs all login attempts (usernames and passwords)
- Tracks and stores all executed commands
- Customizable fake responses for different commands
- No real system access is provided to the attacker

## How It Works

The honeypot listens for SSH connections on a specified port. When a user logs in (with any credentials), they are dropped into a fake shell that looks and behaves like a real one. Their inputs are logged, and command responses are generated based on pre-defined fake outputs.

## 🚀 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/piyushbansal14/ssh-honeypot.git
   cd ssh-honeypot

````

2. Install dependencies:

   ```bash
   pip install paramiko
   ```

3. Run the honeypot:

   ```bash
   python honeypot.py
   ```

## Usage

SSH into the honeypot using:

```bash
ssh testuser@localhost -p 2222
```

> Use any username and password — all credentials are accepted and logged.

## Logs

* `logins.txt`: Stores login attempts with timestamps.
* `commands.txt`: Stores all commands executed by the user.

## Disclaimer

This honeypot is intended for educational and research purposes only. Do not deploy it on production systems or public servers without proper security controls.

## License

This project is open-source and licensed under the MIT License.

```

---

## ✅ Optional Additions

If you want to look even more polished later, you can add:
- A `fake_commands.txt` list
- Demo screenshot
- Contribution guidelines (if public)
```
