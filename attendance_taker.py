import dlib
import numpy as np
import cv2
import os
import pandas as pd
import time
import logging
import sqlite3
import datetime
import tkinter as tk
from PIL import Image, ImageTk
import LoginPage

# Initialize Dlib face detector
detector = dlib.get_frontal_face_detector()

# Load shape predictor and face recognition ResNet model
predictor = dlib.shape_predictor('E:\\python-venv\\Face-Recognition-Based-Attendance-System-main\\data\\data_dlib\\shape_predictor_68_face_landmarks.dat')
face_reco_model = dlib.face_recognition_model_v1("E:\\python-venv\\Face-Recognition-Based-Attendance-System-main\\data\\data_dlib\\dlib_face_recognition_resnet_model_v1.dat")

# Ensure the attendance table exists
conn = sqlite3.connect("E:\\python-venv\\attendance.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        name TEXT,
        time TEXT,
        date DATE
    )
""")
conn.commit()
conn.close()

class FaceRecognizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Live Face Recognition Attendance")
        self.root.geometry("1000x600")
        self.root.configure(bg="white")

        self.main_frame = tk.Frame(self.root, bg="white", bd=2)
        self.main_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        self.video_label = tk.Label(self.main_frame, bg="white")
        self.video_label.grid(row=0, column=0, sticky="nsew")

        self.info_frame = tk.Frame(self.main_frame, bg="#e6f0fa", width=250)
        self.info_frame.grid(row=0, column=1, padx=20, sticky="n")
        self.info_frame.grid_propagate(False)

        label_style = {"font": ("Arial", 14), "bg": "#e6f0fa", "fg": "#003366"}

        self.label_fps = tk.Label(self.info_frame, text="FPS: 0", **label_style)
        self.label_fps.pack(pady=5)

        self.label_frame = tk.Label(self.info_frame, text="Frame: 0", **label_style)
        self.label_frame.pack(pady=5)

        self.label_faces = tk.Label(self.info_frame, text="Faces: 0", **label_style)
        self.label_faces.pack(pady=5)

        self.label_face1 = tk.Label(self.info_frame, text="Face 1: Unknown", **label_style)
        self.label_face1.pack(pady=5)

        self.label_face2 = tk.Label(self.info_frame, text="Face 2: Unknown", **label_style)
        self.label_face2.pack(pady=5)

        self.label_attendance = tk.Label(
            self.info_frame,
            text="Attendance: -",
            font=("Arial", 14),
            bg="#e6f0fa",
            fg="#007acc",
            wraplength=200,
            justify="left"
        )
        self.label_attendance.pack(pady=10)

        self.exit_button = tk.Button(self.info_frame, text="Back to Login", font=("Arial", 12), bg="#0059b3", fg="white", command=self.back_to_login)
        self.exit_button.pack(pady=20)

        self.quit_button = tk.Button(self.info_frame, text="Exit", font=("Arial", 12), bg="#808080", fg="white", command=self.on_quit)
        self.quit_button.pack(pady=10)

        self.root.bind('<Escape>', lambda e: self.on_quit())

        self.font = cv2.FONT_ITALIC
        self.frame_time = 0
        self.frame_start_time = time.time()
        self.fps = 0
        self.fps_show = 0
        self.start_time = time.time()

        self.frame_cnt = 0
        self.face_features_known_list = []
        self.face_name_known_list = []
        self.current_frame_face_name_list = []
        self.attendance_set = set()
        self.recognized_faces_cache = {}
        self.after_job = None

    def on_quit(self):
        if self.after_job:
            self.root.after_cancel(self.after_job)
        self.cap.release()
        self.root.destroy()

    def back_to_login(self):
        if self.after_job:
            self.root.after_cancel(self.after_job)
        self.cap.release()
        self.root.destroy()
        LoginPage.main()

    def get_face_database(self):
        path = "E:\\python-venv\\Face-Recognition-Based-Attendance-System-main\\data\\features_all.csv"
        if os.path.exists(path):
            df = pd.read_csv(path, header=None)
            for i in range(df.shape[0]):
                self.face_name_known_list.append(df.iloc[i][0])
                self.face_features_known_list.append([float(x) if x != '' else 0.0 for x in df.iloc[i][1:]])
            return 1
        return 0

    def return_euclidean_distance(self, f1, f2):
        return np.linalg.norm(np.array(f1) - np.array(f2))

    def attendance(self, name):
        conn = sqlite3.connect("E:\\python-venv\\attendance.db")
        cursor = conn.cursor()
        now = datetime.datetime.now()
        date_str = now.strftime('%Y-%m-%d')
        time_str = now.strftime('%H:%M:%S')

        cursor.execute("""
            SELECT time FROM attendance 
            WHERE name = ? AND date = ? 
            ORDER BY time DESC LIMIT 1
        """, (name, date_str))
        result = cursor.fetchone()

        should_mark_attendance = False
        if result:
            last_time_str = result[0]
            last_time = datetime.datetime.strptime(f"{date_str} {last_time_str}", "%Y-%m-%d %H:%M:%S")
            time_diff = (now - last_time).total_seconds()
            if time_diff >= 300:
                should_mark_attendance = True
        else:
            should_mark_attendance = True

        if should_mark_attendance:
            cursor.execute("INSERT INTO attendance (name, time, date) VALUES (?, ?, ?)", (name, time_str, date_str))
            conn.commit()
            self.label_attendance.config(text=f"Attendance: {name} at {time_str}")
        else:
            self.label_attendance.config(text=f"Attendance: {name} already marked recently")

        conn.close()

    def update_fps(self):
        now = time.time()
        if str(self.start_time).split(".")[0] != str(now).split(".")[0]:
            self.fps_show = self.fps
        self.start_time = now
        self.frame_time = now - self.frame_start_time
        self.fps = 1.0 / self.frame_time if self.frame_time > 0 else 0
        self.frame_start_time = now

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.resize(frame, (640, 480))
        self.frame_cnt += 1
        self.update_fps()
        self.current_frame_face_name_list = []
        faces = detector(frame, 0)

        if self.frame_cnt % 4 == 0:
            self.recognized_faces_cache.clear()
            for k, d in enumerate(faces):
                shape = predictor(frame, d)
                face_descriptor = face_reco_model.compute_face_descriptor(frame, shape)
                name = "Unknown"
                min_dist = 0.4
                for i, known_feature in enumerate(self.face_features_known_list):
                    dist = self.return_euclidean_distance(face_descriptor, known_feature)
                    if dist < min_dist:
                        min_dist = dist
                        name = self.face_name_known_list[i]
                if name != "Unknown":
                    self.attendance(name)
                self.recognized_faces_cache[k] = name

        for k, d in enumerate(faces):
            name = self.recognized_faces_cache.get(k, "Unknown")
            self.current_frame_face_name_list.append(name)
            frame = cv2.rectangle(frame, (d.left(), d.top()), (d.right(), d.bottom()), (255, 255, 255), 2)
            frame = cv2.putText(frame, name, (d.left(), d.top() - 10), self.font, 0.6, (255,255,255), 1)

        self.label_fps.config(text=f"FPS: {round(self.fps_show, 2)}")
        self.label_frame.config(text=f"Frame: {self.frame_cnt}")
        self.label_faces.config(text=f"Faces: {len(faces)}")
        self.label_face1.config(text=f"Face 1: {self.current_frame_face_name_list[0] if len(self.current_frame_face_name_list) > 0 else 'Unknown'}")
        self.label_face2.config(text=f"Face 2: {self.current_frame_face_name_list[1] if len(self.current_frame_face_name_list) > 1 else 'Unknown'}")

        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)
        self.after_job = self.root.after(10, self.update_frame)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        self.get_face_database()
        self.update_frame()
        self.root.mainloop()
        self.cap.release()

def main():
    logging.basicConfig(level=logging.ERROR)
    app = FaceRecognizer()
    app.run()

if __name__ == '__main__':
    main()
