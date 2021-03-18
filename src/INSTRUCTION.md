# Instruction

#### 1. Connect to the bebop via Wifi:

#### 2. Source the workspace:

bebop

Launch the ros-node to get the drone connection:

#### 1st terminal:

roslaunch bebop_driver bebop_node.launch

Launch rqt in a 2nd terminal to visualize the available nodes:

#### 2nd terminal:
rqt

Launch rviz in a 3rd terminal to visualize the video, tf, odom, ...:

#### 3rd terminal:
rviz

Record a new rosbag (manual/no flight):

#### 4th terminal:

cd rosbags

rosbag record -a

#### 3. Run the rosbag:

#### 1st terminal:

roscore

#### 2nd terminal:

rosbag play /rosbags/bebop_-double-tap

or

Run the rosbag in a loop:

rosbag play -l /rosbags/bebop_-double-tap

Run the ORB-SLAM-mono node

roslaunch ORBS


#### 4. Control bebop with the modified teleop_twist_keyboard:

#### 1st terminal:

roscore

#### 2nd terminal:

roslaunch bebop_driver bebop_node.launch

#### 3rd terminal:

rosrun bebop_teleop teleop_twist_keyboard.py

control the drone with the keyboard. 

Added additional commands:

press key 1: takeoff

press key 2: land

press key 3: take on-board-snapshot

#### 5. Extract images from a rosbag:

1. cd

2. mkdir rosbag_exports

3. rosrun image_view extract_images _sec_per_frame:=0.01 image:=bebop/image_raw

4. On the other terminal window, run rosbag play <BAGFILE>

5. A sequence of images will be created.

6. You can check if the number of frames created is the same as the number of messages in the .bag file using rosbag info command. If the number is less, decrease the _sec_per_frame value.


Note: The images have been named using this printf style pattern: frame%04d.jpg