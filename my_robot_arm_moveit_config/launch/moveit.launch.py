import os
from launch import LaunchDescription
from launch_ros.actions import Node
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    arm_share = get_package_share_directory('my_robot_arm')
    moveit_share = get_package_share_directory('my_robot_arm_moveit_config')

    ros2_controllers_yaml = os.path.join(moveit_share, "config", "ros2_controllers.yaml")
    moveit_controllers_yaml = os.path.join(moveit_share, "config", "moveit_controllers.yaml")

    moveit_config = (
        MoveItConfigsBuilder("my_robot_arm", package_name="my_robot_arm_moveit_config")
        .robot_description(
            file_path=os.path.join(arm_share, "urdf", "my_robot_arm.urdf.xacro")
        )
        .robot_description_semantic(
            file_path=os.path.join(moveit_share, "config", "my_robot_arm.srdf")
        )
        .robot_description_kinematics(
            file_path=os.path.join(moveit_share, "config", "kinematics.yaml")
        )
        .trajectory_execution(file_path=moveit_controllers_yaml)
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )

    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[moveit_config.robot_description]
    )

    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[moveit_config.robot_description, ros2_controllers_yaml],
        output='screen',
    )

    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen',
    )

    arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['arm_controller'],
        output='screen',
    )

    move_group_node = Node(
        package='moveit_ros_move_group',
        executable='move_group',
        output='screen',
        parameters=[moveit_config.to_dict()]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        parameters=[
            moveit_config.robot_description,
            moveit_config.robot_description_semantic,
            moveit_config.robot_description_kinematics,
            moveit_config.planning_pipelines,
        ]
    )

    return LaunchDescription([
        robot_state_publisher,
        controller_manager,
        joint_state_broadcaster_spawner,
        arm_controller_spawner,
        move_group_node,
        rviz_node,
    ])
