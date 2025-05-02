import cv2
import face_recognition
import pygame
import numpy as np

# Inisialisasi pygame
pygame.init()
window_size = (640, 480)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Face Recognition")

# Daftar wajah yang dikenal
known_face_encodings = []
known_face_names = []

def load_known_faces():
    known_faces = [
        {"name": "nawfal", "image_path": "wajah/nawfal.jpg"},
        {"name": "alwan", "image_path": "wajah/alwan.jpg"},
        {"name": "rasya", "image_path": "wajah/rasya.jpg"}
    ]
    
    for face in known_faces:
        image = face_recognition.load_image_file(face["image_path"])
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(face["name"])
        else:
            print(f"❌ Tidak ada wajah ditemukan di: {face['image_path']}")

# Muat wajah yang dikenal
load_known_faces()

cap = cv2.VideoCapture(0)

running = True
clock = pygame.time.Clock()

while running:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize frame untuk performa
    small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Deteksi wajah dan encoding
    face_locations = face_recognition.face_locations(rgb_small_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_face_names[index]

        # Skala balik koordinat (karena frame dikecilkan)
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Convert frame ke format pygame (RGB → Surface)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb = np.rot90(frame_rgb)  # Rotate to match pygame's orientation
    frame_surface = pygame.surfarray.make_surface(frame_rgb)
    screen.blit(frame_surface, (0, 0))
    pygame.display.update()

    # Cek event quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(120)  # Batasi ke 30 FPS

cap.release()
pygame.quit()
