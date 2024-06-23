import pyautogui

# -- keyboard -- #

def send_hotkey(*key):
    pyautogui.hotkey(key)

def send_key(key):
    pyautogui.press(key)

def write_text(text, interval=0.0):
    pyautogui.write(text, interval=interval)

# -- mouse -- #

def get_mouse_position():
    return pyautogui.position()

def move_mouse_to(x, y, duration=0):
    pyautogui.moveTo(x, y, duration)

def click_mouse(button='left'):
    pyautogui.click(button=button)

def right_click():
    pyautogui.click(button='right')

def double_click():
    pyautogui.doubleClick()

def drag_mouse_to(x, y, duration=0):
    pyautogui.dragTo(x, y, duration)

def drag_mouse(x_offset, y_offset, duration=0):
    pyautogui.drag(x_offset, y_offset, duration)
    
# -- other -- #

def take_screenshot(region=None):
    screenshot = pyautogui.screenshot(region=region)
    from main.functions._file.file import timestamped_filename, get_screenshot_folder
    path = get_screenshot_folder()
    screenshot.save(path + "\\" + timestamped_filename(".png", "screenshot"))

