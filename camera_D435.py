import pyrealsense2 as rs
from copy import copy

pipeline = rs.pipeline()
profile = pipeline.start()
align = rs.align(rs.stream.color)

all_color_frames = []
all_depth_frames = []

for i in range(20):
    print(i)
    frames = pipeline.wait_for_frames()
    frames = align.process(frames)
    depth = frames.get_depth_frame()
    color = frames.get_color_frame()
    all_depth_frames.append(copy(depth))
    # all_color_frames.append(color)
