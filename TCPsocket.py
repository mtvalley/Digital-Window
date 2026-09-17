# TCPsocket.py
import socket

class TCPServer:
    def __init__(self, host='127.0.0.1', port=3000):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen(1)
        print(f"✅ 서버 대기 중: {host}:{port}")
        self.conn, self.addr = self.sock.accept()
        print(f"🔗 연결됨: {self.addr}")

    def send_xyz(self, x, y, z):
        try:
            msg = f"{x*-5},{y*-5},{z*0}"
            self.conn.sendall(msg.encode())
            print(f"📤 전송된 데이터: {msg}")
        except Exception as e:
            print(f"⚠️ 전송 오류: {e}")
