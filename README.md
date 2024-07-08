# BallTracker: Ball Tracking with Computer Vision

## Project Description

This project implements a program using Computer Vision to track the movement of colored balls across various quadrants in a video. The program detects when each ball enters and exits numbered quadrants, recording these events along with timestamps.

### Task
- The program should :
  - Track colored balls (yellow, green, white, peach) moving across predefined quadrants.
  - Record entry and exit events for each ball in the format: Time, Quadrant Number, Ball Colour, Type (Entry or Exit).

### Video to Process
- [Download Video](https://drive.google.com/file/d/1goI3aHVE29Gko9lpTzgi_g3CZZPjJq8w/view?usp=sharing)

### Expected Output
- Processed Video: [Output](https://github.com/Transcendental-Programmer/BallTracker-CV-Ball-Tracking-with-Computer-Vision-/blob/main/output.mp4)
  - Shows ball tracking with color overlays.
- Text File: [events.txt](https://github.com/Transcendental-Programmer/BallTracker-CV-Ball-Tracking-with-Computer-Vision-/blob/main/events.txt)
  - Contains records of all events in the specified format.

### Code Explanation

The code implements a `BallTracker` class that processes each frame of the video using Computer Vision techniques:

- **Initialization (`__init__` method)**:
  - Sets up video capture, defines quadrants and ball colors, initializes tracking variables, and retrieves FPS.

- **`process_frame` method**:
  - Processes each frame to detect balls using motion and color segmentation techniques.
  - Identifies balls based on predefined color ranges and updates the frame with overlays and text labels.

- **`update_ball_positions` method**:
  - Updates the positions of detected balls and records entry/exit events based on their movements within quadrants.

- **`run` method**:
  - Main method that processes each frame of the video, writes the processed video with overlays (`output.mp4`), and records events to `events.txt`.

### Instructions for Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Transcendental-Programmer/BallTracker-CV-Ball-Tracking-with-Computer-Vision-.git
   cd BallTracker-CV-Ball-Tracking-with-Computer-Vision-
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the program:
   ```bash
   python main.py
   ```

4. View the processed video (`output.mp4`) and event records (`events.txt`) generated after the program execution.


