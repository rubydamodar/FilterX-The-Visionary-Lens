import cv2
import numpy as np

# Global variables to manage threshold
threshold_value = 100
current_filter = 'X-ray'  # Default filter

# Function to simulate X-ray effect
def simulate_xray_effect(frame, threshold_value):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, xray_frame = cv2.threshold(gray_frame, threshold_value, 255, cv2.THRESH_BINARY_INV)
    xray_frame = cv2.GaussianBlur(xray_frame, (5, 5), 0)
    return xray_frame

# Function to apply edge detection
def apply_edge_detection(frame):
    return cv2.Canny(frame, 100, 200)

# Function to apply color inversion
def invert_colors(frame):
    return cv2.bitwise_not(frame)

# Function to apply Gaussian blur
def apply_gaussian_blur(frame, kernel_size=5):
    return cv2.GaussianBlur(frame, (kernel_size, kernel_size), 0)

# Function to apply sepia effect
def apply_sepia(frame):
    sepia_filter = np.array([[0.272, 0.534, 0.131],
                              [0.349, 0.686, 0.168],
                              [0.393, 0.769, 0.189]])
    return cv2.transform(frame, sepia_filter)

# Function to apply cartoon effect
def apply_cartoon(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY, 9, 9)
    color = cv2.bilateralFilter(frame, 9, 300, 300)
    cartoon_frame = cv2.bitwise_and(color, color, mask=edges)
    return cartoon_frame

# Function to apply posterize effect
def apply_posterize(frame, levels=4):
    return (frame // (256 // levels)) * (256 // levels)

# Function to apply median blur
def apply_median_blur(frame, kernel_size=5):
    return cv2.medianBlur(frame, kernel_size)

# Function to apply motion blur
def apply_motion_blur(frame, size=15):
    kernel = np.zeros((size, size))
    kernel[int((size - 1) / 2), :] = np.ones(size)
    kernel /= size
    return cv2.filter2D(frame, -1, kernel)

# Function to apply bilateral filter
def apply_bilateral_filter(frame, diameter=9, sigma_color=75, sigma_space=75):
    return cv2.bilateralFilter(frame, diameter, sigma_color, sigma_space)

# Function to apply night vision effect
def apply_night_vision(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = hsv[:, :, 1] * 2  # Saturation
    hsv[:, :, 2] = hsv[:, :, 2] * 1.5  # Value
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Function to apply emboss effect
def apply_emboss(frame):
    kernel = np.array([[0, -1, -1],
                       [1, 0, -1],
                       [1, 1, 0]])
    return cv2.filter2D(frame, -1, kernel)

# Function to apply sketch effect
def apply_sketch(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    inverted = cv2.bitwise_not(gray)
    blurred = cv2.GaussianBlur(inverted, (21, 21), 0)
    inverted_blurred = cv2.bitwise_not(blurred)
    return cv2.divide(gray, inverted_blurred, scale=256)

# Function to apply HSV filter
def apply_hsv(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# Function to apply Lab color space
def apply_lab(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2Lab)

# Function to apply random color filter (Red, Green, Blue)
def apply_color_filter(frame, color='red'):
    if color == 'red':
        frame[:, :, 1] = 0  # Zero out green channel
        frame[:, :, 2] = 0  # Zero out blue channel
    elif color == 'green':
        frame[:, :, 0] = 0  # Zero out red channel
        frame[:, :, 2] = 0  # Zero out blue channel
    elif color == 'blue':
        frame[:, :, 0] = 0  # Zero out red channel
        frame[:, :, 1] = 0  # Zero out green channel
    return frame

# Function to apply the selected filter
def apply_filter(frame):
    if current_filter == 'X-ray':
        return simulate_xray_effect(frame, threshold_value)
    elif current_filter == 'Edge Detection':
        return apply_edge_detection(frame)
    elif current_filter == 'Invert Colors':
        return invert_colors(frame)
    elif current_filter == 'Gaussian Blur':
        return apply_gaussian_blur(frame, kernel_size=15)
    elif current_filter == 'Sepia':
        return apply_sepia(frame)
    elif current_filter == 'Cartoon':
        return apply_cartoon(frame)
    elif current_filter == 'Posterize':
        return apply_posterize(frame)
    elif current_filter == 'Median Blur':
        return apply_median_blur(frame)
    elif current_filter == 'Motion Blur':
        return apply_motion_blur(frame)
    elif current_filter == 'Bilateral Filter':
        return apply_bilateral_filter(frame)
    elif current_filter == 'Night Vision':
        return apply_night_vision(frame)
    elif current_filter == 'Emboss':
        return apply_emboss(frame)
    elif current_filter == 'Sketch':
        return apply_sketch(frame)
    elif current_filter == 'HSV':
        return apply_hsv(frame)
    elif current_filter == 'Lab':
        return apply_lab(frame)
    elif current_filter == 'Red Filter':
        return apply_color_filter(frame, 'red')
    elif current_filter == 'Green Filter':
        return apply_color_filter(frame, 'green')
    elif current_filter == 'Blue Filter':
        return apply_color_filter(frame, 'blue')
    else:
        return frame

# Function to show instructions on the frame
def display_instructions(frame):
    instructions = (
        "Press 'c' to capture image, 'UP' and 'DOWN' to adjust threshold, "
        "'f' to change filter, 'q' to quit."
    )
    cv2.putText(frame, instructions, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Threshold: {threshold_value}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, f"Current Filter: {current_filter}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

# Initialize the webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Apply the selected filter
    filtered_frame = apply_filter(frame)

    # Display instructions
    display_instructions(frame)

    # Display the original frame and the filtered frame
    cv2.imshow('Original Frame', frame)
    cv2.imshow('Filtered Frame', filtered_frame)

    key = cv2.waitKey(1) & 0xFF
    
    # Break the loop on 'q' key press
    if key == ord('q'):
        break
    
    # Capture image on 'c' key press
    elif key == ord('c'):
        cv2.imwrite('captured_image.png', filtered_frame)
        print("Image captured and saved as 'captured_image.png'")

    # Adjust threshold using UP and DOWN arrow keys
    elif key == 2490368:  # Up arrow key
        threshold_value = min(threshold_value + 5, 255)
        print(f"Threshold increased to: {threshold_value}")
    elif key == 2621440:  # Down arrow key
        threshold_value = max(threshold_value - 5, 0)
        print(f"Threshold decreased to: {threshold_value}")
    
    # Change filter
    # Change filter using 'f' key press
    elif key == ord('f'):
        filters = ['X-ray', 'Edge Detection', 'Invert Colors', 'Gaussian Blur', 'Sepia',
                   'Cartoon', 'Posterize', 'Median Blur', 'Motion Blur', 'Bilateral Filter',
                   'Night Vision', 'Emboss', 'Sketch', 'HSV', 'Lab', 'Red Filter', 
                   'Green Filter', 'Blue Filter']

        current_filter = filters[(filters.index(current_filter) + 1) % len(filters)]
        print(f"Filter changed to: {current_filter}")

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
