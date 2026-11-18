import os
 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
 
 
def generate_launch_description():
    pkg_share = get_package_share_directory('rtj_diffbot')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
 
    xacro_file = os.path.join(pkg_share, 'urdf', 'diffbot_control.urdf.xacro')
    world_file = os.path.join(pkg_share, 'worlds', 'rtj_world.sdf')
    bridge_file = os.path.join(pkg_share, 'config', 'bridge_control.yaml')
 
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str)
 
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': f'-r -s {world_file}',
            'on_exit_shutdown': 'true',
        }.items())
 
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }],
        output='screen')
 
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'diffbot',
                   '-z', '0.15'],
        output='screen')
 
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_file}],
        output='screen')
 
    joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen')
 
    diff_drive_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller'],
        output='screen')
 
    # Start controllers in order, each after the previous process exits
    start_jsb = RegisterEventHandler(
        OnProcessExit(target_action=spawn_robot,
                      on_exit=[joint_state_broadcaster]))
    start_ddc = RegisterEventHandler(
        OnProcessExit(target_action=joint_state_broadcaster,
                      on_exit=[diff_drive_controller]))
 
    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        bridge,
        start_jsb,
        start_ddc,
    ])