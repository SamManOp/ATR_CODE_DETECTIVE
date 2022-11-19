#!/usr/bin/env python3
import mediapipe_utils as mpu

import matplotlib.pyplot as plt
import matplotlib.animation as animation

from BlazeposeDepthaiEdge import BlazeposeDepthai
from BlazeposeRenderer import BlazeposeRenderer
import argparse

"""
    KEYPOINT_DICT = {
        "nose": 0,
        "left_eye_inner": 1,
        "left_eye": 2,
        "left_eye_outer": 3,
        "right_eye_inner": 4,
        "right_eye": 5,
        "right_eye_outer": 6,
        "left_ear": 7,
        "right_ear": 8,
        "mouth_left": 9,
        "mouth_right": 10,
        "left_shoulder": 11,
        "right_shoulder": 12,
        "left_elbow": 13,
        "right_elbow": 14,
        "left_wrist": 15,
        "right_wrist": 16,
        "left_pinky": 17,
        "right_pinky": 18,
        "left_index": 19,
        "right_index": 20,
        "left_thumb": 21,
        "right_thumb": 22,
        "left_hip": 23,
        "right_hip": 24,
        "left_knee": 25,
        "right_knee": 26,
        "left_ankle": 27,
        "right_ankle": 28,
        "left_heel": 29,
        "right_heel": 30,
        "left_foot_index": 31,
        "right_foot_index": 32
        }
"""

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--edge', action="store_true",
                    help="Use Edge mode (postprocessing runs on the device)")
    parser.add_argument("-m", "--model", type=str, choices=['full', 'lite', '831'], default='full',
                            help="Landmark model to use (default=%(default)s")
    parser.add_argument('-i', '--input', type=str, default='rgb',
                        help="'rgb' or 'rgb_laconic' or path to video/image file to use as input (default: %(default)s)")  
    parser.add_argument("-o","--output",
                        help="Path to output video file")

    parser_tracker = parser.add_argument_group("Tracker arguments")                 
    parser_tracker.add_argument('-xyz', '--xyz', action="store_true", 
                    help="Get (x,y,z) coords of reference body keypoint in camera coord system (only for compatible devices)")
    args = parser.parse_args()    
    
    pose = BlazeposeDepthai(input_src=args.input, 
            xyz=args.xyz,            
            internal_frame_height=640,
            stats=True)   

    renderer = BlazeposeRenderer(pose, output=args.output)


    x_len_max = 500
    y_rangelim = [-200, 200]

    figure = plt.figure()
    ax = figure.add_subplot(1, 1, 1)
    xs = list(range(0, 500))
    ys = [0] * x_len_max
    ax.set_ylim(y_rangelim)
    
    line, = ax.plot(xs, ys)

    body = None
    def animate(i, ys):

        # Add y to list
        if body:
            ypos = body.landmarks[mpu.KEYPOINT_DICT['right_wrist']][1]
            ys.append(ypos)

            if ypos <= y_rangelim[0]:
                y_rangelim[0] = ypos
                ax.set_ylim(y_rangelim)
            if ypos >= y_rangelim[1]:
                y_rangelim[1] = ypos
                ax.set_ylim(y_rangelim)


            # Limit y list to set number of items
            ys = ys[-x_len_max:]

            # Update line with new Y values
            line.set_ydata(ys)

        return line,
        

    ani = animation.FuncAnimation(figure,
        animate,
        fargs=(ys,),
        interval=50,
        blit=True)

    plt.ion()
    plt.show()

    while True:
        frame, body = pose.next_frame()
        if frame is None: break

        frame = renderer.draw(frame, body)
        key = renderer.waitKey(delay=1)
        

        if key == 27 or key == ord('q'):
            plt.ioff()
            plt.close()

            break

    renderer.exit()
    pose.exit()


if __name__ == "__main__":
    main()