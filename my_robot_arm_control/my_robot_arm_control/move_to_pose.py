#!/usr/bin/env python3
import argparse
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from moveit_msgs.action import MoveGroup
from moveit_msgs.msg import MotionPlanRequest, Constraints, PositionConstraint, OrientationConstraint, WorkspaceParameters
from geometry_msgs.msg import PoseStamped
from shape_msgs.msg import SolidPrimitive


class MoveToPose(Node):
    def __init__(self, x, y, z):
        super().__init__('move_to_pose_client')
        self.x = x
        self.y = y
        self.z = z
        self._client = ActionClient(self, MoveGroup, 'move_action')

    def send_goal(self):
        self.get_logger().info('Waiting for move_action server...')
        self._client.wait_for_server()

        goal_msg = MoveGroup.Goal()
        req = MotionPlanRequest()
        req.group_name = 'arm'
        req.num_planning_attempts = 10
        req.allowed_planning_time = 5.0
        req.max_velocity_scaling_factor = 0.5
        req.max_acceleration_scaling_factor = 0.5

        ws = WorkspaceParameters()
        ws.header.frame_id = 'base_link'
        ws.min_corner.x = -1.0
        ws.min_corner.y = -1.0
        ws.min_corner.z = -1.0
        ws.max_corner.x = 1.0
        ws.max_corner.y = 1.0
        ws.max_corner.z = 1.0
        req.workspace_parameters = ws

        pos_constraint = PositionConstraint()
        pos_constraint.header.frame_id = 'base_link'
        pos_constraint.link_name = 'end_effector'

        primitive = SolidPrimitive()
        primitive.type = SolidPrimitive.SPHERE
        primitive.dimensions = [0.01]

        target_pose = PoseStamped()
        target_pose.header.frame_id = 'base_link'
        target_pose.pose.position.x = self.x
        target_pose.pose.position.y = self.y
        target_pose.pose.position.z = self.z
        target_pose.pose.orientation.w = 1.0

        pos_constraint.constraint_region.primitives.append(primitive)
        pos_constraint.constraint_region.primitive_poses.append(target_pose.pose)
        pos_constraint.weight = 1.0

        orient_constraint = OrientationConstraint()
        orient_constraint.header.frame_id = 'base_link'
        orient_constraint.link_name = 'end_effector'
        orient_constraint.orientation.w = 1.0
        orient_constraint.absolute_x_axis_tolerance = 3.14
        orient_constraint.absolute_y_axis_tolerance = 3.14
        orient_constraint.absolute_z_axis_tolerance = 3.14
        orient_constraint.weight = 1.0

        constraints = Constraints()
        constraints.position_constraints.append(pos_constraint)
        constraints.orientation_constraints.append(orient_constraint)
        req.goal_constraints.append(constraints)

        goal_msg.request = req
        goal_msg.planning_options.plan_only = False

        self.get_logger().info(f'Sending goal: x={self.x}, y={self.y}, z={self.z}')
        future = self._client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return
        self.get_logger().info('Goal accepted, executing...')
        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(f'Result error_code: {result.error_code.val}')
        rclpy.shutdown()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--x', type=float, required=True)
    parser.add_argument('--y', type=float, required=True)
    parser.add_argument('--z', type=float, required=True)
    args, _ = parser.parse_known_args()

    rclpy.init()
    node = MoveToPose(args.x, args.y, args.z)
    node.send_goal()
    rclpy.spin(node)


if __name__ == '__main__':
    main()