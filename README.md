# Face Recognition

This repository contains an optimized Python script for real-time face recognition using OpenCV and the `face_recognition` library. The script is designed for improved performance and can process frames efficiently by leveraging multithreading, frame resizing, and selective frame processing.

## Features
- Real-time face detection and recognition.
- Optimized for increased frames per second (FPS):
  - Processes every nth frame.
  - Scales down frames for faster computation.
  - Uses multithreading for capturing and processing frames.
- Displays recognized faces with bounding boxes and labels.

## Prerequisites
Ensure you have the following installed:

- Python 3.7 or later
- Required libraries:
  ```bash
  pip install face_recognition opencv-python numpy
  ```
- Webcam or camera device

# How to Use

1. **Prepare Known Faces**:
   - Create a folder named `known_faces` in the same directory as the script.
   - Add images of people you want to recognize. Ensure each image is named after the person (e.g., `john_doe.jpg`).

2. **Run the Script**:
   - Execute the script:
     ```bash
     python face_recognition.py
     ```
   - Press `q` to quit the application.

3. **View Recognized Faces**:
   - The application will display a live video feed with recognized faces labeled and unknown faces marked as "Unknown."

## Optimization Techniques Used
- **Frame Resizing**: Reduces the size of frames by 75% for faster face detection.
- **Frame Skipping**: Processes every second frame to lower computational load.
- **Multithreading**: Separates frame capturing and processing into independent threads for real-time efficiency.
- **Preloaded Encodings**: Avoids recalculating known face encodings.

## Example Directory Structure
```
project_folder/
├── known_faces/
│   ├── john_doe.jpg
│   ├── jane_doe.jpg
├── face_recognition.py
```

## Customization
- **Frame Skipping**:
  - Adjust the `process_every_n_frames` variable to process fewer or more frames:
    ```python
    process_every_n_frames = 2
    ```
- **Tolerance**:
  - Modify the tolerance for face matching (lower values are stricter):
    ```python
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
    ```
