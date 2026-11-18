# ROS 2 Jazzy + Gazebo Harmonic Differential Drive

Verified example package for the RoboTechJournal differential-drive tutorials.

## Tested scope
Recorded headless simulation checks used Ubuntu 24.04.5, ROS 2 Jazzy and Gazebo Harmonic 8.15.0. No physical hardware or Gazebo GUI test is claimed.

## Build

```bash
source /opt/ros/jazzy/setup.bash
cd ~/rtj_ws
rosdep install --from-paths src --ignore-src --rosdistro jazzy -r -y
colcon build --packages-select rtj_diffbot
source install/setup.bash
```

Run `ros2 launch rtj_diffbot sim.launch.py` or `ros2 launch rtj_diffbot sim_control.launch.py`.

## Notes
Choose an appropriate licence and replace the placeholder maintainer before distributing a derivative. See the associated RoboTechJournal articles for context and primary-source links.
