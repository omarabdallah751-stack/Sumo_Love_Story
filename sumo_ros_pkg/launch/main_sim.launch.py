import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    # 1. Paths
    pkg_path = get_package_share_directory('sumo_ros_pkg')
    xacro_file = os.path.join(pkg_path, 'urdf', 'main_sumo.urdf.xacro')
    bridge_config = os.path.join(pkg_path, 'config', 'gz_bridge.yaml')
    
    # Process Xacro
    robot_description_config = xacro.process_file(xacro_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    # 2. Nodes
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    # Bridge Node
    node_ros_gz_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{'config_file': bridge_config}],
        output='screen'
    )

    # 3. Include Gazebo Launch (Placeholder for now)
    # Will add ros_gz_sim launch inclusion here later when world is ready

    return LaunchDescription([
        node_robot_state_publisher,
        node_ros_gz_bridge,
    ])