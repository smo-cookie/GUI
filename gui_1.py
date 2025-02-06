# GUI 개발 중..
import os
from pathlib import Path
import ttkbootstrap as ttk
from tkinter import filedialog, messagebox


class SMOCookieApp:
    def __init__(self):
        # 초기 설정 및 메인 윈도우 생성
        self.root = ttk.Window(themename="solar")
        self.root.title("smo-cookie")
        self.root.geometry("600x400")

        # 파일 관련 변수
        self.selected_file = None

        # UI 생성
        self.create_main_ui()

    def create_main_ui(self):
        # 제목 라벨
        ttk.Label(self.root, text="smo-cookie", font=("Arial", 20, "bold")).pack(pady=20)

        # 파일 선택 위젯
        file_frame = ttk.Frame(self.root)
        file_frame.pack(pady=20)

        self.file_label = ttk.Label(file_frame, text="No file selected")
        self.file_label.grid(row=0, column=0, padx=10)

        ttk.Button(file_frame, text="Select File", command=self.select_file).grid(row=0, column=1, padx=10)
        ttk.Button(file_frame, text="Delete File", command=self.delete_file).grid(row=0, column=2, padx=10)

        # 업로드 및 마스킹 버튼
        action_frame = ttk.Frame(self.root)
        action_frame.pack(pady=20)

        ttk.Button(action_frame, text="Upload", command=self.upload_file).grid(row=0, column=0, padx=10)
        ttk.Button(action_frame, text="Mask", command=self.start_masking).grid(row=0, column=1, padx=10)

    def select_file(self):
        # Select File(파일 선택) 대화창 열기
        file_types = [("Word and Excel files", "*.docx *.xlsx")]
        file_path = filedialog.askopenfilename(filetypes=file_types)

        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=f"Selected: {os.path.basename(file_path)}")

    def delete_file(self):
        # Delete File(선택된 파일 초기화)
        if self.selected_file:
            self.selected_file = None
            self.file_label.config(text="No file selected")
            messagebox.showinfo("Info", "File selection cleared.")
        else:
            messagebox.showwarning("Warning", "No file selected to delete.")

    def upload_file(self):
        # 업로드 시 파일이 선택되지 않은 경우 처리
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected for upload.")
            return

        # 여기에서 파일을 서버 또는 데이터베이스로 업로드하는 코드를 추가
        messagebox.showinfo("Success", f"File {os.path.basename(self.selected_file)} uploaded successfully.")

    def start_masking(self):
        # 파일이 선택되어 있지 않을 경우 처리
        if not self.selected_file:
            messagebox.showerror("Error", "No file selected for masking.")
            return

        # 마스킹 작업 수행 후 로그인 창 표시
        detect(self.selected_file)  # 백엔드 detect 기능 호출
        LoginWindow(self.root)  # 로그인 창 열기

# 로그인 기능 없애야 되나?
class LoginWindow:
    def __init__(self, root):
        # 로그인 창 생성
        self.login_window = ttk.Toplevel(root)
        self.login_window.title("Login")
        self.login_window.geometry("400x300")

        # UI 생성
        ttk.Label(self.login_window, text="User Login", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(self.login_window, text="Username").pack(pady=5)
        self.username_entry = ttk.Entry(self.login_window)
        self.username_entry.pack(pady=5)
        

        ttk.Label(self.login_window, text="Password").pack(pady=5)
        self.password_entry = ttk.Entry(self.login_window, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(self.login_window, text="Login", command=self.authenticate_user).pack(pady=20)

    def authenticate_user(self):
        # 로그인 인증
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 간단한 예시 인증
        if username == "admin" and password == "password":
            messagebox.showinfo("Success", "Login successful!")
            self.download_file()
        else:
            messagebox.showerror("Error", "Invalid credentials. Please try again.")

    def download_file(self):
        # 로그인 성공 시 원본 파일 다운로드
        messagebox.showinfo("Download", "The original file has been restored and downloaded.")


def detect(file_path):
    # 백엔드의 detect.py 호출
    print(f"Running detect for: {file_path}")


if __name__ == "__main__":
    app = SMOCookieApp()
    app.root.mainloop() 