# Hand Gesture Control Interface

A real-time hand gesture recognition system built with Python and OpenCV. This interface allows users to trigger commands by moving their hands over customizable on-screen zones.

## Features

- **Real-time Gesture Detection**: Uses background subtraction to detect motion in user-defined zones.
- **Interactive UI**: Displays command zones and visual feedback directly on the camera feed.
- **Dynamic Layout Editing**: Press 'e' to enter a drag-and-drop interface to move and reposition command zones in real-time.
- **Multi-Camera Support**: Automatically detects available cameras and allows the user to select which one to use.
- **Photo Saving**: A "Take Photo" command that saves the current frame to a local `photos/` directory with a timestamp.
- **User-Friendly Calibration**: A simple, key-press-initiated process to calibrate the background for accurate motion detection.

## Requirements

- Python 3.x
- A webcam
- The packages listed in `requirements.txt`

## Setup and Installation

1.  **Clone the repository (or download the files).**

2.  **Install the required Python packages:**
    Open a terminal or command prompt in the project directory and run:
    ```bash
    pip install -r requirements.txt
    ```

## How to Use

1.  **Run the main script:**
    ```bash
    python main.py
    ```

2.  **Initial Menu:**
    - A window will appear showing your webcam feed and a menu.
    - **Press 's'**: To proceed directly to calibration.
    - **Press 'e'**: To enter **Edit Mode**.
    - **Press 'q'**: To quit the program.

3.  **Edit Mode (Optional):**
    - If you pressed 'e', you can now customize the layout.
    - **Drag and Drop**: Use your mouse to click and drag the command boxes to your desired positions.
    - **Press 's'**: To save your new layout and return to the initial menu.

4.  **Calibration:**
    - From the initial menu, press 's'.
    - You will have a 3-second countdown to get ready.
    - Keep the scene static (without your hands in it) for 3 seconds while the system learns the background.

5.  **Interact:**
    - After calibration, move your hand over a command box to start activating it.
    - A progress bar will fill up. Hold your hand steady until it's full to trigger the command.
    - **Take Photo**: If triggered, the current image will be saved in the `photos/` folder.

6.  **Exit the program:**
    - You can trigger the "Exit" command with your hand or press the **'q'** key at any time in the main detection loop.

## File Structure

- `main.py`: The main application script.
- `edit_layout.py`: A module containing the functionality for the interactive layout editor.
- `requirements.txt`: A list of Python dependencies.
- `photos/`: A directory that will be created to store saved photos.

## Recent Updates

- **`main.py`**: General updates and improvements to the main application logic.
- **`requirements.txt`**: Dependencies have been updated.
- **New Media**: Added new image files to `photos/` and a video file `高清版瑞克搖.mp4`.