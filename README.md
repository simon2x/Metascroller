# Metascroller (Works on X Display Manager only)

A small app script with tray icon to allow meta + scroll wheel to trigger global shortcuts (does not require sudo)

Requires global shortcuts defined. At the moment, this cannot be configured in the app. The metascroller.py script itself must be altered.

- Meta+Ctrl+Left e.g. mapped to switch to previous workspace
- Meta+Ctrl+Right e.g. mapped to switch to next workspace

By default, Meta+ScrollUp triggers Meta+Ctrl+Right and Meta+ScrollDown triggers Meta+Ctrl+Left

Works on X Display Manager only as python library `pynpyt` only supports this and not Wayland.

## Install (Tested on Kubuntu 22.04)

```
git clone https://github.com/simon2x/Metascroller.git
```

```
cd Metascroller
```

```
pip3 install -r requirements.txt
```

## Run

```
Run the metascroller.sh executable
```

## Optional 
Create a desktop application entry targeting `metascroller.sh` in your desktop environment (see the other/shortcut-example.png)

## Other

- Some instructions may need to modified to work on other distributions e.g. differences between how python/pip is handled
- This will not block the scroll wheel event from occurring. So if your mouse is over an application like a webpage and perform Meta+Scroll, then the webpage will also scroll
- This script is intended for switching workspaces, but you can choose to map the shortcut for anything else your desktop environment can handle