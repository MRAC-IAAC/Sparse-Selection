# Sparse-Selection
S.2 SOTWARE II SEMINAR MRAC 2020/21
---
The Project SPARSE SELECTION aims to create a process pipeline to optimize the creation of point-clouds with the more accessible use of photogrammetry. The intention is to be able to capture data of areas with limited access, which is even a difficult task for grounded 3D-Scanners. With the use of UAVs, we are proposing a way for capturing data effortlessly and for the goal to use the scans beyond surveying.

#### 1. Overview

Digitization and new technologies give us the opportunity to bring back some architectural qualities, which are seen as not affordable if done by human labor alone. To rediscover form, pattern, and complex topologies in architecture and heritage, we propose the use of photogrammetry beyond surveying to create a library as a first step of the development of thinkable and unthinkable combinations and maybe a novel architectural language. The digitization of the construction sector is not only about reducing costs, it is the chance to rediscover “lost craftsmanship“.

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/210310_software-ii_final.jpg?raw=true)

Image: Process Pipeline

#### 2. Drone Controller

The autonomous flight is achieved with a set of open-source software libraries and tools within the ROS framework. The following repositories were investigated during this project:

#### 3. ROS-Repositories

Different repositories for autonomus flight with ROS. It consider Ubuntu 18.4 and ROS Melodic.

1. ROS driver for Parrot Bebop drone (quadrocopter):

git clone https://github.com/AutonomyLab/bebop_autonomy.git

2. ROS implementation of the ORB-SLAM2 real-time SLAM library for Monocular […] cameras:

git clone https://github.com/appliedAI-Initiative/orb_slam_2_ros

3. Autonomous navigation Bebop-Controller by Way-Points:

git clone https://github.com/MRAC-IAAC/bebop_control

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/orb_slam_730p.gif?raw=true)

Gif: Orb Slam test

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/autonomous_flight_730p.gif?raw=true)

Gif: Autonomus Flight Test

#### 4. Image Capturing [file.py](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/src/Python/video_extract.py)

The idea is to check the image overlap of each frame that is captured from the drone’s onboard camera and check each of those with the following for the perfect overlap to have only the necessary amount of data for the final point-cloud which will be generated in a post-process.

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/image_processing.jpg?raw=true)

Image: Image processing

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/final_process_pipeline.jpg?raw=true)

Image: Final Process Pipeline

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/opencv_image-selection.gif?raw=true)

Gif: Image Selection

#### 5. Post-Process: Image Selection [file.py](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/src/Python/multi_images_overlap.py)

Data storage becomes more and more excessive. To keep the data for the point cloud creation as low as possible, our script tries to isolate only the necessary and high-quality images instead of an unregulated amount of data.

For point cloud creation it is recommended to have at least 60 – 70% image overlap.

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/video-gif-small.gif?raw=true)

#### 6. Point-Cloud Creation

Finally, the extracted images can be used to finally generate the point cloud. By extracting only the necessary images, the process of point-cloud creation can be more efficient due to the fact of not using a vast amount of images which maybe cannot be calculated, or eventually, increase the time to calculate.

![Process Pipeline](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/docs/point_cloud_creation.gif?raw=true)

Gif: Spare Point Cloud - Dense Point Cloud - Mesh Point Cloud

#### 7. Instruction

For the instruction to drone Parrot Bebop 2 autonomus flight, please read this [text](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/src/INSTRUCTION.md).  

#### 8. Folders src & docs

In these folders, you will find several scripts and Grasshopper file to create the Flight path and Point cloud generation and Teleop Keyboard [file.py](https://github.com/MRAC-IAAC/Sparse-Selection/blob/main/src/Python/teleop_twist_keyboard.py) for Drone Parrot Bebop 2 

#### 9. Credits
Sparse-Selection // Software II is a project of IAAC, Institute for Advanced Architecture of Catalonia developed at the Master in Robotics and Advanced Construction in 2020/2021 by:

Students: Hendrik Benz, Alberto Browne, Michael DiCarlo // Faculty: Carlos Rizzo // Faculty Assistant: Soroush Garivani //