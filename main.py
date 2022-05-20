import pygame, os, json, screeninfo
from timer import Window

# get settings
if os.path.exists("settings.json"):
    with open("settings.json") as f:
        settings = json.load(f)
else:
    with open("settings.json", 'w') as f:
        json.dump({}, f)

# initialize window
pygame.init()

for m in screeninfo.get_monitors():
    if m.is_primary:
        window = Window(m, settings)

# main loop
done = False
while not done:
    done = window.update()
    window.draw()
pygame.quit()


