import sys, time, os
import pygame
from pynput import keyboard
from collections import deque

if os.name == "nt":
    try:
        import ctypes
    except: pass

BG = (15, 15, 18)
UP = (50, 50, 55)
DOWN = (0, 200, 255)
TXT = (240, 240, 240)

KEYS = [
    "tab","1","2","e","p","=","backspace","\\",
    "capslock","shift","c","space",".","alt_r","enter","ctrl_r"
]

NAME = {
    "capslock":"CAPS",
    "backspace":"BKSP",
    "space":"SPC",
    "shift":"SHIFT",
    "ctrl_r":"RCTRL",
    "alt_r":"RALT",
    "enter":"ENTER",
    "tab":"TAB"
}

class Tracker:
    def __init__(self):
        self.pressed = set()
        self.hist = deque()

    def press(self, key):
        try: k = key.char.lower()
        except: k = str(key).replace("Key.","").lower()
        if k in KEYS:
            if k not in self.pressed:
                self.pressed.add(k)
                self.hist.append(time.time())

    def release(self, key):
        try: k = key.char.lower()
        except: k = str(key).replace("Key.","").lower()
        self.pressed.discard(k)

    def kps(self):
        now = time.time()
        while self.hist and now - self.hist[0] > 1:
            self.hist.popleft()
        return len(self.hist)

pygame.init()

KEY_SIZE = 38
GAP = 6
COLS = 8
ROWS = 2

W = COLS * (KEY_SIZE + GAP) + 20
H = ROWS * (KEY_SIZE + GAP) + 50

screen = pygame.display.set_mode((W, H), pygame.NOFRAME)

from pygame._sdl2 import Window
win = Window.from_display_module()

info = pygame.display.Info()
win.position = (20, info.current_h - H - 40)

if sys.platform == "darwin":
    try: win.always_on_top = True
    except: pass
if os.name == "nt":
    try:
        hwnd = pygame.display.get_wm_info()["window"]
        ctypes.windll.user32.SetWindowPos(hwnd, -1, 0,0,0,0, 1|2)
    except: pass

font = pygame.font.Font(None, 18)
clock = pygame.time.Clock()
tracker = Tracker()

rects = {}
for i,k in enumerate(KEYS):
    r = i // COLS
    c = i % COLS
    x = 10 + c * (KEY_SIZE + GAP)
    y = 30 + r * (KEY_SIZE + GAP)
    rects[k] = pygame.Rect(x,y,KEY_SIZE,KEY_SIZE)

listener = keyboard.Listener(on_press=tracker.press, on_release=tracker.release)
listener.start()

drag = False
start_mouse = (0, 0)
start_win = (0, 0)

while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            listener.stop()
            sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            drag = True
            start_mouse = pygame.mouse.get_pos()
            start_win = win.position

        if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            drag = False

        if e.type == pygame.MOUSEMOTION and drag:
            mx, my = pygame.mouse.get_pos()
            dx = mx - start_mouse[0]
            dy = my - start_mouse[1]
            win.position = (start_win[0] + dx, start_win[1] + dy)

    screen.fill(BG)
    screen.blit(font.render(f"KPS {tracker.kps()}", True, TXT), (10,8))

    for k,r in rects.items():
        pygame.draw.rect(screen, DOWN if k in tracker.pressed else UP, r, border_radius=8)
        label = NAME.get(k, k.upper())
        t = font.render(label, True, TXT)
        screen.blit(t, t.get_rect(center=r.center))

    pygame.display.flip()
    clock.tick(60)
