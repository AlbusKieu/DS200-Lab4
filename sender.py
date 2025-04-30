import os
import socket
import base64

HOST = '127.0.0.1'
PORT = 5001
DATA_DIR = 'data'  # Gốc chứa các folder: cloudy, desert,...

def encode_image(file_path):
    with open(file_path, 'rb') as f:
        return base64.b64encode(f.read())

def main():
    with socket.socket() as s:
        s.connect((HOST, PORT))
        for label in os.listdir(DATA_DIR):
            label_path = os.path.join(DATA_DIR, label)
            if not os.path.isdir(label_path):
                continue
            for img_file in os.listdir(label_path):
                img_path = os.path.join(label_path, img_file)
                encoded = encode_image(img_path)
                message = f"{label}|".encode() + encoded + b"<END>"
                s.sendall(message)
                print(f"Đã gửi: {img_file} (label: {label})")
    print("Hoàn tất gửi ảnh.")

if __name__ == '__main__':
    main()
