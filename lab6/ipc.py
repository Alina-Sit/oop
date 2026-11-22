import json
import os
import queue
import socket
import threading

HOST = "127.0.0.1"
PORT_OBJECT2 = 50102
PORT_OBJECT3 = 50103


def send(port, message, timeout=3.0):
    with socket.create_connection((HOST, port), timeout=timeout) as conn:
        conn.settimeout(timeout)
        conn.sendall((json.dumps(message) + "\n").encode("utf-8"))
        data = b""
        while not data.endswith(b"\n"):
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
    return json.loads(data.decode("utf-8")) if data else {}


def is_alive(port):
    try:
        return send(port, {"cmd": "ping"}, timeout=1.0).get("ok", False)
    except (OSError, ValueError):
        return False


class MessageServer:
    def __init__(self, port, handler):
        self.handler = handler
        self.inbox = queue.Queue()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if os.name != "nt":
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((HOST, port))
        self.sock.listen(5)
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _accept_loop(self):
        while True:
            try:
                conn, _ = self.sock.accept()
            except OSError:
                return
            threading.Thread(target=self._read, args=(conn,), daemon=True).start()

    def _read(self, conn):
        try:
            conn.settimeout(3.0)
            data = b""
            while not data.endswith(b"\n"):
                chunk = conn.recv(4096)
                if not chunk:
                    break
                data += chunk
            message = json.loads(data.decode("utf-8"))
        except (OSError, ValueError):
            conn.close()
            return
        self.inbox.put((message, conn))

    def poll(self, root):
        try:
            while True:
                message, conn = self.inbox.get_nowait()
                try:
                    reply = self.handler(message)
                except Exception as error:
                    reply = {"ok": False, "error": str(error)}
                try:
                    conn.sendall((json.dumps(reply) + "\n").encode("utf-8"))
                except OSError:
                    pass
                conn.close()
        except queue.Empty:
            pass
        root.after(40, self.poll, root)

    def start(self, root):
        root.after(40, self.poll, root)

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass
