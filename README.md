# FOE Collector

Pyautogui based python program that cyclically checks whether it's possible to perform an action in ForgeOfEmpires.
May be used to automate resources collection over periods of one's absence.
Works only while in medium zoom level.
Collection requires takig control of the mouse.

### Current features:
 * collection of:
    * coins
    * supply
    * units
 * starting the
    * supply production
    * unit training
 * customizable time delay between checks

### Usage:
```
pip install -r requirements
python foe_clicker.py
```
It may be necessary to replace the default images in the `images` directory with appropiate images from one's own screenshot of the game at the desired zoom level.

### TODOs:
- [ ] detection on the furthest zoom level
- [ ] goods collection
- [ ] goods production start
- [ ] improve 'locate' function performance using constrained regions of search
- [ ] passing delay value via the command line
- [ ] customizable production start choices (e.g. 5min/15min/1h...)
