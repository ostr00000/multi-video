## Multi video

Tool to run many video at same time.

There are two implemented players:

- [vlc](https://www.videolan.org/vlc/index.pl.html)
- [mpv](https://mpv.io/)

### Vlc

The vlc player must be configured to allow multiple instances.
Unix pipe are used to communicate with vlc via remote control interface.

To find, move and resize window position 'xdotool' is used.
After vlc start, it is awaited short time on vlc windows initialization.

Tested on VLC version:

- 4.0.0-dev Otto Chriek

#### Warning:

In VLC settings minimal interface must be disabled.

#### Usage:

1. Create configuration
2. Save configuration
3. Run vlc instances

### installation

PyQt5 must be installed before multi_vlc

```bash
python -m pip install PyQt5
python setup.py install
```
