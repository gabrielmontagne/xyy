import numpy as np
import bpy

def label(pixels, text, pos=(10, 25), colour=(255, 255, 255)):
    import cv2
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(pixels, text, pos, FONT, 1, colour, 1, cv2.LINE_8)

def split_topbottom(orig):
    return np.split(orig, 2)

def join_topbottom(a, b):
    return np.concatenate((a, b))

def prop(name, frame_number, default):
    world = bpy.context.scene.world

    fcurve = None
    if world.animation_data:
        fcurve = world.animation_data.action.fcurves.find('["{}"]'.format(name))

    if fcurve:
        result = fcurve.evaluate(frame_number)
    else:
        result = world.get(name, default)

    return result

def process_frame(orig, frame_number, process_name, is_topbottom=False):
    if is_topbottom:
        a, b = split_topbottom(orig)

        a.sort(axis=0)
        b.sort(axis=0)

        label(a, 'a:{}'.format(frame_number))
        label(b, 'x:{}'.format(frame_number))

        return join_topbottom(a, b)

    orig.sort(axis=0)
    label(orig, 'x:{}'.format(frame_number))
    return orig



def algo():
    print('algo xnix')