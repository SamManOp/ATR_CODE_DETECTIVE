# Forked Blazepose with DepthAI and Real-Time Landmark Position Graph

**Run the following to use BlazeposeDepthaiEdge model with real time pose landmark positional data presented on a matplotlib graph.**

```
python3 landmark_pos_demo.py -e
```
This requires DepthAI hardware, i.e., OAK-D, OAK-1, etc...

Currently a work in progress and defaulted to right_wrist landmark y position (vertical)

To change the landmark being tracked use the -l or --landmark flag followed by the landmark:

```
python3 landmark_pos_demo.py -e -l left_wrist
```

Available landmarks:

```
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
```

**See [depthai_blazepose](https://github.com/geaxgx/depthai_blazepose) for original README instructions.**


## Install


Install the python packages (depthai, opencv, open3d) with the following command:

```
python3 -m pip install -r requirements.txt
```

## Run Original Blazepose with DepthAI

**Usage:**

```
-> python3 demo.py -h
usage: demo.py [-h] [-e] [-i INPUT] [--pd_m PD_M] [--lm_m LM_M] [-xyz] [-c]
               [--no_smoothing] [-f INTERNAL_FPS]
               [--internal_frame_height INTERNAL_FRAME_HEIGHT] [-s] [-t]
               [--force_detection] [-3 {None,image,mixed,world}]
               [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -e, --edge            Use Edge mode (postprocessing runs on the device)

Tracker arguments:
  -i INPUT, --input INPUT
                        'rgb' or 'rgb_laconic' or path to video/image file to
                        use as input (default=rgb)
  --pd_m PD_M           Path to an .blob file for pose detection model
  --lm_m LM_M           Landmark model ('full' or 'lite' or 'heavy') or path
                        to an .blob file
  -xyz, --xyz           Get (x,y,z) coords of reference body keypoint in
                        camera coord system (only for compatible devices)
  -c, --crop            Center crop frames to a square shape before feeding
                        pose detection model
  --no_smoothing        Disable smoothing filter
  -f INTERNAL_FPS, --internal_fps INTERNAL_FPS
                        Fps of internal color camera. Too high value lower NN
                        fps (default= depends on the model)
  --internal_frame_height INTERNAL_FRAME_HEIGHT
                        Internal color camera frame height in pixels
                        (default=640)
  -s, --stats           Print some statistics at exit
  -t, --trace           Print some debug messages
  --force_detection     Force person detection on every frame (never use
                        landmarks from previous frame to determine ROI)

Renderer arguments:
  -3 {None,image,mixed,world}, --show_3d {None,image,mixed,world}
                        Display skeleton in 3d in a separate window. See
                        README for description.
  -o OUTPUT, --output OUTPUT
                        Path to output video file
```
**Examples :**

- To use default internal color camera as input with the model "full" in Host mode:

    ```python3 demo.py```

- To use default internal color camera as input with the model "full" in Edge mode [**preferred**]:

    ```python3 demo.py -e```

- To use a file (video or image) as input :

    ```python3 demo.py -i filename```

- To use the model "lite" :

    ```python3 demo.py -lm_m lite```

- To measure body spatial location in camera coordinate system (only for depth-capable device like OAK-D):
    ```python3 demo.py -e -xyz```

    The measure is made only on one reference point:
        - the middle of the hips if both hips are visible;
        - the middle of the shoulders if hips are not visible and both shoulders are visible.

- To show the skeleton in 3D 'world' mode (-xyz flag needed):

    ```python3 demo.py -e -xyz -3 world```

    <p align="center"> <img  src="img/3d_world_visualization.gif" alt="World mode"></p>

    Note that the floor and wall grids does not correspond to a real floor and wall. Each grid square size is 1m x 1m.

- When using the internal camera, to change its FPS to 15 : 

    ```python3 demo.py --internal_fps 15```

    Note: by default, the default internal camera FPS depends on the model, the mode (Edge vs Host), the use of depth ("-xyz"). These default values are based on my own observations. **Please, don't hesitate to play with this parameter to find the optimal value.** If you observe that your FPS is well below the default value, you should lower the FPS with this option until the set FPS is just above the observed FPS.

- When using the internal camera, you probably don't need to work with the full resolution. You can set a lower resolution (and win a bit of FPS) by using this option: 

    ```python3 demo.py --internal_frame_size 450```

    Note: currently, depthai supports only some possible values for this argument. The value you specify will be replaced by the closest possible value (here 432 instead of 450).

- By default, temporal filters smooth the landmark positions. Use *--no_smoothing* to disable the filter.

|Keypress in OpenCV window|Function|
|-|-|
|*Esc*|Exit|
|*space*|Pause|
|r|Show/hide the bounding rotated rectangle around the body|
|l|Show/hide landmarks|
|s|Show/hide landmark score|
|f|Show/hide FPS|
|x|Show/hide (x,y,z) coordinates (only on depth-capable devices and if using "-xyz" flag)|
|z|Show/hide the square zone used to measure depth (only on depth-capable devices and if using "-xyz" flag)|

If using a 3D visualization mode ("-3" or "--show_3d"):
|Keypress in Open3d window|Function|
|-|-|
|o|Oscillating (rotating back and forth) of the view|
|r|Continuous rotating of the view|
|s|Stop oscillating or rotating|
|*Up*|Increasing rotating or oscillating speed|
|*Down*|Decreasing rotating or oscillating speed|
|*Right* or *Left*|Change the point of view to a predefined position|
|*Mouse*|Freely change the point of view|
