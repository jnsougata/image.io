# Imgen
Easy image manipulation and card generation

# Quickstart

```python
from imgen import Canvas
canvas = Canvas(width=800, height=400, color='white')
canvas.load_fonts('BALLAD.ttf', 'BEBAS.ttf')
canvas.background('img.png', blur_level=100)
canvas.round_image('img.png', blur_level=100, rotate=180)
canvas.text('Hello World:', font_size=15, font_color="cyan", position_top=1, position_left=40)
canvas.text(
    '''A "Hello, world!" program is generally a computer program that 
    outputs or displays the message "Hello, world!".A small piece of 
    code in most general-purpose programming languages, this program is 
    used to illustrate a language's basic syntax.''',
    font_size=15, font_color="#F535AA", position_top=50, position_left=20)
canvas.show()
```
