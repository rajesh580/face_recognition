import cv2
import face_recognition
import numpy as np
import os
import threading

frame = None

def load_known_faces(known_faces_dir):
    known_face_encodings = []
    known_face_names = []

    for file_name in os.listdir(known_faces_dir):
        file_path = os.path.join(known_faces_dir, file_name)
        if os.path.isfile(file_path):
            try:
                image = face_recognition.load_image_file(file_path)
                encodings = face_recognition.face_encodings(image)
                if encodings:  
                    known_face_encodings.append(encodings[0])
                    known_face_names.append(os.path.splitext(file_name)[0])
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    return known_face_encodings, known_face_names

KNOWN_FACES_DIR = "known_faces"
if not os.path.exists(KNOWN_FACES_DIR):
    print(f"Directory {KNOWN_FACES_DIR} does not exist.")
    exit(1)

known_face_encodings, known_face_names = load_known_faces(KNOWN_FACES_DIR)

video_capture = cv2.VideoCapture(0)
if not video_capture.isOpened():
    print("Error: Cannot access webcam.")
    exit(1)

video_capture.set(cv2.CAP_PROP_FPS, 30)

frame_count = 0
process_every_n_frames = 2  


def capture_frames():
    global frame
    while True:
        ret, frame = video_capture.read()
        if not ret or frame is None:
            print("Failed to capture frame from webcam.")
            break

def process_frames():
    global frame
    while True:
        if frame is None:
            continue

        global frame_count
        if frame_count % process_every_n_frames == 0:
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
  
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"

                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                if matches and len(face_distances) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1)

        frame_count += 1

        cv2.imshow("Video", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

threading.Thread(target=capture_frames, daemon=True).start()
process_frames()

video_capture.release()
cv2.destroyAllWindows()