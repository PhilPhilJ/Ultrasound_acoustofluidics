import cv2
import os
def video_to_frames(video_path, output_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    # Check if video file is opened successfully
    if not video.isOpened():
        print("Error opening video file")
        return
    
    # Initialize frame count
    frame_count = 0
    
    # Read until video is completed
    while video.isOpened():
        # Read a single frame from the video
        ret, frame = video.read()
        
        # Break the loop if no frame is read
        if not ret:
            break
        
        # Save the frame as an image
        frame_path = f"{output_path}/frame_{frame_count}.png"
        cv2.imwrite(frame_path, frame)
        
        # Increment frame count
        frame_count += 1
    
    # Release the video file and close all windows
    video.release()
    cv2.destroyAllWindows()

def frames_to_video(frames_path, output_path, fps=20):
    # Get the list of image frames
    frames = [f for f in os.listdir(frames_path) if f.endswith('.tif')]
    
    # Sort frames based on the numerical part of the filename
    frames.sort(key=lambda f: int(''.join(filter(str.isdigit, f)).lstrip('0')))
    
    # Get the dimensions of the first frame
    frame = cv2.imread(os.path.join(frames_path, frames[0]))
    height, width, _ = frame.shape
    
    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Write each frame to the video
    for frame_name in frames:
        frame_path = os.path.join(frames_path, frame_name)
        frame = cv2.imread(frame_path)
        video.write(frame)
    
    # Release the video writer
    video.release()

# Example usage
video_path = "/Users/joakimpihl/Desktop/Uden navn.mov"
output_path = "/Users/joakimpihl/Desktop/Vid.mp4"
frames_path = "/Users/joakimpihl/Desktop/Vid_n2/"
#video_to_frames(video_path, frames_path)
frames_to_video(frames_path, output_path)

