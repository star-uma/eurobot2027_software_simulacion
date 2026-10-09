import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'eurobot2027_software_simulacion'
    pkg_share = get_package_share_directory(pkg_name)

    # 1. Lanza tu robot_state_publisher forzando el tiempo de simulación a true
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(pkg_share, 'launch', 'rsp.launch.py')]),
        launch_arguments={'use_sim_time': 'true'}.items()
    )

    # 2. Lanza Gazebo cargando el archivo SDF de la mesa
    world_file = os.path.join(pkg_share, 'worlds', 'eurobot2027.sdf')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ]),
        launch_arguments={'gz_args': ['-r ', world_file]}.items()
    )

    # 3. Nodo que coge la descripción del robot y lo "spawnea" en Gazebo
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description',
                   '-name', 'eurobot_2027',
                   '-z', '0.1'], # Lo dejamos caer desde 10 cm para que asiente en el suelo
        output='screen'
    )

    return LaunchDescription([rsp, gazebo, spawn_entity])