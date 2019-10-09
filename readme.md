
## Multi vlc
Tool to run many vlc at same time on early prepared position.

In vlc must be configured to allow multiple instances.
Unix pipe are used to communicate with vlc via remote control interface.

To find, move and resize window position 'xdotool' is used.
After vlc start, it is awaited short time on vlc windows initialization.

Tested on VLC version:
 - 3.0.6 Vetinari (3.0.6-0-g5803e85)
 - 4.0.0-dev Otto Chriek

#### Usage:

1. Create configuration
2. Save configuration
3. Run vlc instances

####Warning:
IN VLC settings minimal interface must be disabled