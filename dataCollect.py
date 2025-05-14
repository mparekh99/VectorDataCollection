import socket
import time
import os
from datetime import datetime
import anki_vector
from anki_vector.util import degrees
import keyboard


def take_picture(robot, save_dir="photos"):
    os.makedirs(save_dir, exist_ok=True)
    image = robot.camera.capture_single_image()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"vector_{timestamp}.jpg")
    image.raw_image.save(filename)
    print(f"[INFO] Saved image: {filename}")


def main():
    with anki_vector.Robot("00603f86") as robot:
        robot.behavior.set_head_angle(degrees(7.0))
        robot.behavior.set_lift_height(0.0)
        print("[INFO] Vector is ready.")

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)  # allow timeout so we can check ESC key
            s.bind(("localhost", 65432))
            s.listen()
            print("[INFO] Listening on port 65432...")

            while True:
                if keyboard.is_pressed('esc'):
                    print("[INFO] Escape key pressed. Exiting...")
                    break

                try:
                    conn, addr = s.accept()
                    with conn:
                        print(f"[INFO] Connected by {addr}")
                        while True:
                            if keyboard.is_pressed('esc'):
                                print("[INFO] Escape key pressed. Exiting...")
                                return
                            conn.settimeout(1.0)
                            try:
                                data = conn.recv(1024)
                                if not data:
                                    break
                                message = data.decode().strip()
                                print(f"[INFO] Received message: {message}")
                                take_picture(robot)
                                
                            except socket.timeout:
                                continue
                except socket.timeout:
                    continue


if __name__ == "__main__":
    main()
