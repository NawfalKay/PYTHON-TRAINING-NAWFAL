import cv2
import face_recognition

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

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # ✅ Deteksi wajah menggunakan face_recognition
    face_locations = face_recognition.face_locations(rgb_frame, model="hog")
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_face_names[index]

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
