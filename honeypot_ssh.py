import socket
import threading
import paramiko
from datetime import datetime

# ==== [ Host key ] ====
host_key = paramiko.RSAKey.generate(2048)

# ==== [ Fake responses for common commands ] ====
FAKE_RESPONSES = {
    "id": "uid=1000(testuser) gid=1000(testuser) groups=1000(testuser)\n",
    "whoami": "testuser\n",
    "uname -a": "Linux honeypot 5.15.0-91-generic #101 SMP x86_64 GNU/Linux\n",
    "uname -r": "5.15.0-91-generic\n",
    "hostname": "honeypot\n",
    "pwd": "/home/testuser\n",
    "ls": "Desktop  Documents  Downloads  Music  Pictures  Videos\n",
    "exit": "Goodbye!\n"
}

# ==== [ SSH Server class ] ====
class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()
        self.username = ""

    def check_auth_password(self, username, password):
        print(f"[LOGIN ATTEMPT] {username}:{password} at {datetime.now()}")
        with open("logins.txt", "a") as f:
            f.write(f"{datetime.now()} - USERNAME: {username} PASSWORD: {password}\n")
        self.username = username
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

# ==== [ Client session handler ] ====
def handle_connection(client):
    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(host_key)
        server = SSHServer()
        transport.start_server(server=server)

        channel = transport.accept(20)
        if channel is None:
            return

        server.event.wait(10)
        channel.send("Welcome to Fake SSH Server!\n")
        channel.send("Type 'exit' to quit.\n\n")

        while True:
            command = ""
            prompt = f"{server.username}@honeypot:~$ "
            channel.send(prompt)

            while True:
                char = channel.recv(1).decode("utf-8", errors="ignore")
                if char in ['\r', '\n']:
                    channel.send('\r\n')
                    break
                elif char == '\x7f':  # Handle backspace
                    if command:
                        command = command[:-1]
                        channel.send('\b \b')
                else:
                    command += char
                    channel.send(char)

            command = command.strip()
            if not command:
                continue

            print(f"[{server.username}] Ran command: {command}")
            with open("commands.txt", "a") as f:
                f.write(f"{datetime.now()} - {server.username} ran: {command}\n")

            # ==== [ Fake response handling ] ====
            if command in FAKE_RESPONSES:
                response = FAKE_RESPONSES[command]
                if not response.endswith("\n"):
                    response += "\n"
                channel.send(response)
                channel.send("\n")
                if command == "exit":
                    break
            else:
                channel.send("\n")  # blank response, no error message

        channel.close()

    except Exception as e:
        print(f"[!] Error: {e}")
    finally:
        client.close()

# ==== [ Start honeypot server ] ====
def start_honeypot(host="0.0.0.0", port=2222):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    sock.listen(100)
    print(f"[+] SSH Honeypot running on port {port}...")

    while True:
        client, addr = sock.accept()
        print(f"[+] New connection from {addr[0]}")
        threading.Thread(target=handle_connection, args=(client,), daemon=True).start()

# ==== [ Main ] ====
if __name__ == "__main__":
    start_honeypot()
