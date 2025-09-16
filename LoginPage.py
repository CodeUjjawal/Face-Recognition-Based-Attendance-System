import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import attendance_taker
import mainpage


class LoginApp:
    VALID_USERNAME = "admin"
    VALID_PASSWORD = "password"

    def __init__(self, root):
        self.root = root
        self.root.title("Attendance System using Face Recognition")
        self.root.state("normal")
        self.root.configure(bg="white")

        self.root.bind('<Escape>', lambda e: root.destroy())

        self.setup_ui()

    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg="white")
        main_frame.pack(fill="both", expand=True)

        self.setup_left_frame(main_frame)
        self.setup_right_frame(main_frame)

    def setup_left_frame(self, parent):
        left_frame = tk.Frame(parent, bg="white")
        left_frame.pack(side="left", fill="both", expand=True)

        img = Image.open("school_bus.jpg")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        img = img.resize((int(screen_width * 0.45), screen_height), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(img)

        img_label = tk.Label(left_frame, image=self.bg_image)
        img_label.pack(fill="both", expand=True)

    def setup_right_frame(self, parent):
        right_frame = tk.Frame(parent, bg="white", padx=50)
        right_frame.pack(side="right", fill="both", expand=True)

        title_label = tk.Label(right_frame, text="Attendance System using Face Recognition",
                               font=("Helvetica", 20, "bold"), fg="#003366", bg="white")
        title_label.pack(pady=(40, 10))

        login_label = tk.Label(right_frame, text="Login Page",
                               font=("Helvetica", 16, "bold"), fg="#0055aa", bg="white")
        login_label.pack(pady=(0, 30))

        login_frame = tk.Frame(right_frame, bg="#e8f0fe", bd=2, relief="groove", padx=30, pady=20)
        login_frame.pack()

        tk.Label(login_frame, text="Login", font=("Helvetica", 18, "bold"),
                 bg="#e8f0fe", fg="#003366").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        tk.Label(login_frame, text="Username", font=("Helvetica", 12),
                 bg="#e8f0fe", fg="#003366").grid(row=1, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(login_frame, width=30, font=("Helvetica", 12))
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(login_frame, text="Password", font=("Helvetica", 12),
                 bg="#e8f0fe", fg="#003366").grid(row=2, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(login_frame, show="*", width=30, font=("Helvetica", 12))
        self.password_entry.grid(row=2, column=1, pady=5)

        button_frame = tk.Frame(login_frame, bg="#e8f0fe")
        button_frame.grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(button_frame, text="Reset", font=("Helvetica", 12, "bold"), bg="red", fg="white",
                  command=self.reset_fields, width=10).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="Submit", font=("Helvetica", 12, "bold"), bg="#0077cc", fg="white",
                  command=self.validate_login, width=10).grid(row=0, column=1, padx=10)

        tk.Button(right_frame, text="Quick Attendance", font=("Helvetica", 12, "bold"), bg="#003366", fg="white",
                  command=self.quick_attendance).pack(padx=20, pady=20)
        
        tk.Button(right_frame, text="exit", font=("Helvetica", 12, "bold"), bg="#003366", fg="white",
                  command=self.root.destroy).pack(padx=20, pady=20)

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.VALID_USERNAME and password == self.VALID_PASSWORD:
            self.on_login_success()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password!")

    def on_login_success(self):
        messagebox.showinfo("Login", "Login successful! Proceeding to dashboard...")
        self.root.destroy()
        mainpage.main()

    def quick_attendance(self):
        messagebox.showinfo("Quick Attendance", "Quick attendance started!")
        self.root.destroy()
        attendance_taker.main()

    def reset_fields(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = LoginApp(root)
    root.attributes('-fullscreen', True)
    root.bind('<Escape>', lambda e: root.destroy())  # Allow exit with Escape key
    # root.geometry("800x600")  # Set a default size for the window
    
    root.mainloop()
    


if __name__ == "__main__":
    main()