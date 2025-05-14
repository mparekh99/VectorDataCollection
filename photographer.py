import os
import time
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
    '''Allows you to remote control vector with arrow keys and take pictures, used primarily to collect True Negatives for Dataset'''
    
    with anki_vector.Robot("VECTOR_SERIAL_#") as robot:
        # Set Vector Head
        robot.behavior.set_head_angle(degrees(7.0))
        robot.behavior.set_lift_height(0.0)
        print("[INFO] Vector is ready.")
        print("[INFO] Use arrow keys to control. Press SPACE to take a picture. Press ESC to quit.")

        try:
            while True:
                if keyboard.is_pressed("up"):
                    robot.motors.set_wheel_motors(100, 100)  # move forward
                elif keyboard.is_pressed("down"):
                    robot.motors.set_wheel_motors(-100, -100)  # move backward
                elif keyboard.is_pressed("left"):
                    robot.motors.set_wheel_motors(-50, 50)  # turn left
                elif keyboard.is_pressed("right"):
                    robot.motors.set_wheel_motors(50, -50)  # turn right
                else:
                    robot.motors.set_wheel_motors(0, 0)  # stop if no arrow key is pressed

                if keyboard.is_pressed("space"):
                    take_picture(robot)
                    time.sleep(0.5)  # slight delay to prevent multiple photos

                if keyboard.is_pressed("esc"):
                    print("[INFO] Exiting control loop.")
                    break

                time.sleep(0.1)

        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user.")


if __name__ == "__main__":
    main()
