<img width="1920" height="1200" alt="hello github" src="https://github.com/user-attachments/assets/daf5d3b5-bc15-46bd-aa15-5ae2d2f1413b" />🖐️ Gesture Controlled On-Screen Keyboard

This project is a virtual on-screen keyboard controlled using hand gestures with OpenCV, MediaPipe, and Pygame.
Users can type words, numbers, and special characters by performing finger gestures instead of using a physical keyboard.

✨ Features

🎯 Hand gesture detection using MediaPipe

⌨️ Full keyboard layout (letters, numbers, symbols, space, backspace, enter, shift, capslock)

🔠 CapsLock & Shift support (for uppercase & symbols like ! @ #)

🎵 Sound feedback when a key is pressed (click.wav)

📝 Typed text displayed live on screen under the keyboard

↩️ Backspace deletes characters, Enter creates a new line

⚡ Real-time typing experience with finger-tap gesture

🛠️ Tech Stack

Python 3.9+

OpenCV → For camera feed & visualization

MediaPipe → Hand landmark detection

Pygame → Sound feedback

NumPy → Distance calculations

📂 Installation

Clone the repository:

git clone https://github.com/yourusername/gesture-keyboard.git
cd gesture-keyboard


Install dependencies:

pip install opencv-python mediapipe pygame numpy


(Optional) Add a click.wav sound file in the same folder for key press feedback.

▶️ Usage

Run the app:

python app.py


Bring your index finger close to your thumb (like a click gesture) over a key to press it.

Press Space, Backspace, Enter, CapsLock, Shift just like a real keyboard.

The typed text will appear below the keyboard in the same window.

📸 Demo Screenshot

## 📸 Demo Screenshot

![Gesture Keyboard Screenshot](screenshot.png)

🚀 Future Improvements

Highlight pressed keys visually

Add predictive text suggestions

Multi-hand support for faster typing

👩‍💻 Author

Developed by Lipa Prusty ✨
