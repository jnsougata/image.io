

# ImageIO 

**ImageIO**  is a package created to power the user with easy image manipulation like  **circular cropping**,  **merging two images**,  **adding text**  etc.

[**GitHub**](https://github.com/jnsougata/Image.IO) | [**Join Discord**](https://discord.gg/YAFGAaMrTC)
    
# How to use?
- **Imports:**
	- `from ImageIO import Io, Canvas`
	
- **Code walk through:**
	- **Draw an image:**
		- `img  = Io.draw(size = (width, height), color:hex or str [optioanl])`
			> Returns a rect image (BytesIO Form) of color of give hex string
		
	- **Fetch image from URL:**
		- `img  = Io.fetch(url = 'image url')`
			> Returns an image (BytesIO Form) from the given URL 
			
	- **Create a canvas:**
		- `canvas = Canvas(size = (hight, width), color:hex or str [optional])`
			> Creates a canvas object of given size and color
			
		- **Set background to canvas:**
			- `canvas.set_background(_byte, _path, _blur)` 
				- **_byte:** any image of BytesIO form
				- **_path:** any image path of local image
				- **_blur:** bool: makes the image blur if True
					- *use either **_byte** or **_path*** [**mandatory**]
					
		- **Add image to canvas:**
			- `canvas.add_image(_path, _byte, resize, crop, position)` 
				- **_byte:** any image of BytesIO form
				- **_path:** any image path of local image
				- **resize:** a tuple: (width, height) to resize the image
				- **crop:** a tuple: (left, top, right, bottom) to crop the image
				- **position:** a tuple: (x, y) to add the image inside the canvas
					- *use either **_byte** or **_path*** [**mandatory**]
					- *use either **resize** or **crop*** [**optional**]
					
		- **Add round image to canvas:**
			- `canvas.add_round_image(_path, _byte, resize, crop, position)` 
				- **_byte:** any image of BytesIO form
				- **_path:** any image path of local image
				- **resize:** a tuple: (width, height) to resize the image
				- **crop:** a tuple: (left, top, right, bottom) to crop the image
				- **position:** a tuple: (x, y) to add the image inside the canvas
					- *use either **_byte** or **_path*** [**mandatory**]
					- *use either **resize** or **crop*** [**optional**]
					- ***auto aligns** image to center if position is **None***
					
		- **Add text to canvas:**
			- `canvas.add_text(text, font_pack, auto_align, size, color, position)` 
				- **text:** any str: to add on the canvas
				- **font_pack:** path to the font pack in your local directory
				- **auto_align:** a bool: aligns the text horizontally if **True**
				- **size:** float: size of the text in pixel [***defaults to 20***]
				- **color:** hex or str: fills the text with the color [***defaults to white***]
				- **position:** a tuple: (x, y) to add the text inside the canvas 
					- *auto aligns text to center if position is **None***
			
		- **Save canvas locally:**
			- `canvas.save(name)` 
				- **name:** str: name of the image with extension [ *png,  jpg* ] (recommended)
	
