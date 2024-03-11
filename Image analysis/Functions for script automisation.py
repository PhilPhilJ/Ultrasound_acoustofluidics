import numpy as np

def mean_value(frame, ratio=0.2):
    mean_values = []
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    center_col = frame.shape[1] // 2
    left_col = int(center_col - (center_col * ratio))
    right_col = int(center_col + (center_col * ratio))
    cropped_frame = np.concatenate([frame[:, :left_col], frame[:, right_col:]])
        
    mean_value = np.mean(cropped_frame)
    mean_values.append(mean_value)
    
    mean_values = np.array(mean_values)
    mean_values /= mean_values[-1]
    
    return mean_values

def end_fit(norm_intensities):
    if len(norm_intensities) < 10:
        gradient = np.diff(norm_intensities[-10:])
        mean_gradient = np.mean(gradient) 
        if mean_gradient < 0.01:
            return True
        else:
            return False
        
