from setuptools import setup

def readme():
    with open('README.md') as file:
        README = file.read()
    return README


setup(
    name = 'image.io',
    version = '1.5.0',
    description = 'Easy Image Manipulation',
    long_description = readme(),
    long_description_content_type="text/markdown",
    package_dir={'ImageIO': 'source'},
    packages=['ImageIO'],
    install_requires=[
        'pillow',
        'urllib3'
    ],
    url = 'https://github.com/jnsougata/Image.IO',
    project_urls={
        "Bug Tracker": "https://github.com/jnsougata/Image.IO/issues"
    },
    author = 'Sougata Jana',
    author_email = 'jnsougata@gmail.com',
    license = 'MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.6"
)
