# Code Explanation

#### `BallTracker` Class Initialization (`__init__` method)

1. **`__init__(self, video_path)`**:
   - Initializes the `BallTracker` class with a video path.
   - Sets up video capture (`self.cap`) using `cv2.VideoCapture`.
   - Defines `self.quadrants` with coordinates for four numbered quadrants.
   - Defines `self.ball_colors` with HSV color ranges for different ball colors (`yellow`, `green`, `white`, `peach`).
   - Initializes various tracking variables (`self.events`, `self.last_positions`, etc.).
   - Retrieves frames per second (`self.fps`) from the video.

#### `process_frame` Method

2. **`process_frame(self, frame)`**:
   - Processes each frame of the video to detect and track balls.
   - Converts the frame to grayscale and applies Gaussian blur (`cv2.GaussianBlur`) to reduce noise.
   - Computes the difference (`diff_frame`) between the current frame and the background frame (`self.background`).
   - Applies thresholding (`cv2.threshold`) to create a binary image (`thresh_frame`) highlighting areas of significant change.
   - Converts the frame to HSV color space (`cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)`) for color-based ball detection.
   - Iterates through each ball color defined in `self.ball_colors`:
     - Creates a mask using `cv2.inRange` to isolate pixels within the color range.
     - Applies the mask to `thresh_frame` to filter out non-ball areas.
     - Finds contours (`cv2.findContours`) in the masked image to identify potential ball locations.
     - Selects the contour with the largest area within specified bounds (`300 < area < 5000`) as the detected ball.
     - Draws a circle around the detected ball and adds a text label indicating its color (`cv2.circle`, `cv2.putText`).

#### `update_ball_positions` Method

3. **`update_ball_positions(self, detected_balls, current_time)`**:
   - Updates the positions of detected balls (`detected_balls`) and records entry/exit events based on their movements.
   - Determines the current quadrant (`self.get_quadrant`) for each detected ball position.
   - Tracks the time since the last detection and records entry or exit events (`event`) accordingly.
   - Updates `self.last_positions`, `self.last_detection_time`, and `self.events` with each detected event.

#### `run` Method

4. **`run(self)`**:
   - Main method to process each frame of the video and generate outputs.
   - Initializes a video writer (`cv2.VideoWriter`) to create an output video (`out.mp4`) with ball tracking overlays.
   - Loops through each frame of the input video (`self.cap.isOpened()`):
     - Reads the next frame (`self.cap.read()`).
     - Processes the frame (`self.process_frame`) to detect and track balls, updating the output video.
   - Releases the video capture (`self.cap.release()`) and output video (`out.release()`).
   - Writes the recorded events (`self.events`) to a text file (`events.txt`) with the format `Time, Ball Colour, Event Type (Entry or Exit), Quadrant Number`.

### Summary

This code utilizes Computer Vision techniques to track colored balls across predefined quadrants in a video. It employs motion detection, color segmentation in HSV space, contour analysis, and event tracking to record entry and exit events of balls in each quadrant. The `BallTracker` class provides methods to process video frames, update ball positions, and generate visual and textual outputs summarizing ball movements and events.
