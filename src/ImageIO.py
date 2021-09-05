import io
from typing import Tuple
from PIL import Image, ImageDraw


class Figure:

    def __init__(self):
        pass


    @staticmethod
    def draw(size: Tuple, color: hex or str = None):
        color = 0x36393f if color is None else color
        new_image = Image.new("RGB", size, color=color)
        buff = io.BytesIO()
        new_image.save(buff, 'png')
        buff.seek(0)
        return buff


    @staticmethod
    def show(source: str or bytes):
        image = Image.open(source)
        image.show()



class Canvas:

    def __init__(self, size:Tuple, color:hex or str = None):
        color = 0x36393f if color is None else color
        size = size if size is not None and len(size) == 2 else None
        card = Image.new("RGB", size, color = color)
        buff = io.BytesIO()
        card.save(buff, 'png')
        buff.seek(0)
        self.width = size[0]
        self.height = size[1]
        self.output = buff


    def show(self):
        image = Image.open(self.output)
        image.show()


    def set_background(self, _byte = None, _path:str = None):
        canvas = Image.open(self.output)
        size = canvas.size
        if _path is not None and _byte is None:
            bg = Image.open(_path)
        elif _byte is not None and _path is None:
            bg = Image.open(_byte)
        else:
            raise Exception("Use either _path or _byte")


        if bg is not None:
            _bg = bg.resize(size)
            buff = io.BytesIO()
            _bg.save(buff, 'png')
            buff.seek(0)
            self.output = buff
        else:
            raise TypeError("Image can not be NoneType")



    def add_image(self, _path:str = None, _byte = None, resize:Tuple = None, crop:Tuple = None, position:Tuple = None):
        canvas = Image.open(self.output)
        if _path is not None and _byte is None:
            img = Image.open(_path)
        elif _byte is not None and _path is None:
            img = Image.open(_byte)
        else:
            raise Exception("Use either _path or _byte")


        if img is not None:

            if resize is not None and crop is None:
                auto_align = ((self.width - resize[0]) // 2, (self.height - resize[1]) // 2)
                manual_align = position
                offset = auto_align if position is None else manual_align
                _img = img.resize(resize, resample=0)
                Image.Image.paste(canvas, _img, offset)
                buff = io.BytesIO()
                canvas.save(buff,'png')
                buff.seek(0)
                self.output = buff
            elif crop is not None and resize is None:
                _img = img.crop(crop)
                dim = _img.size
                auto_align = ((self.width - dim[0]) // 2, (self.height - dim[1]) // 2)
                manual_align = position
                offset = auto_align if position is None else manual_align
                Image.Image.paste(canvas, _img, offset)
                buff = io.BytesIO()
                canvas.save(buff, 'png')
                buff.seek(0)
                self.output = buff
            elif crop is None and resize is None:
                size = img.size
                auto_align = ((self.width - size[0]) // 2, (self.height - size[1]) // 2)
                manual_align = (position[0], position[1])
                offset = auto_align if position is None else manual_align
                Image.Image.paste(canvas, img, offset)
                buff = io.BytesIO()
                canvas.save(buff, 'png')
                buff.seek(0)
                self.output = buff
            else:
                raise Exception('Use either Resize or Crop')
        else:
            raise TypeError('Image can not be NoneType')
            


    def add_round_image(self, _path:str = None, _byte = None, resize:Tuple = None, crop:Tuple = None, position:Tuple = None):
        canvas = Image.open(self.output)
        if _path is not None and _byte is None:
            img = Image.open(_path)
        elif _byte is not None and _path is None:
            img = Image.open(_byte)
        else:
            img = None


        if img is not None:

            if resize is not None and crop is None:
                main = img.resize(resize)
                mask = Image.new("L", main.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.pieslice([(0, 0), main.size], 0, 360,fill=255, outline="white")
                dim = main.size
                auto_align = ((self.width - dim[0]) // 2, (self.height - dim[1]) // 2)
                manual_align = position
                offset = auto_align if position is None else manual_align
                canvas.paste(main, offset, mask)
                buff = io.BytesIO()
                canvas.save(buff, 'png')
                buff.seek(0)
                self.output = buff
            elif crop is not None and resize is None:
                main = img.crop(crop)
                mask = Image.new("L", main.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.pieslice([(0, 0), main.size], 0, 360, fill=255, outline="white")
                dim = main.size
                auto_align = ((self.width - dim[0]) // 2, (self.height - dim[1]) // 2)
                manual_align = position
                offset = auto_align if position is None else manual_align
                canvas.paste(main, offset, mask)
                buff = io.BytesIO()
                canvas.save(buff, 'png')
                buff.seek(0)
                self.output = buff
            elif crop is None and resize is None:
                main = img
                mask = Image.new("L", main.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.pieslice([(0, 0), main.size], 0, 360, fill=255, outline="white")
                dim = main.size
                auto_align = ((self.width - dim[0]) // 2, (self.height - dim[1]) // 2)
                manual_align = position
                offset = auto_align if position is None else manual_align
                canvas.paste(main, offset, mask)
                buff = io.BytesIO()
                canvas.save(buff, 'png')
                buff.seek(0)
                self.output = buff
            else:
                raise Exception('Use either Resize or Crop')

        else:
            raise TypeError('Image can not be NoneType')
