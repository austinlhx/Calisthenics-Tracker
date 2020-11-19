import argparse
import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from ML.parse import parse_sequence, load_ps
from ML.evaluate import evaluate_pose

def run(video : str, exercise : str):
    if video:
        print('processing video file...')
        video = os.path.basename(video)
            
        output_path = os.path.join('..', os.path.splitext(video)[0])
        curr_dir = os.getcwd()
        print(curr_dir)
        assert os.path.exists(os.path.join('ML', 'openpose', 'bin', 'OpenPoseDemo.exe'))==True
           
        openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
        os.chdir('ML/openpose')
            
        subprocess.call([openpose_path, 
            '--video', os.path.join('..', 'videos', video), 
            '--write_json', output_path,
            '--model_pose', 'BODY_25',
            '--net_resolution', '-1x80',
            '--render_pose', '1',
            '--disable_multi_thread'
        ])

        parse_sequence(output_path, '..')
        pose_seq = load_ps(os.path.join('..', os.path.splitext(video)[0] + '.npy'))
        (correct, feedback) = evaluate_pose(pose_seq, exercise)

        os.chdir('../..')

        if correct:
            print('Exercise performed correctly!')
        else:
            print('Exercise could be improved:')
        return feedback
    else:
        print('No video file specified.')
        return

if __name__ == "__main__":
    run('', '')