import io
from typing import Tuple, Union
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PathLike = Union[str, bytes, io.BytesIO]
ColorLike = Union[str, Tuple[int, int, int], float, int]
MISSING = object()


class Canvas:

    def __init__(self, width: int = 1280, height: int = 720, color: ColorLike = 'white'):
        self.width, self.height = width, height
        card = Image.new("RGB", (width, height), color='white')
        buff = io.BytesIO()
        card.save(buff, 'png')
        buff.seek(0)
        self.buff = buff

    def background(self, path: PathLike, *, blur_level: int = MISSING):
        canvas = Image.open(self.buff)
        bg = Image.open(path)
        if blur_level is not MISSING:
            bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_level))
        canvas.paste(bg.resize((self.width, self.height), resample=Image.LANCZOS), (0, 0, self.width, self.height))
        buff = io.BytesIO()
        canvas.save(buff, 'png')
        buff.seek(0)
        self.buff = buff

    def image(
            self,
            path: PathLike,
            position_left: int = MISSING,
            position_top: int = MISSING,
            *,
            resize_x: int = MISSING,
            resize_y: int = MISSING,
            crop_left: int = MISSING,
            crop_top: int = MISSING,
            crop_right: int = MISSING,
            crop_bottom: int = MISSING
    ):
        canvas = Image.open(self.buff)
        img = Image.open(path)
        if resize_x is not MISSING and resize_y is MISSING:
            img = img.resize((resize_x, img.size[1]))
        elif resize_x is MISSING and resize_y is not MISSING:
            img = img.resize((img.size[0], resize_y))
        elif resize_x is not MISSING and resize_y is not MISSING:
            img = img.resize((resize_x, resize_y))
        cl = 0 if crop_left is MISSING else crop_left
        ct = 0 if crop_top is MISSING else crop_top
        cr = img.width if crop_right is MISSING else crop_right
        cb = img.height if crop_bottom is MISSING else crop_bottom
        img = img.crop((cl, ct, cr, cb))
        if position_left is MISSING and position_top is not MISSING:
            offset = (self.width - img.width) // 2, position_top
        elif position_left is not MISSING and position_top is MISSING:
            offset = position_left, (self.height - img.height) // 2
        elif position_left is MISSING and position_top is MISSING:
            offset = (self.width - img.width) // 2, (self.height - img.height) // 2
        else:
            offset = position_left, position_top
        canvas.paste(img, box=offset)
        buff = io.BytesIO()
        canvas.save(buff, 'png')
        buff.seek(0)
        self.buff = buff

    def round_image(
            self,
            path: PathLike,
            position_left: int = MISSING,
            position_top: int = MISSING,
            *,
            resize_x: int = MISSING,
            resize_y: int = MISSING,
            crop_left: int = MISSING,
            crop_top: int = MISSING,
            crop_right: int = MISSING,
            crop_bottom: int = MISSING
    ):
        canvas = Image.open(self.buff)
        img = Image.open(path)
        if resize_x is not MISSING and resize_y is MISSING:
            img = img.resize((resize_x, img.size[1]))
        elif resize_x is MISSING and resize_y is not MISSING:
            img = img.resize((img.size[0], resize_y))
        elif resize_x is not MISSING and resize_y is not MISSING:
            img = img.resize((resize_x, resize_y))
        cl = 0 if crop_left is MISSING else crop_left
        ct = 0 if crop_top is MISSING else crop_top
        cr = img.width if crop_right is MISSING else crop_right
        cb = img.height if crop_bottom is MISSING else crop_bottom
        img = img.crop((cl, ct, cr, cb))
        if position_left is MISSING and position_top is not MISSING:
            offset = (self.width - img.width) // 2, position_top
        elif position_left is not MISSING and position_top is MISSING:
            offset = position_left, (self.height - img.height) // 2
        elif position_left is MISSING and position_top is MISSING:
            offset = (self.width - img.width) // 2, (self.height - img.height) // 2
        else:
            offset = position_left, position_top
        img = img.crop((cl, ct, cr, cb))
        mask = Image.new("L", img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.pieslice(((0, 0), img.size), 0, 360, fill=255, outline="white")
        if position_left == 0 and position_top != 0:
            offset = (self.width - img.size[0]) / 2, position_top
        elif position_left != 0 and position_top == 0:
            offset = position_left, (self.height - img.size[1]) / 2
        else:
            offset = position_left,
        canvas.paste(img, offset, mask)
        buff = io.BytesIO()
        canvas.save(buff, 'png')
        buff.seek(0)
        self.buff = buff

    def text(
            self,
            text: str,
            font_pack: PathLike,
            *,
            font_size: int = 30,
            position_left: float = MISSING,
            position_top: float = MISSING,
            font_color: ColorLike = 'black',
    ):
        if text == '':
            raise ValueError('text cannot be empty')

        canvas = Image.open(self.buff)
        font = ImageFont.truetype(font_pack, size=font_size)
        draw = ImageDraw.Draw(canvas)
        text_width, text_height = draw.textsize(text, font=font)

        if position_left is MISSING and position_top is not MISSING:
            offset = (self.width - text_width) / 2, position_top
        elif position_left is not MISSING and position_top is MISSING:
            offset = position_left, (self.height - text_height) / 2
        elif position_left is MISSING and position_top is MISSING:
            offset = (self.width - text_width) / 2, (self.height - text_height) / 2
        else:
            offset = position_left, position_top
        draw.text(offset, text, font=font, fill=font_color)
        buff = io.BytesIO()
        canvas.save(buff, 'png')
        buff.seek(0)
        self.buff = buff

    def show(self):
        Image.open(self.buff).show()

    def save(self, path: PathLike):
        img = Image.open(self.buff)
        img.save(path)
