import io
import os
from typing import Tuple, Union, List
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import textwrap


MISSING = object()
PathLike = Union[str, bytes, io.BytesIO]
ColorLike = Union[str, Tuple[int, int, int], float, int]


class Canvas:

    def __init__(
            self,
            width: int = 2048,
            height: int = 1080,
            color: ColorLike = 'white',
    ):
        self.fonts = []
        self.width, self.height = width, height
        card = Image.new("RGB", (width, height), color='white')
        buff = io.BytesIO()
        card.save(buff, 'png')
        buff.seek(0)
        self.__buff = buff

    def load_fonts(self, *fonts: PathLike):
        for font in fonts:
            self.fonts.append(font)

    def background(self, path: PathLike, *, blur_level: int = MISSING):
        canvas = Image.open(self.__buff)
        bg = Image.open(path)
        if blur_level is not MISSING:
            bg = bg.filter(ImageFilter.GaussianBlur(radius=blur_level))
        canvas.paste(bg.resize((self.width, self.height), resample=Image.LANCZOS), (0, 0, self.width, self.height))
        buff = io.BytesIO()
        canvas.save(buff, 'png')
        buff.seek(0)
        self.__buff = buff

    def image(
            self,
            path: PathLike,
            position_left: int = MISSING,
            position_top: int = MISSING,
            *,
            rotate: int = MISSING,
            resize_x: int = MISSING,
            resize_y: int = MISSING,
            crop_left: int = MISSING,
            crop_top: int = MISSING,
            crop_right: int = MISSING,
            crop_bottom: int = MISSING,
            blur_level: int = MISSING,
    ):
        canvas = Image.open(self.__buff)
        img = Image.open(path)
        if rotate is not MISSING:
            img = img.rotate(rotate)
        if blur_level is not MISSING:
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_level))
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
        self.__buff = buff

    def round_image(
            self,
            path: PathLike,
            position_left: int = MISSING,
            position_top: int = MISSING,
            *,
            rotate: int = MISSING,
            resize_x: int = MISSING,
            resize_y: int = MISSING,
            crop_left: int = MISSING,
            crop_top: int = MISSING,
            crop_right: int = MISSING,
            crop_bottom: int = MISSING,
            blur_level: int = MISSING,
    ):
        canvas = Image.open(self.__buff)
        img = Image.open(path)
        if rotate is not MISSING:
            img = img.rotate(rotate)
        if blur_level is not MISSING:
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_level))
        if img.width != img.height:
            crop_val = (max(img.size) - min(img.size)) // 2
            if img.height > img.width:
                img = img.crop((0, crop_val, img.width, img.height - crop_val))
            else:
                img = img.crop((crop_val, 0, img.width - crop_val, img.height))
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
        canvas.paste(img, offset, mask)
        buff = io.BytesIO()
        canvas.save(buff, 'png')
        buff.seek(0)
        self.__buff = buff

    def text(
            self,
            text: str,
            text_spacing: float = 0.0,
            position_left: float = MISSING,
            position_top: float = MISSING,
            *,
            font_index: int = 0,
            font_size: int = 30,
            font_color: ColorLike = 'black',
    ):
        if text == '':
            raise ValueError('text cannot be empty')
        if len(self.fonts) == 0:
            raise ValueError('fonts cannot be empty if text is used. use `load_font(...)` to add fonts')
        if font_index >= len(self.fonts):
            raise ValueError('font_index cannot be greater than the number of fonts added to the canvas')
        canvas = Image.open(self.__buff)
        font = ImageFont.truetype(self.fonts[font_index], size=font_size)
        draw = ImageDraw.Draw(canvas)
        text_width, text_height = draw.textsize(text, font=font, spacing=text_spacing)
        if position_left is MISSING and position_top is not MISSING:
            offset = (self.width - text_width) / 2, position_top
        elif position_left is not MISSING and position_top is MISSING:
            offset = position_left, (self.height - text_height) / 2
        elif position_left is MISSING and position_top is MISSING:
            offset = (self.width - text_width) / 2, (self.height - text_height) / 2
        else:
            offset = position_left, position_top
        if len(text) * font_size // 2 > self.width:
            text = textwrap.fill(text, width=int(self.width // font_size * 1.199999))
        else:
            draw.text(offset, text, font=font, fill=font_color, spacing=text_spacing)

        draw.text(offset, text, font=font, fill=font_color)
        buff = io.BytesIO()
        canvas.save(buff, 'png')
        buff.seek(0)
        self.__buff = buff

    def read(self) -> bytes:
        return self.__buff.read()

    def show(self):
        Image.open(self.__buff).show()

    def save(self, path: PathLike):
        img = Image.open(self.__buff)
        img.save(path)
