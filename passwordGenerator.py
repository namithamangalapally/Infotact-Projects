import tkinter as tk
from tkinter import messagebox, filedialog
import random, string, urllib.request, io
from PIL import Image, ImageTk

# -----------------------------
# LOGIN PAGE CLASS
# -----------------------------
class LoginPage:
    def __init__(self, root, on_success):
        self.root = root
        self.on_success = on_success
        # Create a fixed-size login frame
        self.frame = tk.Frame(root, bg="white", width=600, height=300)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.frame.pack_propagate(False)

        tk.Label(self.frame, text="Login", font=("Arial", 20), bg="white", fg="black").pack(pady=20)
        tk.Label(self.frame, text="Username:", bg="white", fg="black").pack(pady=5)
        self.username_entry = tk.Entry(self.frame)
        self.username_entry.pack(pady=5)
        tk.Label(self.frame, text="Password:", bg="white", fg="black").pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self.frame, text="Login", command=self.check_login).pack(pady=20)
    
    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Hardcoded credentials for demonstration
        if username == "admin" and password == "admin123":
            self.frame.destroy()
            self.on_success()
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

# -----------------------------
# MAIN APPLICATION CLASS
# -----------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Password Generator and Text Editor")
        root.geometry("800x600")
        self.load_bg_image("https://static1.makeuseofimages.com/wordpress/wp-content/uploads/2024/06/person-inputting-password-user-name-on-secure-laptop.jpg")
        self.create_widgets()
    
    def load_bg_image(self, path):
        try:
            if path.startswith("http"):
                with urllib.request.urlopen(path) as u:
                    raw_data = u.read()
                img = Image.open(io.BytesIO(raw_data))
            else:
                img = Image.open(path)
            img = img.resize((800, 600), Image.Resampling.LANCZOS)
            self.bg = ImageTk.PhotoImage(img)
            bg_label = tk.Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print("Error loading background image:", e)
    
    def create_widgets(self):
        # Central container for widgets
        container = tk.Frame(self.root, bg="white", bd=2, relief="ridge")
        container.place(relx=0.5, rely=0.5, anchor="center", width=600, height=400)
        
        # --- Password Generator Frame ---
        pg_frame = tk.LabelFrame(container, text="Password Generator", bg="white")
        pg_frame.pack(padx=10, pady=10, fill="x")
        
        tk.Label(pg_frame, text="Length:", bg="white", fg="black").grid(row=0, column=0, sticky="w")
        self.length_var = tk.IntVar(value=12)
        tk.Entry(pg_frame, textvariable=self.length_var, width=5).grid(row=0, column=1, sticky="w")
        
        # Complexity Checkboxes
        self.use_upper = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        tk.Checkbutton(pg_frame, text="Uppercase", variable=self.use_upper, bg="white", fg="black").grid(row=0, column=2, padx=2)
        tk.Checkbutton(pg_frame, text="Digits", variable=self.use_digits, bg="white", fg="black").grid(row=0, column=3, padx=2)
        tk.Checkbutton(pg_frame, text="Symbols", variable=self.use_symbols, bg="white", fg="black").grid(row=0, column=4, padx=2)
        
        tk.Button(pg_frame, text="Generate", command=self.generate_password).grid(row=0, column=5, padx=5)
        self.pw_var = tk.StringVar()
        tk.Entry(pg_frame, textvariable=self.pw_var, width=30).grid(row=1, column=0, columnspan=5, pady=5)
        tk.Button(pg_frame, text="Copy", command=self.copy_password).grid(row=1, column=5, padx=5)
        tk.Button(pg_frame, text="Save to File", command=self.save_password_to_file).grid(row=2, column=0, columnspan=6, pady=5)
        
        # --- Text Editor Frame ---
        te_frame = tk.LabelFrame(container, text="Text Editor", bg="white")
        te_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Use grid layout inside te_frame so that the text editor expands and the button stays below
        self.text_area = tk.Text(te_frame, wrap="word", undo=True, bg="white", fg="black")
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # Configure grid weight so the text area expands
        te_frame.rowconfigure(0, weight=1)
        te_frame.columnconfigure(0, weight=1)
        
        # Separate copy button for text editor
        tk.Button(te_frame, text="Copy Text from Editor", command=self.copy_text_editor).grid(row=1, column=0, pady=(0,5))
    
    def generate_password(self):
        length = self.length_var.get()
        chars = string.ascii_lowercase
        if self.use_upper.get():
            chars += string.ascii_uppercase
        if self.use_digits.get():
            chars += string.digits
        if self.use_symbols.get():
            chars += string.punctuation
        if length < 1:
            messagebox.showerror("Error", "Length must be at least 1.")
            return
        self.pw_var.set("".join(random.choice(chars) for _ in range(length)))
    
    def copy_password(self):
        self.root.clipboard_clear()
        self.root.clipboard_append(self.pw_var.get())
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    
    def save_password_to_file(self):
        password = self.pw_var.get()
        if not password:
            messagebox.showerror("Error", "No password generated yet.")
            return
        file_path = filedialog.asksaveasfilename(
            title="Save Password", 
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(password + "\n")
                messagebox.showinfo("Saved", f"Password saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save password:\n{e}")
    
    def copy_text_editor(self):
        text = self.text_area.get("1.0", tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            messagebox.showinfo("Copied", "Text from editor copied to clipboard.")
        else:
            messagebox.showerror("Error", "Text editor is empty.")

# -----------------------------
# MAIN PROGRAM
# -----------------------------
if __name__ == "__main__":
    root = tk.Tk()
    
    def start_app():
        App(root)
    
    LoginPage(root, on_success=start_app)
    root.mainloop()
