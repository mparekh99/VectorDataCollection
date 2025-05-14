import anki_vector
from anki_vector.util import degrees, distance_mm, speed_mmps
import time
import random
import math
import matplotlib.pyplot as plt
import socket


def random_point_in_triangle(A, B, C):
    ''' Generates a random point inside the triangle ABC using barycentric coordinates.
    The function ensures uniform distribution by applying the square root to r1, 
    preventing clustering near the corners of the triangle.'''

    r1 = random.random()
    r2 = random.random()
    lambda_A = 1 - math.sqrt(r1)
    lambda_B = math.sqrt(r1) * (1 - r2)
    lambda_C = math.sqrt(r1) * r2
    Px = lambda_A * A[0] + lambda_B * B[0] + lambda_C * C[0]
    Py = lambda_A * A[1] + lambda_B * B[1] + lambda_C * C[1]
    return Px, Py


def navigate(rand_pt, actions, robot):
    deg = 0

    # X
    if rand_pt[0] != 0:
        if rand_pt[0] > 0:
            deg = -90
            
            robot.behavior.turn_in_place(degrees(deg))

        else:
            deg = 90

            robot.behavior.turn_in_place(degrees(deg))

        robot.behavior.drive_straight(distance_mm(abs(rand_pt[0])), speed_mmps(150))

        actions[0] = deg
        actions[1] = abs(rand_pt[0])

    # Y
    if rand_pt[1] != 0:
        robot.behavior.turn_in_place(degrees(-actions[0]))  # Reorient
        robot.behavior.drive_straight(distance_mm(rand_pt[1]), speed_mmps(150))
        actions[2] = -actions[0]
        actions[3] = rand_pt[1]
        # handle_ypos(rand_pt[1], actions, robot)


def send_to_other_script(data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 65432))
        s.sendall(str(data).encode())

def ret_nav(actions, robot):
    # Y
    robot.behavior.turn_in_place(degrees(180))  # Reorient
    robot.behavior.drive_straight(distance_mm(actions[3]), speed_mmps(150))
    # X 
    robot.behavior.turn_in_place(degrees(actions[0]))  # Reorient
    robot.behavior.drive_straight(distance_mm(actions[1]), speed_mmps(150))
    robot.behavior.turn_in_place(degrees(-actions[2]))


def rand_rotate(robot):

    # Perform a random rotation
    random_angle = random.uniform(-180, 180)
    robot.behavior.turn_in_place(degrees(random_angle))


    send_to_other_script("Reached Point!") # Connect to socket to signal the other vector to take the picture. 

    time.sleep(2)

    # Rotate back to original orientation
    robot.behavior.turn_in_place(degrees(-random_angle))

def main():
    A = (-11 * 25.4, 0)  ## converting inches to millimeters  
    B = (0, 11 * 25.4)
    C = (11 * 25.4, 0)

    with anki_vector.Robot("VECTOR_SERIAL_#") as robot:

        time.sleep(3)

        for _ in range(100):
            
            actions = [0, 0, 0, 0]  # Reset all actions 

            random_point = random_point_in_triangle(A, B, C) # Get random point
            print(f"Random point: {random_point}")

            navigate(random_point, actions, robot) # Go to random point from (0,0)

            rand_rotate(robot) # Do a random rotation


            time.sleep(1)

            ret_nav(actions, robot) # Retrace steps, return back to (0,0)


if __name__ == "__main__":
    main()
