"""Render the approved laser view using v37 and the local Fusion save.

The beam visibility flag is needed for native beam geometry. The frame
decoder uses the separate normal palette at $FF296C, not the visor palette.
"""
import runpy
from pathlib import Path

DEFAULT_SAVE = Path('upload/Cyber-Cop_v36a.gs9')

def laser_frame(save=DEFAULT_SAVE):
    p = runpy.run_path('v36/probe_saves04.py')
    assert p['R'][0xf9f85:0xf9f88] == b'v37'
    image, u = p['render_save'](save, 0x38a)
    assert p['rd'](u, 0xffff2298) == 1  # native beam visibility; no red palette in the preview
    return image
