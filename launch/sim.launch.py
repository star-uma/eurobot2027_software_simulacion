import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, AppendEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_name = 'eurobot2027_software_simulacion'
    pkg_share = get_package_share_directory(pkg_name)

    # Inyecta la carpeta worlds en el path de recursos de Gazebo
    env_ign = AppendEnvironmentVariable('IGN_GAZEBO_RESOURCE_PATH', os.path.join(pkg_share, 'worlds'))
    env_gz = AppendEnvironmentVariable('GZ_SIM_RESOURCE_PATH', os.path.join(pkg_share, 'worlds'))

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
        arguments=[
            '-topic', 'robot_description',
            '-name', 'eurobot_2027',
            '-x', '0.1',   # Nuevo lateral izquierdo positivo
            '-y', '1.0',   # Nuevo centro vertical positivo
            '-z', '0.1', 
            '-Y', '0.0'
        ],
        output='screen'
    )


    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/cmd_vel@geometry_msgs/msg/Twist]ignition.msgs.Twist'],
        output='screen'
    )


    return LaunchDescription([env_ign, env_gz, rsp, gazebo, spawn_entity, bridge])
