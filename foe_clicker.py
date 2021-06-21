import pyautogui  # for clicking
from pynput import mouse  # for mouse input
import time
import sys
from datetime import datetime

# stored pressed mosue positions
positions = []
is_ready_to_record = False
mouse_pressed = False
last_drag_pos_time = 0

print('To begin the recording press the middle mouse button')
print('Record your left mouse button actions. When your are done, press the right button to finish.')

def on_click(x, y, button, pressed):
    global is_ready_to_record, mouse_pressed
    if button == mouse.Button.middle:
        is_ready_to_record = True
        print('Started the recording')
        return True
    if is_ready_to_record:
        if button == mouse.Button.left:
            mouse_pressed = pressed
            x, y = pyautogui.position()
            print('{} at {}'.format('Pressed Left Click' if pressed else 'Released Left Click', (x, y)))
            positions.append((x, y, time.time(), pressed))
        elif button == mouse.Button.right:
            print("Recording completed")
            return False  # Returning False if you need to stop the listener when Left clicked.
    else:
        return True  # Don't stop the listener

def on_move(x, y):
    global last_drag_pos_time
    now = time.time()
    if mouse_pressed and now - last_drag_pos_time > 0.07:
        x, y = pyautogui.position()
        positions.append((x, y, now, mouse_pressed))
        last_drag_pos_time = time.time()
        print('Pointer moved to {0}'.format((x, y)))

listener = mouse.Listener(on_click=on_click, on_move=on_move)
listener.start()
listener.join()

no_of_executions = 1
try:
    cooldown = 5
    # cooldown = int(input('How many secs to wait before each gathering: '))
    while True:
        curr_move = 0
        time.sleep(cooldown)
        print(f'Execution #{no_of_executions} at {datetime.now().strftime("%H:%M:%S")}')
        
        x0, y0, t0, _ = positions[curr_move]
        pyautogui.moveTo(x0, y0, duration=0.1)

        while curr_move != len(positions) - 1:
            curr_move += 1
            x, y, t, pressed = positions[curr_move]
            if pressed:
                pyautogui.mouseDown(x=x, y=y, button='left', duration=t-t0)
            else:
                pyautogui.mouseUp(x=x, y=y, button='left', duration=t-t0)
            t0 = t  # preserve the last time
        no_of_executions += 1
        

except Exception as err:
    print('Something went wrong: ' + str(err))
    sys.exit()