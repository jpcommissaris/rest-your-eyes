import sys
import objc
import platform
from setuptools import setup

APP = ["main.py"]
DATA_FILES = []
OPTIONS = {
    "argv_emulation": True,
    "packages": ["Cocoa", "Quartz", "UserNotifications", "AppKit"],
    "iconfile": None,  # You can set a .icns file here later if you want a custom icon
}

setup(
    app=APP,
    name="Rest Your Eyes",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
