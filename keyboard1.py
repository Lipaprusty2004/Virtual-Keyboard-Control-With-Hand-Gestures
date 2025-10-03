import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time
import pygame

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize pygame for sound
pygame.mixer.init()
try:
    click_sound = pygame.mixer.Sound('click.wav')
except:
    click_sound = None
    print("Warning: 'click.wav' not found. Sound will be disabled.")

# Keyboard Layout
keys = [
    ['ESC','F1','F2','F3','F4','F5','F6','F7','F8','F9','F10','F11','F12'],
    ['`','1','2','3','4','5','6','7','8','9','0','-','=','Backspace'],
    ['Tab','Q','W','E','R','T','Y','U','I','O','P','[',']','\\'],
    ['Caps','A','S','D','F','G','H','J','K','L',';','\'','Enter'],
    ['Shift','Z','X','C','V','B','N','M',',','.','/','Shift'],
    ['Space']
]

# Shift key mapping for symbols
shift_map = {
    '`':'~', '1':'!', '2':'@', '3':'#', '4':'$', '5':'%', 
    '6':'^', '7':'&', '8':'*', '9':'(', '0':')',
    '-':'_', '=':'+', '[':'{', ']':'}', '\\':'|',
    ';':':', '\'':'"', ',':'<', '.':'>', '/':'?'
}

# Draw Keyboard
def draw_keyboard(img):
    key_list = []
    start_x, start_y = 50, 100
    key_w, key_h = 70, 70
    for row_index, row in enumerate(keys):
        x_offset = 0
        for key in row:
            w = key_w
            if key in ['Tab','Caps','Shift','Backspace','Enter','Space']:
                if key == 'Tab': w *= 1.5
                elif key == 'Caps': w *= 1.8
                elif key == 'Shift': w *= 2.2
                elif key == 'Backspace': w *= 2.5
                elif key == 'Enter': w *= 2.2
                elif key == 'Space': w *= 9

            x = start_x + x_offset
            y = start_y + row_index * (key_h + 10)
            cv2.rectangle(img, (x, y), (x + int(w), y + key_h), (50, 50, 200), -1)
            cv2.putText(img, key, (x + 10, y + 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
            key_list.append((key, (x, y, int(w), key_h)))
            x_offset += int(w) + 10
    return key_list

# Detect key under finger
def get_key_from_position(x, y, key_list):
    for key, (kx, ky, kw, kh) in key_list:
        if kx < x < kx + kw and ky < y < ky + kh:
            return key
    return None

# Initialize camera
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

typed_text = ""
pressed = False
capslock = False
shift_active = False

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    key_list = draw_keyboard(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm = hand_landmarks.landmark
            index_x, index_y = int(lm[8].x * w), int(lm[8].y * h)
            thumb_x, thumb_y = int(lm[4].x * w), int(lm[4].y * h)

            cv2.circle(frame, (index_x, index_y), 12, (0, 255, 0), -1)

            distance = np.hypot(index_x - thumb_x, index_y - thumb_y)

            if distance < 40 and not pressed:
                key = get_key_from_position(index_x, index_y, key_list)
                if key:
                    if click_sound: click_sound.play()
                    print("Pressed:", key)

                    # Special keys
                    if key == 'Space':
                        typed_text += ' '
                    elif key == 'Backspace':
                        typed_text = typed_text[:-1]
                    elif key == 'Enter':
                        typed_text += '\n'
                    elif key == 'Caps':
                        capslock = not capslock
                    elif key == 'Shift':
                        shift_active = True
                    elif key == 'Tab':
                        typed_text += '    '
                    elif key == 'ESC':
                        pass
                    else:
                        char = key
                        # Handle shift for symbols
                        if shift_active and key in shift_map:
                            char = shift_map[key]
                        # Handle shift for letters
                        elif key.isalpha():
                            if capslock ^ shift_active:  # XOR logic
                                char = key.upper()
                            else:
                                char = key.lower()
                        typed_text += char
                        shift_active = False  # reset after one use

                pressed = True

            elif distance > 50:
                pressed = False

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Show typed text
    cv2.rectangle(frame, (50, 600), (1230, 680), (0, 0, 0), -1)
    for i, line in enumerate(typed_text.split("\n")[-2:]):  # show last 2 lines
        cv2.putText(frame, line, (60, 640 + i*30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 3)

    cv2.imshow("Gesture Keyboard", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
