# Eurobot 2027 - Software de Simulación

```text
Ejecutar comandos en eurobot2027_ws, dos carpetas anteriores.
```
## Instalación gazebo ignition

1. Configurar paquetes de los repositorios.

```bash
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -

sudo apt-get update
```

2. Instalar Gazebo Ignition
```bash
sudo apt-get install libignition-gazebo<#>-dev
```
## Instalación de dependencias 

```bash
sudo rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
```
## Compilación del paquete simulación
```bash
colcon build --packages-select eurobot2027_software_simulacion --symlink-install
```
## Referencia a los archivos
```bash
source install/setup.bash
```

## Lanzamiento gazebo (terminal 1)
```bash
ros2 launch eurobot2027_software_simulacion sim.launch.py
```
## Control teleop (terminal 2)
```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```