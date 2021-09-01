
"""

New Card feature to return instantly maipulated image

"""


import io
from typing import Tuple
from PIL import Image



class Card:

    def __init__(self, size:Tuple, color:hex = None):

        color = 0x36393f if color is None else color
        size = size if size is not None and len(size) == 2 else None

        card = Image.new("RGB", size, color = color)

        buff = io.BytesIO()
        card.save(buff, 'png')
        buff.seek(0)

        self.width = size[0]
        self.height = size[1]
        self.canvas = buff


    def set_background(self, _byte = None, _path:str = None):

        canvas = Image.open(self.canvas)
        size = canvas.size

        if _path is not None and _byte is None:
            bg = Image.open(_path)

        elif _byte is not None and _path is None:
            bg = Image.open(_byte)
        else:
            bg = None

        if bg is not None:
            _bg = bg.resize(size)

            buff = io.BytesIO()
            _bg.save(buff, 'png')
            buff.seek(0)

            self.canvas = buff
        else:
            raise Exception("Use either _path or _byte")



    def add_image(self, _path:str = None, _byte = None, resize:Tuple = None, crop:Tuple = None, position:Tuple = None):

        if _path is not None and _byte is None:
            img = Image.open(_path)

        elif _byte is not None and _path is None:
            img = Image.open(_byte)

        else:
            img = None


        if img is not None:

            if resize is not None and crop is None:

                if position is None:
                    offset = ((self.width - resize[0]) // 2, (self.height - resize[1]) // 2)
                else:
                    offset = (position[0], position[1])

                _img = img.resize(resize, resample=0)
                canvas = Image.open(self.canvas)
                Image.Image.paste(canvas, _img, offset)

                buff = io.BytesIO()
                canvas.save(buff,'png')
                buff.seek(0)

                self.canvas = buff

            elif crop is not None and resize is None:

                _img = img.crop(crop)
                dim = _img.size

                if position is None:
                    offset = ((self.width - dim[0]) // 2, (self.height - dim[1]) // 2)
                else:
                    offset = (position[0], position[1])

                canvas = Image.open(self.canvas)
                Image.Image.paste(canvas, _img, offset)

                buff = io.BytesIO()
                canvas.save(buff, 'png')
                buff.seek(0)

                self.canvas = buff

        else:
            raise Exception("Use either Crop or Resize")
            

    def add_round_image(self, _path:str = None, _byte = None, resize:Tuple = None, crop:Tuple = None, position:Tuple = None):
        pass

