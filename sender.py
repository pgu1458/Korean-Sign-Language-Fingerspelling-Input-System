import socket

class Sender:
    def __init__(self, host="127.0.0.1", port=9000):
        self.host = host
        self.port = port
        self.sock = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"서버 연결 성공: {self.host}:{self.port}")
        except Exception as e:
            print(f"연결 실패: {e}")
            self.sock = None

    def send(self, char):
        if self.sock is None:
            return
        try:
            if (char.startswith("CMD:") or char.startswith("STATE:") or 
                char.startswith("ERROR:") or char.startswith("VOICE:")):
                msg = f"{char}\n"
            else:
                msg = f"CHAR:{char}\n"
            self.sock.sendall(msg.encode("utf-8"))
            print(f"전송: {msg.strip()}")
        except Exception as e:
            print(f"전송 실패: {e}")
            self.sock = None

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            print("연결 종료")