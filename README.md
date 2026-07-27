# Sumo Robot URDF Description

This repository contains the structural description files (URDF/XACRO) for a Sumo Robot. The project is designed using a **Modular Architecture** (split across multiple files) to ensure clean code, easy maintenance, and component reusability.

---

## File Structure (Modular Design)

The robot's body and components are divided into 4 primary modules, which are seamlessly integrated into the top-level main file:

* **`sumo_robot.xacro` (Main File)**: The top-level file that brings the entire robot together. It contains all the dynamic math constants, origin coordinates, and offsets. It establishes the `base_footprint_link`, connects it to the main chassis, and includes all the sub-modules.
* **`base_components.xacro`**: Defines the `frame_link` (the core physical body of the robot). It also houses the sensors and components attached directly to the chassis, such as the Lidar, Servo motor, Axe (weapon), and 4 peripheral cameras.
* **`motors_couplers.xacro`**: Dedicated to defining the 4 drive motors attached to the frame, as well as the mechanical couplers that transmit motion from the motors to the wheels.
* **`wheels.xacro`**: Contains the physical and visual properties of the 4 wheels. Each wheel is dynamically jointed to its corresponding coupler.

---

## Kinematic Chain (New TF Tree)

The coordinate frame tree (TF Tree) has been optimized to streamline the robot's movement in the ROS environment. The redundant, dummy `base_link` has been entirely removed. The `frame_link` now acts as the primary physical center of the robot, directly connected to the ground projection (`base_footprint_link`).

Here is the hierarchical Parent-to-Child joint relationships:

```text
base_footprint_link (Root)
 └── frame_link (Main Chassis)
      ├── lidar_link (Fixed)
      ├── servo_link (Fixed)
      │    └── axe_link (Revolute)
      ├── camera_link (Fixed)
      ├── camera1_link (Fixed)
      ├── camera2_link (Fixed)
      ├── camera3_link (Fixed)
      ├── motor_link (Fixed)
      │    └── coupler_link (Fixed)
      │         └── wheel_link (Continuous)
      ├── motor1_link (Fixed)
      │    └── coupler1_link (Fixed)
      │         └── wheel1_link (Continuous)
      ├── motor2_link (Fixed)
      │    └── coupler2_link (Fixed)
      │         └── wheel2_link (Continuous)
      └── motor3_link (Fixed)
           └── coupler3_link (Fixed)
                └── wheel3_link (Continuous)
