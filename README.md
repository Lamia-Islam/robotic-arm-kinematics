# Robotic Arm Kinematics & Path Planning

A simulated 6-DOF robotic arm built with ROS 2 (Humble), MoveIt2, and ros2_control — featuring Inverse Kinematics, collision-aware motion planning, and trajectory execution.

This project was built as Project 1 of the DecodeLabs Industrial Training Kit, focused on translating 3D Cartesian coordinates into precise, collision-free physical arm movement through kinematic logic.

## Features

- 6-DOF robotic arm modeled in URDF/Xacro with full collision geometry
- Inverse Kinematics via MoveIt2's OMPL planning pipeline (RRTConnect)
- Collision-aware trajectory planning using the Flexible Collision Library (FCL)
- Real controller execution via ros2_control + joint_trajectory_controller
- Interactive control in RViz — drag a target marker, plan, and execute
- Programmatic control via a custom Python action client (move_to_pose.py)

## Packages

- **my_robot_arm** — URDF/Xacro robot description and basic display launch file
- **my_robot_arm_moveit_config** — MoveIt2 configuration: SRDF, kinematics, OMPL planning pipeline, controllers, and main launch file
- **my_robot_arm_control** — Python script for sending programmatic target poses

## Usage

Launch the full simulation:
