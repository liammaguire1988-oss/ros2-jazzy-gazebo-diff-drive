import os
 
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
 
 
def generate_launch_description():
    pkg_share = get_package_share_directory('rtj_diffbot')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')
 
    xacro_file = os.path.join(pkg_share, 'urdf', 'diffbot.urdf.xacro')
    world_file = os.path.join(pkg_share, 'worlds', 'rtj_world.sdf')
    bridge_file = os.path.join(pkg_share, 'config', 'bridge.yaml')
 
    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str)
 
    # Start Gazebo Sim with our world, running immediately (-r)
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')),
        launch_arguments={
            'gz_args': f'-r -s {world_file}',
            'on_exit_shutdown': 'true',
        }.items())
 
    # Publishes the robot_description topic and TF for every non-moving link
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True,
        }],
        output='screen')
 
    # Spawns the robot into the running simulation from /robot_description
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'diffbot',
                   '-z', '0.15'],
        output='screen')
 
    # Bridges Gazebo topics to ROS 2 topics using the YAML file
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_file}],
        output='screen')
 
    return LaunchDescription([
        gz_sim,
        robot_state_publisher,
        spawn_robot,
        bridge,
    ])