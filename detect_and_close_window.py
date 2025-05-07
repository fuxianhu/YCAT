import time
from pywinauto import Application

def detect_and_close_window(window_title):
    try:
        # Connect to the window with the specified title
        app = Application(backend='uia').connect(title=window_title)
        # Get the window handle
        window = app.window(title=window_title)
        # Close the window
        window.close()
        print(f"Window '{window_title}' has been closed.")
    except Exception as e:
        print(f"Window '{window_title}' not found or could not be closed: {e}")

if __name__ == "__main__":
    window_title = "FastGithub.UI v2.1.5"
    while True:
        detect_and_close_window(window_title)
        time.sleep(1)  # Check every second