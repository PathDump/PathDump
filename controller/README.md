# PathDump Controller

Python implementation of PathDump controller.

## How to install

```
sudo ./install.sh <directory>
```

\<directory\> is the target directory to install the controller module. If the
user has write permission on the target directory, 'sudo' can be omitted.

## How to run

Go to the directory that the controller is installed, and run:

```
sudo ./agent.py <config file>
```

A configuration file (\<config file\>) should be specified. 'sudo' can be
omitted again if the user owns the directory.

## Dependency

External Python packages (Flask and watchdog) are required. The installation
script attempts to install the packages using pip.

## Additional notes

An example configuration file is config/controller/pathdump.cfg. This
configuration file is copied to the specified installation directory during
the installation process. 
