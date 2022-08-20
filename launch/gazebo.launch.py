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
    pkg_share = FindPackageShare(package='cad_assembly_amr').find('cad_assembly_amr')
    world_file_name = 'empty_world/smalltown.world'
    world_path = os.path.join(pkg_share, 'worlds', world_file_name)

    world = LaunchConfiguration('world')

    return LaunchDescription([
        DeclareLaunchArgument(
            name='world',
            default_value=world_path,
            description='Full path to the world model file to load'
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('gazebo_ros'),
                    'launch',
                    'gzserver.launch.py'
                ])
            ]),
            launch_arguments={'world' : world}.items()
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('gazebo_ros'),
                    'launch',
                    'gzclient.launch.py'
                ])
            ])
        ),
        # Node(
        #     name="tf_footprint_base",
        #     package="tf2_ros",
        #     executable="static_transform_publisher 0 0 0 0 0 0 world base",

        # ),
        ExecuteProcess(
        cmd=[[
            FindExecutable(name='ros2'),
            ' run tf2_ros static_transform_publisher',
            ' 0 0 0 0 0 0 base_link, base_footprint'
        ]],
        shell=True
    )

    ])