#!/usr/bin/env python3

import cv2

from depthai_sdk import OakCamera, TextPosition
from depthai_sdk.callback_context import VisualizeContext


def callback(ctx: VisualizeContext):
    packet = ctx.packet
    visualizer = ctx.visualizer

    num = len(packet.img_detections.detections)
    print('New msgs! Number of people detected:', num)

    visualizer.add_text(f"Number of people: {num}", position=TextPosition.TOP_MID)
    visualizer.draw(packet.frame)
    cv2.imshow(f'frame {packet.name}', packet.frame)


with OakCamera(replay='people-images-01') as oak:
    color = oak.create_camera('color')
    nn = oak.create_nn('person-detection-retail-0013', color)
    oak.replay.setFps(3)

    oak.visualize(nn, callback=callback)
    # oak.show_graph()
    oak.start(blocking=True)
