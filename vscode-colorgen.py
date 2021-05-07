import numpy as np
from colormap import rgb2hex, rgb2hls, hls2rgb
import json
import os
import errno
import random

# User variables:
# all h, s, l values must be between 0.0 and 1.0. Take into account the 
# lighten/darken factors
# 
# l: luminosity - how bright or dark the color is.
# s: saturation - how vibrant the color is
# lighten_factor: - will add or subtract this amount to create some variations
l = 0.2
s = 0.08
lighten_factor = 0.05
darken_factor = 0.05

# Begin
config_file = '.vscode/settings.json'
h = random.SystemRandom().random()


def lighten(h, l, s, factor):
    l = l + factor
    r, g, b = hls2rgb(h, l, s)
    return rgb2hex(int(r * 255), int(g * 255), int(b * 255))


def darken(h, l, s, factor):
    return lighten(h, l, s, factor * -1)


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            # get node or create one
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value
    return destination

# initial color mid-dark color:
mid = lighten(h, l, s, 0.0)
lighter = lighten(h, l, s, lighten_factor)
darker = darken(h, l, s, darken_factor)

# Generate the settings.json config
workbench = {}
workbench["workbench.colorCustomizations"] = {}
workbench["workbench.colorCustomizations"]["tab.inactiveBackground"] = lighter
workbench["workbench.colorCustomizations"]["titleBar.activeBackground"] = mid
workbench["workbench.colorCustomizations"]["activityBar.background"] = mid
workbench["workbench.colorCustomizations"]["editorGroupHeader.tabsBackground"] = mid
workbench["workbench.colorCustomizations"]["sideBar.background"] = darker
workbench["workbench.colorCustomizations"]["statusBar.background"] = "#252526"

# create .vscode if not exists
os.makedirs(os.path.dirname(config_file), exist_ok=True)

# super lazy way to get open file and just continue if it doesn't exist
config = {}
try:
    f = open(config_file,"r")
    config = json.load(f)
    f.close()
except:
    pass

# Deep merge color config into existing settings.json config
merge(workbench, config)

# write the file back out!
f = open(config_file,"w")
f.write(json.dumps(workbench, indent=2))
f.close()



