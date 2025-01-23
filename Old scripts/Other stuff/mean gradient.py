import pandas as pd
import numpy as np

def calculate_mean_gradient(file_path):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    df = df.iloc[:, 2]  # Select only the third column (Normalized intensity)

    # Extract the last 10-20 points
    last_points = df[-70:-60]

    # Calculate the gradients
    gradients = np.diff(last_points)


    # Calculate the mean gradient
    mean_gradient = np.mean(gradients)

    return mean_gradient

# Replace 'file_path' with the actual path to your CSV file
gradients = []

for run in range(0, 405):
    file_path = f'/Users/joakimpihl/Desktop/DTU/Bachelor/7. Semester/Bachelorprojekt/Results/GaussOnNormal/I_norm/I_norm run {run}.csv'
    mean_gradient = calculate_mean_gradient(file_path)
    gradients.append(mean_gradient)



print(f"The mean gradient of the last 10-20 points is: {np.mean(np.abs(gradients)),2}")