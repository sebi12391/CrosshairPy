import sys
import os
import pyautogui
import ctypes
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from screeninfo import get_monitors
import json

# Default settings
DEFAULT_SETTINGS = {
    "CROSSHAIR_IMAGE_NAME": "crosshair.png",
    "RESIZE_IMAGE": True,
    "RESIZE_TO_WIDTH": 50,
    "RESIZE_TO_HEIGHT": 50,
    "TIMER_INTERVAL_MS": 1,
    "FOLLOW_MOUSE": True,
    "OFFSET_X": 0,  # Offset from the center or mouse in the X-axis
    "OFFSET_Y": 0   # Offset from the center or mouse in the Y-axis
}

# Check if the settings file exists, if not, create it with default values
SETTINGS_FILE = "settings.json"
if not os.path.isfile(SETTINGS_FILE):
    with open(SETTINGS_FILE, "w") as settings_file:
        json.dump(DEFAULT_SETTINGS, settings_file, indent=4)

# Read settings from the file
with open(SETTINGS_FILE, "r") as settings_file:
    SETTINGS = json.load(settings_file)

# Set the title of the command prompt window to "Crosshair Controller"
ctypes.windll.kernel32.SetConsoleTitleW("Crosshair Controller")

class Crosshair(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Set window properties
        self.setWindowTitle("Crosshair Overlay")  # Set the crosshair window title
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowTransparentForInput
        )
        
        # Get the screen resolution using screeninfo
        monitor = get_monitors()[0]  # Assuming the user wants to use the primary monitor
        screen_width, screen_height = monitor.width, monitor.height
        
        self.setGeometry(0, 0, screen_width, screen_height)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Create a QLabel for the crosshair image
        self.crosshair_label = QLabel(self)
        original_pixmap = QPixmap(SETTINGS["CROSSHAIR_IMAGE_NAME"])
        if SETTINGS["RESIZE_IMAGE"]:
            pixmap = original_pixmap.scaled(SETTINGS["RESIZE_TO_WIDTH"], SETTINGS["RESIZE_TO_HEIGHT"], Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            pixmap = original_pixmap
        self.crosshair_label.setPixmap(pixmap)
        self.crosshair_label.setGeometry(
            pixmap.rect().x(), pixmap.rect().y(), pixmap.width(), pixmap.height()
        )

        # Set up a timer to continuously update the crosshair position
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCrosshairPosition)
        self.timer.start(SETTINGS["TIMER_INTERVAL_MS"])

        # Print current settings
        print(f"Current Settings:\n"
              f"Crosshair Image: {SETTINGS['CROSSHAIR_IMAGE_NAME']}\n"
              f"Resize Image: {SETTINGS['RESIZE_IMAGE']}\n"
              f"Resize to Width: {SETTINGS['RESIZE_TO_WIDTH']}\n"
              f"Resize to Height: {SETTINGS['RESIZE_TO_HEIGHT']}\n"
              f"Timer Interval (ms): {SETTINGS['TIMER_INTERVAL_MS']}\n"
              f"Follow Mouse: {SETTINGS['FOLLOW_MOUSE']}\n"
              f"Offset X: {SETTINGS['OFFSET_X']}\n"
              f"Offset Y: {SETTINGS['OFFSET_Y']}\n")

    def updateCrosshairPosition(self):
        if SETTINGS["FOLLOW_MOUSE"]:
            # Get the current cursor position
            cursor_x, cursor_y = pyautogui.position()

            # Calculate the crosshair position with offset
            crosshair_x = cursor_x - self.crosshair_label.width() // 2 + SETTINGS["OFFSET_X"]
            crosshair_y = cursor_y - self.crosshair_label.height() // 2 + SETTINGS["OFFSET_Y"]
        else:
            # Display the crosshair in the center of the screen with offset
            crosshair_x = (self.width() - self.crosshair_label.width()) // 2 + SETTINGS["OFFSET_X"]
            crosshair_y = (self.height() - self.crosshair_label.height()) // 2 + SETTINGS["OFFSET_Y"]

        # Move the crosshair label to the calculated position
        self.crosshair_label.move(crosshair_x, crosshair_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    crosshair = Crosshair()
    crosshair.show()
    print("Crosshair program is running.")
    sys.exit(app.exec_())
