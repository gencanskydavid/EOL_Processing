#usr/bin/python3

import yaml
import os,sys

CONFIG_PATH = "config.yaml"

def find_data_file(filename):
    if getattr(sys, 'frozen', False):
        # The application is frozen
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen
        datadir = os.path.dirname(os.path.realpath(__file__))
        # The following line has been changed to match where you store your data files:
    
    return os.path.join(datadir, filename)

class ConfigError(Exception):
    pass

try:
    with open(find_data_file(CONFIG_PATH), 'r') as stream:
        config = yaml.safe_load(stream)
except FileNotFoundError as e:
    raise ConfigError("config.yaml could not been found.")
except Exception as e:
    raise ConfigError(e)

try:
    PATHS = config["PATHS"]
except KeyError as e:
    raise ConfigError("PATHS setting is not defined in config file. Check the config file.")

try:
    MODE = config["MODE"]
except KeyError as e:
    raise ConfigError("MODE setting is not defined in config file. Check the config file")


if MODE == "auto":
    pass
elif MODE == "manual":
    pass
else:
    raise ConfigError("Invalid MODE setting. Choose 'auto' or 'manual' mode. Check the config file.")



print("Settings:")
print(f" PATHS:")
for key in PATHS:
    print(f"  {key}: {PATHS[key]}")
print(f" MODE: {MODE}")
print("Config has been successfully loaded.")
print("")

