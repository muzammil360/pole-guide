# Installation
Make sure you have Python 3.6+ installed. In order to install all the dependencies
```
python -m pip install -r requirements.txt
```

**NOTE**: Please make sure that `python` points to a python installation of `v3.6` or above. To check absolute path of python execuable being pointed to, type
```
which Python
```

# How to run
Go to `<project_root>` and type 
```
python main.py --weights=<path/to/weights/file>
```
Above is the bare minimum command. You can change more settings by giving additional command line args. For more info, keep reading this readme.

## Visualization
In order to visualize the detection output, use `--visualize` flag with the run command.

## How to change settings
In order to see a list of command line arguments, type
```
python main.py --help
```

Some of the settings have been harded. In order to change them, take a look at `main.py` after the line `if __name__ == '__main__':` . 

**WARNING**: You need to understand what you are doing while changing these settings. 