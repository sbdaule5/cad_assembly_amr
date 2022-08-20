import os
from sys import executable
# from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration, TextSubstitution, FindExecutable
from launch_ros.actions import Node


from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    slam_params_file = LaunchConfiguration("slam_params_file")
    use_sim_time = LaunchConfiguration("use_sim_time")

    use_sim_time_argument = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="use gazebo simulation time")
    slam_params_file_argument = DeclareLaunchArgument(
        name="slam_params_file",
        default_value=os.path.join(FindPackageShare(package='slam_toolbox').find('slam_toolbox'), "config", "mapper_params_online_async.yaml")
    )
    print(os.path.join(FindPackageShare(package='slam_toolbox').find('slam_toolbox'), "config", "mapper_params_online_async.yaml"))
    
    async_slam_toolbox_node = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        parameters=[
            slam_params_file,
            {"use_sim_time" : use_sim_time}
        ],
        output="screen"
    )
    return LaunchDescription([
        use_sim_time_argument,
        slam_params_file_argument,
        async_slam_toolbox_node
    ])