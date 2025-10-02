import tkinter as tk
from tkinter import ttk, messagebox
import Std_info_BackEnd as backend  # your backend file


class StudentApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Student Management System")
        self.master.geometry("1100x500")
        self.master.resizable(False, False)

        # ---------- LEFT FRAME (FORM) ----------
        left_frame = tk.Frame(master, padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        labels = ["Name", "Roll", "DOB", "Contact",
                  "Email", "Gender", "Class", "Address"]
        self.entries = {}

        for i, text in enumerate(labels):
            tk.Label(left_frame, text=text+":").grid(row=i,
                                                     column=0, padx=5, pady=5, sticky="w")
            ent = tk.Entry(left_frame, width=30)
            ent.grid(row=i, column=1, padx=5, pady=5)
            self.entries[text.lower()] = ent

        # ---------- BUTTONS ----------
        btn_frame = tk.Frame(left_frame, pady=10)
        btn_frame.grid(row=len(labels), column=0, columnspan=2)

        tk.Button(btn_frame, text="Add", width=12, command=self.add_student).grid(
            row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Update", width=12, command=self.update_student).grid(
            row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Delete", width=12, command=self.delete_student).grid(
            row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Search", width=12, command=self.search_students).grid(
            row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="View All", width=12, command=self.view_students).grid(
            row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Close", width=12, command=self.master.quit).grid(
            row=2, column=1, padx=5, pady=5)

        # ---------- RIGHT FRAME (TABLE) ----------
        right_frame = tk.Frame(master, padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(right_frame,
                                 columns=("id", "name", "roll", "dob", "contact",
                                          "email", "gender", "class", "address"),
                                 show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            right_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Define column headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=100)

        # Bind row selection
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

        # Initially load all students
        self.view_students()

    # ---------- FUNCTIONS ----------
    def clear_form(self):
        for ent in self.entries.values():
            ent.delete(0, tk.END)

    def get_form_data(self):
        return {key: ent.get() for key, ent in self.entries.items()}

    def add_student(self):
        data = self.get_form_data()
        success = backend.insert(data["name"], data["roll"], data["dob"], data["contact"],
                                 data["email"], data["gender"], data["class"], data["address"])
        if success:
            messagebox.showinfo("Success", "Student added successfully!")
            self.view_students()
            self.clear_form()   # ✅ now clears form only after success
        else:
            messagebox.showwarning(
                "Duplicate Roll", f"Roll number {data['roll']} already exists!")

    def view_students(self):
        rows = backend.view()
        self.tree.delete(*self.tree.get_children())  # clear old data
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def search_students(self):
        data = self.get_form_data()
        rows = backend.search(data["name"], data["roll"], data["email"], data["gender"],
                              data["class"], data["contact"], data["dob"], data["address"])
        self.tree.delete(*self.tree.get_children())
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "No student selected")
            return
        student_id = self.tree.item(selected[0])["values"][0]
        backend.delete(student_id)
        self.view_students()
        self.clear_form()

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Error", "No student selected")
            return
        student_id = self.tree.item(selected[0])["values"][0]
        data = self.get_form_data()
        backend.update(student_id, data["name"], data["roll"], data["dob"], data["contact"],
                       data["email"], data["gender"], data["class"], data["address"])
        self.view_students()

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        row = self.tree.item(selected[0])["values"]
        keys = ["id", "name", "roll", "dob", "contact",
                "email", "gender", "class", "address"]
        for key, value in zip(keys[1:], row[1:]):  # skip id
            self.entries[key].delete(0, tk.END)
            self.entries[key].insert(0, value)


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()
