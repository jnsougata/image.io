from ImageIO import *


img1 = Figure.draw((2000, 1000), color='blue')
img3 = Figure.draw((50, 50), color='red')
img2 = Figure.draw((2000, 1000), color='green')

TEST = Canvas(size=(600, 200), color='black')
TEST.add_image(_byte=img1, resize=(200, 100))
TEST.add_image(_byte=img2, resize=(100, 100), position=(470, 50))
TEST.add_round_image(_path="C:\\ImageIO\\test_image.png", resize=(100, 100), position=(30,50))
TEST.show()
