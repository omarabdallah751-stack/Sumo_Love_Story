# Sumo Robot URDF Description

## Project Overview

This repository contains the structural description files (**URDF/XACRO**) for a Sumo Robot operating in a **ROS 2** environment. The project follows a modular architecture, where the robot is divided into multiple Xacro files representing the chassis, drivetrain, wheels, sensors, and attack mechanism. This structure improves readability, maintainability, and reusability while simplifying future modifications.

---

## Team Members

|Name|
|---|
|Mohamed Khairy|
|Yousef Aamer|
|Omar Abdallah Ramadan|
|Rodaina Sabry|
|Mai Ahmed|
|Mohamed Elmansy|
|Eman|

---
## Mechanical Design Summary

The robot features a rigid **octagonal chassis** constructed from a **20 × 20 mm T-slot aluminum frame**, reinforced with **steel panels** to provide high structural strength, durability, and impact resistance during Sumo competitions.

Its combat system combines both offensive and defensive mechanisms. A **front servo-actuated blade** delivers rapid attacking motions, while **two fixed side attack blades** increase the likelihood of making contact with opponents from multiple directions. For additional protection, a **rear electric defense module** helps shield the robot from attacks approaching from behind.

To enhance situational awareness, the robot incorporates a protected **four-camera vision system** that provides near **360° environmental coverage**, supporting future computer vision and autonomous targeting algorithms.

Mobility is achieved using a **four-wheel Mecanum drive** with rollers mounted at **45°**, allowing the robot to move omnidirectionally. This configuration enables precise lateral, diagonal, rotational, and forward/backward motion, providing excellent maneuverability and positioning during combat.

---
## Robot Architecture

### Chassis

The main body of the robot is represented by **`frame_link`**, which serves as the parent link for all mechanical and sensor components.

- **Mass:** **8.56573 kg**
    
- Houses all major subsystems including motors, cameras, Lidar, and the attack mechanism.
    

### Chassis Design

---

## Sensors

### Lidar

A Lidar sensor is mounted on the upper section of the chassis using a fixed joint.

It provides environmental scanning for obstacle detection, localization, and future autonomous navigation.

---

### Vision System

The robot includes **four cameras**:

- `camera_link`
    
- `camera1_link`
    
- `camera2_link`
    
- `camera3_link`
    

Each camera is attached to the chassis using fixed joints and positioned at different offsets around the frame.

This configuration provides wide-angle coverage around the robot and is intended to support future computer vision algorithms.

---

## Drivetrain

The robot uses a **four-wheel independent drive system**.

Each side consists of:

```
Frame
   │
Motor
   │
Coupler
   │
Wheel
```

### Features

- Four independent drive motors
    
- Mechanical couplers for power transmission
    
- Four continuously rotating wheels
    
- Continuous joints allowing forward and reverse motion
    

---

## Wheels

Each wheel has the following properties:

- **Mass:** **123.31 g**
    
- Connected through a continuous joint
    
- Independently driven
    

### Wheel Design

---

# Attack / Defense Mechanism

The robot's primary offensive mechanism is a **servo-driven striking axe**.

### Features

- Axe Mass: **148.77 g**
    
- Controlled by a dedicated servo
    
- Servo represented by `servo_link`
    
- Axe represented by `axe_link`
    
- Connected using a **revolute joint**
    
- Rotates about the **X-axis**
    
- Motion constrained by joint limits
    

### Axe Design
<img width="1387" height="805" alt="Screenshot 2026-07-25 204823" src="https://github.com/user-attachments/assets/11d6e354-dcdb-419d-8d08-c004109da918" />


### Complete Assembly
<img width="722" height="621" alt="image" src="https://github.com/user-attachments/assets/8e7e2653-cf71-439b-89d2-7722c40f33ac" />

---

# Future Autonomous Combat

The hardware has been designed to support future autonomous combat algorithms.

The four-camera vision system can provide nearly **360° environmental coverage**, allowing computer vision models (such as **YOLO** or custom **OpenCV** pipelines) to detect and track opponent robots.

A future control node can:

1. Detect the opponent.
    
2. Estimate its position and distance.
    
3. Verify that it is within the optimal striking range.
    
4. Publish commands to the `axe_joint`.
    
5. Trigger the servo automatically for a precisely timed attack.
    

This modular architecture allows perception and motion planning to be integrated without modifying the robot's mechanical description.

---

# Software Requirements

Install the following ROS 2 packages before running the project:

- ROS 2 (Humble, Iron, or Jazzy)
    
- `xacro`
    
- `robot_state_publisher`
    
- `joint_state_publisher_gui`
    
- `rviz2`
    

---

# Project Structure

```text
sumo_description/
├── launch/
├── meshes/
├── rviz/
├── urdf/
│   ├── main.xacro
│   ├── frame.xacro
│   ├── motors.xacro
│   ├── wheels.xacro
│   ├── cameras.xacro
│   ├── lidar.xacro
│   └── axe.xacro
└── package.xml
```

---

# Build

```bash
cd ~/ROS/Project

colcon build --packages-select sumo_description

source install/setup.bash
```

---

# Launch

Launch the robot visualization using:

```bash
ros2 launch sumo_description <your_launch_file>.launch.py
```

The launch file automatically:

- Loads the URDF/Xacro model
    
- Starts `robot_state_publisher`
    
- Starts `joint_state_publisher_gui`
    
- Opens RViz with the robot model
    

---

# TF Tree

```
frame_link
├── lidar_link
├── camera_link
├── camera1_link
├── camera2_link
├── camera3_link
├── motor_FL
│   └── coupler_FL
│       └── wheel_FL
├── motor_FR
│   └── coupler_FR
│       └── wheel_FR
├── motor_RL
│   └── coupler_RL
│       └── wheel_RL
├── motor_RR
│   └── coupler_RR
│       └── wheel_RR
└── servo_link
    └── axe_link
```

---

# Visualization

The robot can be visualized in **RViz2**, where you can:

- Inspect the complete TF tree
    
- Test wheel rotation
    
- Control the axe joint
    
- Verify camera and Lidar placement
    
- Validate the robot geometry before simulation

<img width="3408" height="2130" alt="Screenshot from 2026-07-27 10-19-57" src="https://github.com/user-attachments/assets/cdaa65ae-5c57-488e-a8e0-9c8e3d2bec8d" />
<img width="2948" height="1574" alt="image" src="https://github.com/user-attachments/assets/da1773e8-1b15-4e33-9b0b-342dd9a5def0" />

    
