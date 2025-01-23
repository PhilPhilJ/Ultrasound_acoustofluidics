import cv2
import numpy as np

# Load the image
image = cv2.imread('/Users/joakimpihl/Desktop/Skærmbillede 2024-02-26 kl. 14.16.15.png')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Hough Circle Transform to detect circles
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 10,
                           param1=50, param2=15, minRadius=5, maxRadius=50)

# Check if any circles were found
if circles is not None:
    # Convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")

    # Loop over all detected circles
    for (x, y, r) in circles:
        # Draw the circle on the original image
        cv2.circle(image, (x, y), r, (0, 255, 0), 2)

    # Print the total number of circles found
    print(f"Total circles found: {len(circles)}")

    # Display the image with highlighted circles
    cv2.imshow("Circles", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No circles found in the image.")