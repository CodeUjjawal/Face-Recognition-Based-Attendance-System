import sqlite3
from tkinter import Tk, Label, Button, messagebox, ttk, StringVar
from tkcalendar import DateEntry
from datetime import datetime
import mainpage


class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Tracker")
        self.root.geometry("700x550")
        self.root.configure(bg='white')
        self.root.bind('<Escape>', lambda e: self.root.quit())  # Escape key binding

        # Title Label
        title_label = Label(root, text="Attendance Tracker Sheet", font=("Arial", 20, "bold"),
                            bg='white', fg='#003366')
        title_label.pack(pady=20)

        # Date selection
        date_label = Label(root, text="Select Date:", font=("Arial", 14), bg='white', fg='#003366')
        date_label.pack()

        self.selected_date = StringVar()
        self.date_entry = DateEntry(root, textvariable=self.selected_date, date_pattern='yyyy-mm-dd',
                                    background='blue', foreground='white', borderwidth=2, font=("Arial", 12))
        self.date_entry.pack(pady=10)

        # Buttons Frame
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        show_button = Button(btn_frame, text="Show Attendance", command=self.fetch_attendance,
                             font=("Arial", 12, "bold"), bg='#003366', fg='white', width=18)
        show_button.grid(row=0, column=0, padx=5)

        back_button = Button(btn_frame, text="reset", command=self.reset_form,
                             font=("Arial", 12, "bold"), bg='#003366', fg='white', width=10)
        back_button.grid(row=0, column=1, padx=5)

        exit_button = Button(btn_frame, text="Exit", command=self.tomain,
                             font=("Arial", 12, "bold"), bg='red', fg='white', width=10)
        exit_button.grid(row=0, column=2, padx=5)

        # Treeview (Table)
        self.tree = ttk.Treeview(root, columns=('Name', 'Morning Time', 'Evening Time'), show='headings')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Morning Time', text='Morning Time')
        self.tree.heading('Evening Time', text='Evening Time')

        self.tree.column('Name', anchor='center', width=200)
        self.tree.column('Morning Time', anchor='center', width=150)
        self.tree.column('Evening Time', anchor='center', width=150)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black",
                        rowheight=25, fieldbackground="white", font=("Arial", 12))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'),
                        background='#003366', foreground='white')

        self.tree.pack(pady=20, fill='x', padx=20)
    
    def tomain(self):
        messagebox.showinfo("Back", "Back to main dashboard...")
        self.root.destroy()
        mainpage.main()        

    def clear_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def reset_form(self):
        self.clear_table()
        self.selected_date.set('')

    def fetch_attendance(self):
        self.clear_table()

        date_str = self.selected_date.get().strip()
        if not date_str:
            messagebox.showwarning("Missing Date", "Please select a date before showing attendance.")
            return

        try:
            datetime.strptime(date_str, '%Y-%m-%d')  # validate format

            conn = sqlite3.connect('E:\\python-venv\\attendance.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name, time FROM attendance WHERE date = ?", (date_str,))
            rows = cursor.fetchall()
            conn.close()

            if not rows:
                messagebox.showwarning("No Data", "No attendance data available for the selected date.")
                return

            attendance_dict = {}

            for name, time_str in rows:
                try:
                    time_obj = datetime.strptime(time_str, '%H:%M:%S')
                    hour = time_obj.hour

                    if name not in attendance_dict:
                        attendance_dict[name] = {'morning': '', 'evening': ''}

                    if hour <= 10:
                        attendance_dict[name]['morning'] = time_str
                    else:
                        attendance_dict[name]['evening'] = time_str

                except ValueError:
                    continue  # Skip bad time formats

            for name, times in attendance_dict.items():
                self.tree.insert('', 'end', values=(name, times['morning'], times['evening']))

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def main():
    root = Tk()
    app = AttendanceApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()