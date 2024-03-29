from argparse import ArgumentParser
from flask import Flask, request, Response
from imageio import read, imwrite
from os.path import join
import numpy as np

app = Flask(__name__)


def split_topbottom(orig):
    return np.split(orig, 2)


def join_topbottom(a, b):
    return np.concatenate((a, b))


def process_frame(func):
    @app.route('/process', methods=['POST'])
    def wrapper():
        config = request.json

        bitmap = list(read(config.get('image_path'))).pop()

        if config.get('use_multiview'):
            top, bottom = split_topbottom(bitmap)
            top_frame = func(top, request.json)
            bottom_frame = func(bottom, request.json)
            new_frame = join_topbottom(top_frame, bottom_frame)
        else:
            new_frame = func(bitmap, request.json)

        new_save_path = join(
            config.get('processed_dir'),
            f'{config.get("original_file_name")}.png'
        )

        imwrite(new_save_path, new_frame, 'PNG-FI')
        return Response(new_save_path, content_type='text/plain')

    return wrapper


def start_server():
    parser = ArgumentParser()
    parser.add_argument('--port', type=int, default=3000)
    args, _ = parser.parse_known_args()
    app.run(host='0.0.0.0', port=args.port, threaded=False)
    print('start XYY server', args.port)


def label(pixels, text, pos=(10, 25), colour=(255, 255, 255)):
    import cv2
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(pixels, text, pos, font, 1, colour, 1, cv2.LINE_8)


def prop(name, frame_number, default):
    import bpy
    world = bpy.context.scene.world

    fcurve = None
    if world.animation_data:
        fcurve = world.animation_data.action.fcurves.find(
            '["{}"]'.format(name))

    if fcurve:
        result = fcurve.evaluate(frame_number)
    else:
        result = world.get(name, default)

    return result
