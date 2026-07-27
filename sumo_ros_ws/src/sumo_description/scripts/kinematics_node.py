#!/usr/bin/env python3

import sys
import select
import termios
import tty
import math
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64

# Save the terminal's default settings
settings = termios.tcgetattr(sys.stdin)


def getKey():
    """Read keyboard input without requiring Enter."""
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)

    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


class KeyboardXDriveNode(Node):
    def __init__(self):
        super().__init__('keyboard_xdrive_node')

        # Create publishers for each wheel
        self.pub_fl = self.create_publisher(Float64, '/wheel_fl_cmd', 10)
        self.pub_fr = self.create_publisher(Float64, '/wheel_fr_cmd', 10)
        self.pub_bl = self.create_publisher(Float64, '/wheel_bl_cmd', 10)
        self.pub_br = self.create_publisher(Float64, '/wheel_br_cmd', 10)

        # Robot dimensions
        self.wheel_radius = 0.033
        self.wheel_separation_x = 0.181
        self.wheel_separation_y = 0.266

        self.geometry_factor = (
            self.wheel_separation_x / 2.0 +
            self.wheel_separation_y / 2.0
        )

        self.cos45 = math.cos(math.radians(45))

        # Default linear and angular speeds
        self.speed = 0.5
        self.turn = 1.0

        self.get_logger().info(
            "Keyboard controller started!\n"
            "Controls:\n"
            "  W : Forward\n"
            "  S : Backward\n"
            "  A : Left\n"
            "  D : Right\n"
            "  Q : Rotate CCW\n"
            "  R : Rotate CW\n"
            "  Space : Stop\n"
            "  Ctrl+C : Exit"
        )

    def publish_velocities(self, Vx, Vy, Wz):
        """Compute wheel velocities and publish them."""

        v_fl = (self.cos45 * (Vx - Vy) - Wz * self.geometry_factor) / self.wheel_radius
        v_fr = (self.cos45 * (Vx + Vy) + Wz * self.geometry_factor) / self.wheel_radius
        v_bl = (self.cos45 * (Vx + Vy) - Wz * self.geometry_factor) / self.wheel_radius
        v_br = (self.cos45 * (Vx - Vy) + Wz * self.geometry_factor) / self.wheel_radius

        msg_fl = Float64(); msg_fl.data = float(v_fl)
        msg_fr = Float64(); msg_fr.data = float(v_fr)
        msg_bl = Float64(); msg_bl.data = float(v_bl)
        msg_br = Float64(); msg_br.data = float(v_br)

        self.pub_fl.publish(msg_fl)
        self.pub_fr.publish(msg_fr)
        self.pub_bl.publish(msg_bl)
        self.pub_br.publish(msg_br)


def main(args=None):
    rclpy.init(args=args)
    node = KeyboardXDriveNode()

    # Current commanded velocities
    Vx = 0.0
    Vy = 0.0
    Wz = 0.0

    try:
        while rclpy.ok():
            key = getKey()

            if key == 'w':
                Vx = node.speed
                Vy = 0.0
                Wz = 0.0

            elif key == 's':
                Vx = -node.speed
                Vy = 0.0
                Wz = 0.0

            elif key == 'a':
                Vx = 0.0
                Vy = node.speed
                Wz = 0.0

            elif key == 'd':
                Vx = 0.0
                Vy = -node.speed
                Wz = 0.0

            elif key == 'q':
                Vx = 0.0
                Vy = 0.0
                Wz = node.turn

            elif key == 'r':
                Vx = 0.0
                Vy = 0.0
                Wz = -node.turn

            elif key == ' ':
                # Stop the robot
                Vx = 0.0
                Vy = 0.0
                Wz = 0.0

            elif key == '\x03':
                # Ctrl+C
                break

            # Publish whenever a valid control key is pressed
            if key in ['w', 's', 'a', 'd', 'q', 'r', ' ']:
                node.publish_velocities(Vx, Vy, Wz)

    except Exception as e:
        print(e)

    finally:
        # Ensure the robot stops before shutting down
        node.publish_velocities(0.0, 0.0, 0.0)

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()