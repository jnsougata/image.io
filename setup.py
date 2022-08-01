from setuptools import setup


def readme():
    with open('README.md') as file:
        return file.read()


setup(
    name='imagen',
    version='0.0.1',
    description='image-card generator/manipulator',
    long_description=readme(),
    long_description_content_type="text/markdown",
    package_dir={'imgen': 'src'},
    packages=['imgen'],
    install_requires=['pillow'],
    url='https://github.com/jnsougata/imgen',
    project_urls={"Bug Tracker": "https://github.com/jnsougata/imgen/issues"},
    author='Sougata Jana',
    author_email='jnsougata@gmail.com',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)
