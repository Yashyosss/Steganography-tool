import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os

class SteganographyTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("900x600")
        self.root.resizable(False, False)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_sidebar()
        self.create_main_area()

        # Status Bar
        self.status = ctk.CTkLabel(root, text="Ready", height=20, anchor="w", fg_color="#2C2F33", corner_radius=0)
        self.status.pack(side="bottom", fill="x")

    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=15)
        sidebar.pack(side="left", fill="y", padx=10, pady=10)

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Embed Message", self.show_embed_message),
            ("Detect Message", self.show_detect_message),
            ("History", self.show_history),
            ("Help", self.show_help),
            ("Themes", self.show_themes)
        ]

        for (text, command) in buttons:
            btn = ctk.CTkButton(sidebar, text=text, command=command, corner_radius=12)
            btn.pack(padx=10, pady=10, fill="x")

    def create_main_area(self):
        self.main_area = ctk.CTkFrame(self.root, corner_radius=15)
        self.main_area.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        self.dashboard_label = ctk.CTkLabel(self.main_area, text="Welcome to Steganography Tool", font=("Arial", 18))
        self.dashboard_label.pack(pady=30)

    def clear_main_area(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.clear_main_area()
        self.dashboard_label = ctk.CTkLabel(self.main_area, text="Dashboard Welcome to Steganography Tool", font=("Arial", 18))
        self.dashboard_label.pack(pady=30)

    def show_embed_message(self):
        self.clear_main_area()

        ctk.CTkLabel(self.main_area, text="Select Image to Embed Message", font=("Arial", 14)).pack(pady=10)

        select_button = ctk.CTkButton(self.main_area, text="Select Image", command=self.embed_select_image)
        select_button.pack(pady=10)

    def embed_select_image(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.bmp;*.jpg;*.jpeg;*.gif")])
        if image_path:
            self.show_embed_message_form(image_path)

    def show_embed_message_form(self, image_path):
        self.clear_main_area()

        ctk.CTkLabel(self.main_area, text="Enter Message to Embed", font=("Arial", 14)).pack(pady=10)

        message_entry = ctk.CTkTextbox(self.main_area, height=150, width=600, corner_radius=10)
        message_entry.pack(pady=10)

        def save_embedded():
            message = message_entry.get("1.0", "end").strip()
            if message:
                self.embed_message(image_path, message)

        save_button = ctk.CTkButton(self.main_area, text="Embed & Save", command=save_embedded)
        save_button.pack(pady=10)

    def embed_message(self, image_path, message):
        img = Image.open(image_path)
        img = img.convert("RGB")

        message += "<END>"

        binary_message = ''.join(format(ord(char), '08b') for char in message)
        img_data = list(img.getdata())

        if len(binary_message) > len(img_data) * 3:
            messagebox.showerror("Error", "Message too long for selected image")
            return

        new_data = []
        data_index = 0

        for pixel in img_data:
            pixel = list(pixel)
            for i in range(3):
                if data_index < len(binary_message):
                    pixel[i] = pixel[i] & ~1 | int(binary_message[data_index])
                    data_index += 1
            new_data.append(tuple(pixel))

        img.putdata(new_data)

        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if save_path:
            img.save(save_path)
            messagebox.showinfo("Success", "Message embedded and saved!")

    def show_detect_message(self):
        self.clear_main_area()

        ctk.CTkLabel(self.main_area, text="Select Image to Detect Message", font=("Arial", 14)).pack(pady=10)

        select_button = ctk.CTkButton(self.main_area, text="Select Image", command=self.detect_message)
        select_button.pack(pady=10)

        self.detect_result = ctk.CTkTextbox(self.main_area, height=250, width=600, corner_radius=10)
        self.detect_result.pack(pady=10)

    def detect_message(self):
        image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.bmp;*.jpg;*.jpeg;*.gif")])
        if not image_path:
            return

        img = Image.open(image_path)
        img = img.convert("RGB")
        img_data = list(img.getdata())

        binary_message = "".join(str(pixel[i] & 1) for pixel in img_data for i in range(3))

        message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))

        hidden_message = message.split("<END>")[0]

        self.detect_result.delete("1.0", "end")
        if hidden_message.strip():
            self.detect_result.insert("end", hidden_message)
        else:
            messagebox.showinfo("Info", "No hidden message found.")

    def show_history(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="History (Coming Soon)", font=("Arial", 16)).pack(pady=30)

    def show_help(self):
        self.clear_main_area()
        ctk.CTkLabel(self.main_area, text="Help: 1. Select an image to embed or detect hidden messages. \n 2. Go to Embed message tab or Detect message tab for next process. \n 3. The output will be shown \n 4. Theme Selection check in Theme tab \n Thank you and have a nice day.", font=("Arial", 14)).pack(pady=30)

    def show_themes(self):
        theme_window = ctk.CTkToplevel(self.root)
        theme_window.title("Themes")
        theme_window.geometry("300x200")

        def apply_dark_mode():
            ctk.set_appearance_mode("dark")

        def apply_light_mode():
            ctk.set_appearance_mode("light")

        dark_btn = ctk.CTkButton(theme_window, text="Dark Mode", command=apply_dark_mode)
        dark_btn.pack(pady=10)

        light_btn = ctk.CTkButton(theme_window, text="Light Mode", command=apply_light_mode)
        light_btn.pack(pady=10)

if __name__ == "__main__":
    root = ctk.CTk()
    app = SteganographyTool(root)
    root.mainloop()
