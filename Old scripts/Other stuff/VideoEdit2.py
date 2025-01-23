import cv2
import numpy as np

def process_video(input_path, output_path):
    vid = cv2.VideoCapture(input_path)
    total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    FPS = vid.get(cv2.CAP_PROP_FPS)
    output_size = (int(3387 - 1104), height)

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Use 'MJPG' codec
    out = cv2.VideoWriter(output_path, fourcc, FPS, output_size)

    # Create a background subtractor
    background_subtractor = cv2.createBackgroundSubtractorMOG2()

    for i in range(total_frames):
        ret, frame = vid.read()
        if not ret:
            break

        # Apply background subtraction
        fg_mask = background_subtractor.apply(frame)

        # Remove the background
        frame_no_bg = cv2.bitwise_and(frame, frame, mask=fg_mask)

        # Convert to grayscale
        frame_no_bg_gray = cv2.cvtColor(frame_no_bg, cv2.COLOR_BGR2GRAY)

        # Apply adaptive thresholding
        frame_no_bg_binary = cv2.adaptiveThreshold(frame_no_bg_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 10)

        # Crop the width
        frame_no_bg_binary_cropped = frame_no_bg_binary[:, 1104:3387]

        # Write the processed frame
        out.write(frame_no_bg_binary_cropped)
        print(f"Processed frame {i}/{total_frames}")

    # Release resources
    vid.release()
    out.release()
    cv2.destroyAllWindows()

# Example usage:
input_path = '/Users/joakimpihl/Desktop/Focus sweep 2/run8.mp4'
output_path = '/Users/joakimpihl/Desktop/run8_background_removed_cropped.mp4'

process_video(input_path, output_path)
