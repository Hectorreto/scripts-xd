import keyboard, threading, time, pyautogui
from pynput import mouse

option = ''
start_time = 0
record = []
all_buttons = {}

def repeat_record():
    if len(record) == 0:
        return
    
    last_time = 0
    step = 0
    sub_step = 0

    while option == '3':
        if step < len(record):
            x, y, button, pressed, t = record[step]
            action = 'Pressed' if pressed else 'Released'

            if sub_step == 0:
                time.sleep((t - last_time) * 2/3)
                sub_step = 1
            elif sub_step == 1:
                pyautogui.moveTo(x, y, duration=(t - last_time) * 1/3)
                sub_step = 2
            else:
                if pressed:
                    pyautogui.mouseDown(x, y, button=button.name)
                else:
                    pyautogui.mouseUp(x, y, button=button.name)
                    
                step += 1
                last_time = t
                sub_step = 0
                print(f'{action} at {x}, {y} in {t}')
        else:
            step = 0
            last_time = 0
            

def show_instructions():
    print('################################')
    print('#                              #')
    print('#           Main Menu          #')
    print('#                              #')
    print('################################')
    print('Press 1 to start recording')
    print('Press 2 to stop recording')
    print('Press 3 to play back recorded clicks')
    print('Press 0 to exit')
    print('')


def keyboard_listener():
    global option, start_time, record, last_time, step

    while True:
        key = keyboard.read_key()
        
        if key == '1' and option != '1':
            print("Recording...")
            option = '1'
            record = []

        if key == '2' and option != '2':
            show_instructions()
            option = '2'

        if key == '3' and option != '3':
            print("Repeating clicks...")
            option = '3'
            threading.Thread(target=repeat_record).start()

        if key == '0':
            print("Exiting...")
            option = '0'
            return

def on_click(x, y, button, pressed):
    if option != '1':
        return
    
    global start_time
    action = 'pressed' if pressed else 'released'

    if len(record) == 0:
        start_time = time.time()

    all_buttons[button.name] = action
        
    print(f'{button.name} {action} at {x}, {y} in {time.time() - start_time}')
    record.append((x, y, button, pressed, time.time() - start_time))


threading.Thread(target=keyboard_listener).start()
mouse.Listener(on_click=on_click).start()
show_instructions()

# release all mouse buttons
for button in all_buttons:
    if all_buttons[button] == 'pressed':
        pyautogui.mouseUp(button=button)
