# Calisthenics-Tracker

The goal of this project is to create an application which provides custom feedback for user posture during excercises, by using key pose estimation. This application leverages openpose for keypose estimation based on a pretrained CNN model and uses the guidelines in PoseTrainer (https://www.researchgate.net/publication/324759769_Pose_Trainer_Correcting_Exercise_Posture_using_Pose_Estimation) to design the feedback for users. Our front-end is built under ```/public``` and allows users to stream/upload videos of their workouts, which is then processed by our Flac server for serving the results of the ML.

## Setup & Installation

### Flask Server
1. Navigate to the ```/API``` folder on the terminal

2. [Create and activate Python virtual environment](https://docs.python.org/3/library/venv.html)

3. [Install OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)  

4. Download either the MPI or Body_25 models, under OpenPose by running ``get_models.bat```

5. Install pip requirements using the following command ```pip install -r requirements.txt```

6. Run flask server using the following command ```python run main.py```

7. Adjust the network resolution to balance accuracy with speed with ``--net_resolution```

### Front-End (HTML, CSS, JavaScript)

1. Navigate to the ```/Public``` folder on the terminal

2. Install node modules using the following command ```npm install```
