import pyautogui
import time
import sys
import os
from datetime import datetime
from termcolor import colored
import random


MIN_SQ_GAP = 20
MOVE_DURATION = 0.15
MARKER_OFFSET = (0, 85)
CHOICE_OFFSET = (15, 0)
PROD_SELECT_DELAY = 0.8  # wait time between subsequent production selections
LPAD = ' ' * 4
TWEEN = pyautogui.easeOutQuad

class ImageNotFound(Exception):
    pass

def dist_sq(a, b):
    """ 
    Calculates the squared euclidean distance between points a and b 
    """
    return (a[0] - b[0])**2 + (a[1] - b[1])**2

def add_vecs(a, b):
    """
    Performs a + b for vectors a and b of the same lengths
    Throws assertion error
    """
    assert len(a) == len(b), 'Can not add vectors of different lengths'
    return tuple(map(lambda i: a[i] + b[i], range(len(a))))

def locate_and_parse(needle, haystack, confidence=0.8):
    res = pyautogui.locateAll(needle, haystack, confidence=confidence, grayscale=False)
    res = list(res)

    if not res:
        return []

    # remove points that are close to the previous targets as well as those 
    # that are close to the second to last targets
    # helps with the multiple detection of the same coin image
    # the second condition prevents some of the oscillations between targets
    # on similar y coordinates
    centers = [pyautogui.center(res[0])]
    for rect in res:
        center = pyautogui.center(rect)
        if dist_sq(center, centers[-1]) > MIN_SQ_GAP:
            if len(centers) >= 2 and dist_sq(center, centers[-2]) > MIN_SQ_GAP:
                centers.append(center)
            elif len(centers) < 2:
                centers.append(center)
    return centers

# TODO three functions beloew are similar to each other

def collect_coins(screen):
    buildings = locate_and_parse('images/coin_with_star.png', screen)
    buildings.extend(locate_and_parse('images/coin.png', screen))
    if not buildings:
        print(colored(LPAD + '-No coins to collect', 'yellow'))
        return
    for building in buildings:
        pyautogui.moveTo(add_vecs(building, MARKER_OFFSET), duration=MOVE_DURATION, tween=TWEEN)
        pyautogui.click()
    print(colored(LPAD + f'-Collected coins from {len(buildings)} buildings', 'green'))

def collect_units(screen):
    buildings = locate_and_parse('images/swords.png', screen, confidence=0.7)
    if not buildings:
        print(colored(LPAD + '-No units to collect', 'yellow'))
        return
    for building in buildings:
        pyautogui.moveTo(add_vecs(building, MARKER_OFFSET), duration=MOVE_DURATION, tween=TWEEN)
        pyautogui.click()
    print(colored(LPAD + f'-Collected {len(buildings)} units', 'green'))

def collect_production(screen):
    buildings = locate_and_parse('images/tool.png', screen)
    if not buildings:
        print(colored(LPAD + '-No supply to collect', 'yellow'))
        return
    for building in buildings:
        pyautogui.moveTo(add_vecs(building, MARKER_OFFSET), duration=MOVE_DURATION, tween=TWEEN)
        pyautogui.click()

    print(colored(LPAD + f'-Collected supply from {len(buildings)} buildings','green'))

def find_production_target(region=None):
    """
    Returns the bottom right edge of target box
    """
    result = None
    box = pyautogui.locateOnScreen('images/15min.png', region=region, confidence=0.9)
    if box is not None:
        # its a normal production building
        result = box
   
    if not result:
        box = pyautogui.locateCenterOnScreen('images/recruit.png', region=region)
        if box is not None:
             # its an army training building
            result = box
    
    if not result:
         # its unidentifiable
        print('NOO targeet')
        return None
    x, y, w, h = box
    return (x + w, y+h)

def start_production():
    """
    Returns false if no buildings were found
    """
    time.sleep(1)  # wait for the moons to appear
    building = pyautogui.locateCenterOnScreen('images/moon2.png', confidence=0.7)
    if not building:
        print(colored(LPAD + '-No sleeping supply buildings', 'cyan'))
        return False

    pyautogui.moveTo(add_vecs(building, MARKER_OFFSET), duration=MOVE_DURATION, tween=TWEEN)
    pyautogui.click()  # open the production selection menu
    time.sleep(0.5)  # wait for the menu to pop out

    # click the choice button as long as there are popups
    target = find_production_target()
    prod_start_count = 0
    while target:
        # raise ImageNotFound('Could not find the production choice field')
        pyautogui.moveTo(add_vecs(target, CHOICE_OFFSET), duration=MOVE_DURATION)
        pyautogui.click()
        prod_start_count += 1
        time.sleep(PROD_SELECT_DELAY)

        x, y = target
        target_region = (x - 80, y - 30, 160, 80)  # some optimization
        target = find_production_target(region=target_region)
    else:
        if prod_start_count > 0:
            print(colored(LPAD + f'-Started production in {prod_start_count} buildings', 'green'))
        return True
    
def main():
    os.system('color')
    # input
    delay = pyautogui.prompt( text='How often to scan the screen (in seconds)', 
                    title='FOE automatic gatherer', 
                    default=str(60))

    try:
        assert delay is not None, 'Quitting'
        delay = int(delay)
        assert delay > 0, 'Delay cant be negative. Aborting'
    except ValueError:
        print(f'Argument {delay} can not be converted to int. Aborting')
        sys.exit()
    except AssertionError as e:
        print(str(e))
        sys.exit()

    print(f'\nStarting the collector.\nDelay = {delay}.\nPress Ctrl+C to quit.')

    # the main loop
    no_of_executions = 1
    while True:
        try:
            print(f'Execution #{no_of_executions} at {datetime.now().strftime("%H:%M:%S")}')
            screen = pyautogui.screenshot()
            collect_coins(screen)
            collect_units(screen)
            collect_production(screen)
            while start_production():
                pass
            time.sleep(delay)
            no_of_executions += 1
        except KeyboardInterrupt:
            print("Goodbye")
            sys.exit()

if __name__ == '__main__':
    main()