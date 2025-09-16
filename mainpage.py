import tkinter as tk
from tkinter import ttk
import LoginPage
import ShowAttendance
import get_faces_from_camera_tkinter as get_face

class ModernAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern GUI System")
        self.root.geometry("900x600")
        self.root.configure(bg='white')

        self.create_widgets()

    def logout(self):
        self.root.destroy()
        LoginPage.main()

    def face(self):
        self.root.destroy()
        get_face.main()

    def attend(self):
        self.root.destroy()
        ShowAttendance.main()

    def create_widgets(self):
        # Header
        header_label = tk.Label(self.root, text="Welcome to the Modern Attendance System", fg="white", bg="#2c3e50", font=("Segoe UI", 16, "bold"), height=2)
        header_label.pack(fill="x", side="top")

        logout_button = ttk.Button(self.root, text="Logout", command=self.logout)
        logout_button.pack(side="right", padx=10, pady=10,anchor='ne',)

        # Footer
        footer_label = tk.Label(self.root, text="© 2025 My Attendance System", fg="white", bg="#2c3e50", font=("Segoe UI", 10), height=2)
        footer_label.pack(fill="x", side="bottom")

        # Left side text as labels
        text_lines = [
            "This system is designed to provide a modern interface for tracking attendance using facial recognition.",
            "",
            "Features:",
            "- Real-time face detection and recognition with Dlib and OpenCV.",
            "- Live camera feed integrated into the GUI.",
            "- Automatic attendance marking and logging.",
            "- Data persistence using SQLite.",
            "- Detailed records with timestamps and face data.",
            "- Secure login and logout flow.",
            "- Admin dashboard for management.",
            "- Exportable CSV attendance reports.",
            "- User-friendly interface with responsive design.",
            "- Designed for educational institutions, offices, and events.",
            "",
        ]

        for i, line in enumerate(text_lines):
            tk.Label(self.root, text=line, bg='#ffffff', font=("Segoe UI", 12), anchor='w', justify='left').place(x=30, y=80 + i*25)

        # Style configuration for buttons
        style = ttk.Style()
        style.configure('TButton', font=("Segoe UI", 14), padding=10)

        # Right side buttons with larger size and border effect
        btn1 = tk.Button(self.root, text="Add Face", font=("Segoe UI", 14), bg="#3498db", fg="white", relief="raised", bd=3, width=22, height=2,command=self.face)
        btn1.place(x=630, y=250)

        btn2 = tk.Button(self.root, text="View Attendance Records", font=("Segoe UI", 14), bg="#2ecc71", fg="white", relief="raised", bd=3, width=22, height=2,command=self.attend)
        btn2.place(x=630, y=330)

def main():
    root = tk.Tk()
    app = ModernAttendanceApp(root)
    root.mainloop()

# To run the GUI directly
if __name__ == "__main__":
    main()
