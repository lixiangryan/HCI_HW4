# Hand Gesture Control Interface

This project is a real-time hand gesture recognition system built with Python and OpenCV. It allows users to control applications by moving their hands over predefined areas on the screen.

## Features

- **Real-time Gesture Detection**: Uses background subtraction to detect motion in specific zones.
- **Interactive UI**: Displays command zones and visual feedback directly on the camera feed.
- **Customizable Commands**: Easily configure command zones for different actions (e.g., "Take Photo", "Play Video", "Exit").
- **Calibration Process**: Includes a calibration phase to adapt to the environment's lighting and background.

## Prerequisites

- Python 3.x
- A webcam

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

2.  **Start Calibration:**
    - A window showing your webcam feed will appear.
    - Press the **'s'** key on your keyboard to begin the calibration process.

3.  **Get Ready:**
    - You will have a few seconds to prepare before calibration starts.

4.  **Calibrate:**
    - Keep the scene static (without your hands in it) for a few seconds. The system is learning the background.

5.  **Interact:**
    - After calibration is complete, you can move your hand over the command boxes (e.g., "Take Photo", "Exit") to trigger actions.
    - A progress bar will fill up as you hold your hand over a zone.
    - Once the action is triggered, the system is ready for the next command.

6.  **Exit the program:**
    - You can either trigger the "Exit" command with your hand or press the **'q'** key to quit.
