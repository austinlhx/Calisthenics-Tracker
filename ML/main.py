import argparse
import os
import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt

from parse import parse_sequence, load_ps
from evaluate import evaluate_pose


def main():
    parser = argparse.ArgumentParser(description='Pose Trainer')
    parser.add_argument('--display', type=int, default=1, help='display openpose video')
    parser.add_argument('--input_folder', type=str, default='videos', help='input folder for videos')
    parser.add_argument('--output_folder', type=str, default='poses', help='output folder for pose JSON')
    parser.add_argument('--video', type=str, default="", help='input video filepath for evaluation')
    parser.add_argument('--file', type=str, help='input npy file for evaluation')
    parser.add_argument('--exercise', type=str, default='bicep_curl', help='exercise type to evaluate')

    args = parser.parse_args()
    print(args)
        if args.video:
            print('processing video file...')
            video = os.path.basename(args.video)
            
            output_path = os.path.join('..', os.path.splitext(video)[0])
            assert os.path.exists(os.path.join('openpose', 'bin', 'OpenPoseDemo.exe'))==True
           
            openpose_path = os.path.join('bin', 'OpenPoseDemo.exe')
            os.chdir('openpose') 
            
            '''
            subprocess.call([openpose_path, 
                            '--video', os.path.join('..', args.video), 
                            '--write_json', output_path,
                            '--model_pose', 'BODY_25',
                            '--net_resolution', '-1x80',
                            '--render_pose', '1',
                            '--disable_blending',
                            '--disable_multi_thread'
                            ])
            '''

            parse_sequence(output_path, '..')
            pose_seq = load_ps(os.path.join('..', os.path.splitext(video)[0] + '.npy'))
            (correct, feedback) = evaluate_pose(pose_seq, args.exercise)
            if correct:
                print('Exercise performed correctly!')
            else:
                print('Exercise could be improved:')
            print(feedback)
        else:
            print('No video file specified.')
            return

if __name__ == "__main__":
    main()