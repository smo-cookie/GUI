import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap import Style

UPLOAD_DIR = "uploads"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class SMOCookieApp:
    def __init__(self):
        self.root = tk.Tk()
        self.style = Style(theme="solar")
        self.root.title("smo-cookie")
        self.root.geometry("800x600")

        self.selected_file = None
        self.masking_options = [
            "주민등록번호", "주소", "연락처", "생년월일", "계좌번호", "여권번호", "이메일", "카드번호", "성명"
        ]
        self.selected_options = {}

        self.create_main_ui()
    
    def create_main_ui(self):
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TButton", font=("Arial", 10))

        tk.Label(self.root, text="smo-cookie", font=("Arial", 20, "bold")).pack(pady=20)

        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)

        self.file_label = tk.Label(file_frame, text="No file selected")
        self.file_label.grid(row=0, column=0, padx=10)
        
        self.create_button(file_frame, "Select File", self.select_file, 1, "green")
        self.create_button(file_frame, "Open File", self.open_file, 2, "steel blue")
        self.create_button(file_frame, "Delete File", self.delete_file, 3, "firebrick")

        options_frame = tk.LabelFrame(self.root, text="Masking Options")
        options_frame.pack(pady=10, fill='x', padx=20)

        for option in self.masking_options:
            var = tk.BooleanVar()
            self.selected_options[option] = var
            tk.Checkbutton(options_frame, text=option, variable=var).pack(anchor='w', padx=10, pady=2)

        tk.Label(self.root, text="Additional information to mask (separate with commas)").pack(pady=5)
        self.additional_info = tk.StringVar()
        tk.Entry(self.root, textvariable=self.additional_info, width=50).pack(pady=5)

        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=20)
        
        self.create_button(action_frame, "Upload", self.upload_file, 0, "darkgoldenrod")
        self.create_button(action_frame, "Mask", self.start_masking, 1, "darkgoldenrod")


    def create_button(self, parent, text, command, column, color=None):
        button = tk.Button(parent, text=text, command=command, font=("Arial", 10))
    
        if color:
            button.config(fg="white", bg=color)  
    
        button.grid(row=0, column=column, padx=5, pady=5)


    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[["Word and Excel files", "*.docx *.xlsx"]])
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")

    def open_file(self):
        if not self.selected_file:
            messagebox.showwarning("Warning", "No file selected to open.")
            return
        try:
            if os.name == 'nt':
                os.startfile(self.selected_file)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.run([opener, self.selected_file])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open file: {e}")

    def delete_file(self):
        if self.selected_file:
            self.selected_file = None
            self.file_label.config(text="No file selected")
            messagebox.showinfo("Info", "File selection cleared.")
        else:
            messagebox.showwarning("Warning", "No file selected to delete.")

    def upload_file(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected for upload.")
            return
        
        dest_path = os.path.join(UPLOAD_DIR, os.path.basename(self.selected_file))
        try:
            shutil.copy(self.selected_file, dest_path)
            messagebox.showinfo("Success", f"File uploaded to {dest_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to upload file: {e}")

    def start_masking(self):
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected for masking.")
            return

        selected_types = [key for key, var in self.selected_options.items() if var.get()]
        additional_data = self.additional_info.get().split(',') if self.additional_info.get() else []
        
        self.call_backend_masking(self.selected_file, selected_types, additional_data)
        messagebox.showinfo("Success", "Masking completed successfully!")


if __name__ == "__main__":
    app = SMOCookieApp()
    app.root.mainloop()
