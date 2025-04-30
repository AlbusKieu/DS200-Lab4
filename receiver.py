import socket
import os
import base64

HOST = '127.0.0.1'
PORT = 5001
SAVE_DIR = 'received_data'
os.makedirs(SAVE_DIR, exist_ok=True)

def save_image(label, data, idx):
    label_dir = os.path.join(SAVE_DIR, label)
    os.makedirs(label_dir, exist_ok=True)
    file_path = os.path.join(label_dir, f'image_{idx}.jpg')
    with open(file_path, 'wb') as f:
        f.write(base64.b64decode(data))

def main():
    with socket.socket() as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Đang chờ dữ liệu...")
        conn, _ = s.accept()
        with conn:
            buffer = b''
            idx = 0
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                buffer += data
                while b"<END>" in buffer:
                    packet, buffer = buffer.split(b"<END>", 1)
                    label_data_split = packet.split(b'|', 1)
                    if len(label_data_split) != 2:
                        continue
                    label = label_data_split[0].decode()
                    img_data = label_data_split[1]
                    save_image(label, img_data, idx)
                    print(f"Đã nhận và lưu: image_{idx}.jpg (label: {label})")
                    idx += 1
    print("Hoàn tất nhận dữ liệu.")

if __name__ == '__main__':
    main()
