import cv2
import numpy as np
import time

class BallTracker:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.quadrants = {
            1: [(555, 11), (886, 368)],
            2: [(886, 14), (1257, 362)],
            3: [(557, 372), (887, 729)],
            4: [(878, 381), (1246, 727)]
        }
        self.ball_colors = {
            'yellow': ([20, 100, 100], [30, 255, 255]),
            'green': ([40, 50, 50], [80, 255, 255]),
            'white': ([0, 0, 200], [180, 30, 255]),
            'peach': ([0, 50, 140], [20, 150, 255])
        }
        self.events = []
        self.last_positions = {}
        self.last_detection_time = {}
        self.frame_count = 0
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        self.min_exit_time = 2.0
        self.min_entry_time = 1.0
        self.background = None
        self.overlay_text = []

    def process_frame(self, frame):
        self.frame_count += 1
        current_time = self.frame_count / self.fps

        if self.background is None:
            self.background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.background = cv2.GaussianBlur(self.background, (21, 21), 0)
            return frame

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        diff_frame = cv2.absdiff(self.background, gray_frame)
        thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
        thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        detected_balls = {color: None for color in self.ball_colors}
        
        for color, (lower, upper) in self.ball_colors.items():
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            mask = cv2.bitwise_and(mask, thresh_frame)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            max_area = 0
            best_contour = None
            for contour in contours:
                area = cv2.contourArea(contour)
                if 300 < area < 5000 and area > max_area:
                    max_area = area
                    best_contour = contour
            
            if best_contour is not None:
                x, y, w, h = cv2.boundingRect(best_contour)
                center = (x + w // 2, y + h // 2)
                
                detected_balls[color] = center
                vis_color = self.get_vis_color(color)
                cv2.circle(frame, center, max(w, h) // 2, vis_color, 2)
                cv2.putText(frame, color, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, vis_color, 2)

        self.update_ball_positions(detected_balls, current_time)
        
        for text, start_time in self.overlay_text:
            if current_time - start_time < 3:  
                cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            else:
                self.overlay_text.remove((text, start_time))
        
        return frame

    def update_ball_positions(self, detected_balls, current_time):
        for color, position in detected_balls.items():
            if position:
                current_quadrant = self.get_quadrant(position)
                if color not in self.last_positions:
                    if current_quadrant:
                        self.last_positions[color] = current_quadrant
                        event = f"{current_time:.0f}, {color}, entry, quadrant {current_quadrant}"
                        self.events.append(event)
                        self.overlay_text.append((f"{color.capitalize()} Entry Q{current_quadrant} - {current_time:.0f}s", current_time))
                        self.last_detection_time[color] = current_time
                elif self.last_positions[color] != current_quadrant:
                    time_since_last_detection = current_time - self.last_detection_time.get(color, 0)
                    if time_since_last_detection > self.min_entry_time:
                        if self.last_positions[color]:
                            event = f"{current_time:.0f}, {color}, exit, quadrant {self.last_positions[color]}"
                            self.events.append(event)
                            self.overlay_text.append((f"{color.capitalize()} Exit Q{self.last_positions[color]} - {current_time:.0f}s", current_time))
                        event = f"{current_time:.0f}, {color}, entry, quadrant {current_quadrant}"
                        self.events.append(event)
                        self.overlay_text.append((f"{color.capitalize()} Entry Q{current_quadrant} - {current_time:.0f}s", current_time))
                        self.last_positions[color] = current_quadrant
                self.last_detection_time[color] = current_time
            elif color in self.last_positions:
                time_since_last_detection = current_time - self.last_detection_time.get(color, 0)
                if time_since_last_detection > self.min_exit_time:
                    event = f"{current_time:.0f}, {color}, exit, quadrant {self.last_positions[color]}"
                    self.events.append(event)
                    self.overlay_text.append((f"{color.capitalize()} Exit Q{self.last_positions[color]} - {current_time:.0f}s", current_time))
                    del self.last_positions[color]
                    del self.last_detection_time[color]

    def get_quadrant(self, position):
        for q_num, (top_left, bottom_right) in self.quadrants.items():
            if top_left[0] < position[0] < bottom_right[0] and top_left[1] < position[1] < bottom_right[1]:
                return q_num
        return None

    def get_vis_color(self, color):
        color_map = {
            'yellow': (0, 255, 255),
            'green': (0, 255, 0),
            'white': (255, 255, 255),
            'peach': (180, 180, 255)
        }
        return color_map.get(color, (0, 0, 0))

    def run(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter('output.mp4', fourcc, self.fps, (int(self.cap.get(3)), int(self.cap.get(4))))

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            processed_frame = self.process_frame(frame)
            out.write(processed_frame)

        self.cap.release()
        out.release()

        with open('events.txt', 'w') as f:
            for event in self.events:
                f.write(event + '\n')

if __name__ == "__main__":
    tracker = BallTracker("AI Assignment video.mp4")
    start_time = time.time()
    tracker.run()
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time} seconds")