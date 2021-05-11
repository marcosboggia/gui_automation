# Made by Marcos Boggia
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name='gui_automation',
    version='3.2.1',
    author="Marcos Boggia",
    author_email="marcos_boggia@hotmail.com",
    description="Simple python library useful for automating tasks using images.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marcosboggia/gui_automation",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'opencv-python',
        'PyAutoGUI',
        'imutils',
        'pywin32',
        'pywin32-ctypes',
        'pywinauto'
    ],
    classifiers=[
     "Programming Language :: Python :: 3",
     "License :: OSI Approved :: MIT License",
     "Operating System :: OS Independent",
    ],
 )
