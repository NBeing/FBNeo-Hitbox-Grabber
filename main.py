import pyautogui
import pygetwindow
import PIL
import time

import input_handler
import keyboard
# https://stackoverflow.com/questions/70161288/pydirectinput-pynput-pyautogui-dont-always-press-keys
# https://docs.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-6.0/aa299374(v=vs.60)?redirectedfrom=MSDN
FBNEO_KEYS = {
    "lp"        : 0x16, # u
    "mp"        : 0x17,
    "hp"        : 0x18,
    "lk"        : 0x24,
    "mk"        : 0x25,
    "hk"        : 0x26,
    "up"        : 0x11,
    "down"      : 0x10,
    "left"      : 0x10,
    "right"     : 0x12,
    "pause"     : 0x19, # P
    "next_frame": 0x29, # `
    "record"    : 0x15,
    "playback"  : 0x23,
}

# get screensize
screen_x,screen_y = pyautogui.size()
print("Screen size",screen_x, screen_y)

def is_window_name_fbneo(window_title):
    pref_list = ['FinalBurn', 'Fightcade']
    res = list(filter(window_title.startswith, pref_list)) != []
    return res == True

#try to get fbneo window
def get_fbneo_window():
    # get all window titles
    window_titles = pygetwindow.getAllTitles()
    window_titles = list(filter( is_window_name_fbneo, window_titles))
    print("Fbneo window", window_titles[0])
    return window_titles[0]



def get_window_coords(window):
    my = pygetwindow.getWindowsWithTitle(window)[0]
    my.moveTo(0,0)
    fbneo_win_x = my.width
    fbneo_win_y = my.height
    print("Fbneo coords", fbneo_win_x, fbneo_win_y)
    my.activate()
    time.sleep(3)
    return (fbneo_win_x, fbneo_win_y)

print(FBNEO_KEYS["pause"])
fbneo_window = get_fbneo_window()
fbneo_win_x, fbneo_win_y = get_window_coords(fbneo_window)

def do_screenshot_and_crop(num):
    # save screenshot
    p = pyautogui.screenshot()
    p.save(r'uncropped.png')

    # edit screenshot
    im = PIL.Image.open('uncropped.png')
    print("Fbneo coords", fbneo_win_x, fbneo_win_y)

    im_crop = im.crop((10, 0, fbneo_win_x - 10, fbneo_win_y - 10))
    im_crop.save("{0}.png".format(num), quality=100)

def do_screenshot_and_frame_advance(num):
    do_screenshot_and_crop(num)
    print("Press")
    input_handler.PressKey(FBNEO_KEYS["next_frame"])
    time.sleep(.25)
    print("release")
    input_handler.ReleaseKey(FBNEO_KEYS["next_frame"])
    time.sleep(1)

def pause_game():
    input_handler.PressKey(FBNEO_KEYS["pause"])
    time.sleep(1)
    input_handler.ReleaseKey(FBNEO_KEYS["pause"])
def input_frame( movelist ):
    input_handler.PressKey(FBNEO_KEYS["lp"])
    input_handler.PressKey(FBNEO_KEYS["next_frame"])
    time.sleep(0.25)
    input_handler.ReleaseKey(FBNEO_KEYS["next_frame"])
    input_handler.ReleaseKey(FBNEO_KEYS["lp"])

def record_move():
    numFrames = 0
    pause_game()

    input_handler.PressKey(FBNEO_KEYS["lp"])
    while numFrames < 25:
        do_screenshot_and_frame_advance(numFrames)
        numFrames = numFrames + 1
    input_handler.ReleaseKey(FBNEO_KEYS["lp"])

while True:
    if keyboard.is_pressed('r'):
        print("Beginning increment move", flush=True)
        record_move()
    