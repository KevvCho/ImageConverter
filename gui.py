import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os
from pathlib import Path

class ImageConverterGUI:
    def __init__(self, root, converter):
        self.root = root
        self.converter = converter
        self.current_file = None
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Configure grid
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Main content area
        self.create_main_content()
        
    def create_sidebar(self):
        """Create sidebar with controls"""
        sidebar = ctk.CTkFrame(self.root, width=250, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(10, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(sidebar, text="Image Converter", 
                                 font=ctk.CTkFont(size=22, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Load image button
        self.load_btn = ctk.CTkButton(sidebar, text="Load Image", 
                                    command=self.load_image, height=40)
        self.load_btn.grid(row=1, column=0, padx=20, pady=10)
        
        # File info
        self.file_info = ctk.CTkLabel(sidebar, text="No image loaded", 
                                    font=ctk.CTkFont(size=12), wraplength=220)
        self.file_info.grid(row=2, column=0, padx=20, pady=10)
        
        # Separator
        separator = ctk.CTkFrame(sidebar, height=2)
        separator.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Output format
        ctk.CTkLabel(sidebar, text="Output Format:", 
                   font=ctk.CTkFont(weight="bold")).grid(row=4, column=0, padx=20, pady=(10,5), sticky="w")
        
        self.format_var = ctk.StringVar(value="JPEG")
        format_combo = ctk.CTkComboBox(sidebar, values=["JPEG", "PNG", "WEBP", "BMP"], 
                                     variable=self.format_var, command=self.on_format_change)
        format_combo.grid(row=5, column=0, padx=20, pady=5, sticky="ew")
        
        # Quality slider
        ctk.CTkLabel(sidebar, text="Quality:").grid(row=6, column=0, padx=20, pady=(15,5), sticky="w")
        
        self.quality_var = ctk.IntVar(value=85)
        quality_slider = ctk.CTkSlider(sidebar, from_=1, to=100, variable=self.quality_var,
                                     command=self.on_quality_change)
        quality_slider.grid(row=7, column=0, padx=20, pady=5, sticky="ew")
        
        self.quality_label = ctk.CTkLabel(sidebar, text="85%")
        self.quality_label.grid(row=8, column=0, padx=20, pady=(0,10))
        
        # Resize options
        ctk.CTkLabel(sidebar, text="Resize:", 
                   font=ctk.CTkFont(weight="bold")).grid(row=9, column=0, padx=20, pady=(15,5), sticky="w")
        
        resize_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        resize_frame.grid(row=10, column=0, padx=20, pady=5, sticky="ew")
        resize_frame.grid_columnconfigure(0, weight=1)
        resize_frame.grid_columnconfigure(1, weight=1)
        
        self.width_var = ctk.StringVar(value="Original")
        self.height_var = ctk.StringVar(value="Original")
        
        ctk.CTkLabel(resize_frame, text="Width:").grid(row=0, column=0, sticky="w")
        width_entry = ctk.CTkEntry(resize_frame, textvariable=self.width_var, width=80)
        width_entry.grid(row=1, column=0, pady=2)
        
        ctk.CTkLabel(resize_frame, text="Height:").grid(row=0, column=1, sticky="w")
        height_entry = ctk.CTkEntry(resize_frame, textvariable=self.height_var, width=80)
        height_entry.grid(row=1, column=1, pady=2)
        
        self.maintain_aspect = ctk.BooleanVar(value=True)
        aspect_check = ctk.CTkCheckBox(sidebar, text="Maintain aspect ratio", 
                                     variable=self.maintain_aspect)
        aspect_check.grid(row=11, column=0, padx=20, pady=5, sticky="w")
        
        # Convert button
        self.convert_btn = ctk.CTkButton(sidebar, text="Convert Image", 
                                       command=self.convert_image, state="disabled")
        self.convert_btn.grid(row=12, column=0, padx=20, pady=20)
        
        # Save button
        self.save_btn = ctk.CTkButton(sidebar, text="Save Image", 
                                    command=self.save_image, state="disabled",
                                    fg_color="#2B8C44", hover_color="#247A3A")
        self.save_btn.grid(row=13, column=0, padx=20, pady=(0,20))
        
    def create_main_content(self):
        """Create main content area with image previews"""
        main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        main_frame.grid(row=0, column=1, sticky="nsew")
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Title
        title = ctk.CTkLabel(main_frame, text="Image Preview", 
                           font=ctk.CTkFont(size=18, weight="bold"))
        title.grid(row=0, column=0, padx=20, pady=20)
        
        # Preview area
        preview_frame = ctk.CTkFrame(main_frame)
        preview_frame.grid(row=1, column=0, padx=20, pady=(0,20), sticky="nsew")
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(1, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        
        # Original image preview
        original_frame = ctk.CTkFrame(preview_frame)
        original_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(original_frame, text="Original Image", 
                   font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.original_canvas = ctk.CTkCanvas(original_frame, width=300, height=300, 
                                           bg="#2B2B2B", highlightthickness=0)
        self.original_canvas.pack(pady=10)
        self.original_canvas.create_text(150, 150, text="No image loaded", 
                                       fill="white", font=("Arial", 12))
        
        # Converted image preview
        converted_frame = ctk.CTkFrame(preview_frame)
        converted_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        ctk.CTkLabel(converted_frame, text="Converted Image", 
                   font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        self.converted_canvas = ctk.CTkCanvas(converted_frame, width=300, height=300, 
                                            bg="#2B2B2B", highlightthickness=0)
        self.converted_canvas.pack(pady=10)
        self.converted_canvas.create_text(150, 150, text="Preview will appear here", 
                                        fill="white", font=("Arial", 12))
        
        # File size info
        self.size_info = ctk.CTkLabel(main_frame, text="Original: N/A | Converted: N/A", 
                                    font=ctk.CTkFont(size=12))
        self.size_info.grid(row=2, column=0, pady=10)
        
    def load_image(self):
        """Load image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff"),
                ("JPEG", "*.jpg *.jpeg"),
                ("PNG", "*.png"),
                ("WEBP", "*.webp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            success, message = self.converter.load_image(file_path)
            if success:
                self.current_file = file_path
                self.update_file_info()
                self.update_previews()
                self.convert_btn.configure(state="normal")
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)
    
    def update_file_info(self):
        """Update file information display"""
        info = self.converter.get_image_info()
        if info:
            text = (f"File: {info['filename']}\n"
                   f"Size: {info['size'][0]}x{info['size'][1]}\n"
                   f"Format: {info['format']}\n"
                   f"File Size: {info['file_size']}")
            self.file_info.configure(text=text)
    
    def update_previews(self):
        """Update image previews"""
        original_preview, processed_preview = self.converter.get_preview_images()
        
        # Update original preview
        self.original_canvas.delete("all")
        if original_preview:
            photo = ImageTk.PhotoImage(original_preview)
            self.original_canvas.image = photo  # Keep reference
            self.original_canvas.create_image(150, 150, image=photo)
        else:
            self.original_canvas.create_text(150, 150, text="No image loaded", 
                                           fill="white", font=("Arial", 12))
        
        # Update converted preview
        self.converted_canvas.delete("all")
        if processed_preview:
            photo = ImageTk.PhotoImage(processed_preview)
            self.converted_canvas.image = photo  # Keep reference
            self.converted_canvas.create_image(150, 150, image=photo)
            
            # Update size info
            original_size = self.converter.get_image_info()['file_size']
            converted_size = self.converter.estimate_file_size(self.format_var.get(), 
                                                             self.quality_var.get())
            self.size_info.configure(text=f"Original: {original_size} | Converted: {converted_size}")
        else:
            self.converted_canvas.create_text(150, 150, text="Preview will appear here", 
                                            fill="white", font=("Arial", 12))
            self.size_info.configure(text="Original: N/A | Converted: N/A")
    
    def on_format_change(self, choice):
        """Handle format change"""
        if self.converter.original_image:
            self.convert_image()
    
    def on_quality_change(self, value):
        """Handle quality change"""
        self.quality_label.configure(text=f"{int(float(value))}%")
        if self.converter.processed_image:
            self.convert_image()
    
    def convert_image(self):
        """Convert the image"""
        if not self.converter.original_image:
            return
        
        # Get resize dimensions
        resize = None
        try:
            width = int(self.width_var.get()) if self.width_var.get() != "Original" else None
            height = int(self.height_var.get()) if self.height_var.get() != "Original" else None
            
            if width is not None and height is not None:
                resize = (width, height)
            elif width is not None:
                resize = (width, self.converter.original_image.size[1])
            elif height is not None:
                resize = (self.converter.original_image.size[0], height)
        except ValueError:
            messagebox.showerror("Error", "Invalid dimensions")
            return
        
        success, message = self.converter.convert_image(
            output_format=self.format_var.get(),
            quality=self.quality_var.get(),
            resize=resize,
            maintain_aspect=self.maintain_aspect.get()
        )
        
        if success:
            self.update_previews()
            self.save_btn.configure(state="normal")
        else:
            messagebox.showerror("Error", message)
    
    def save_image(self):
        """Save the converted image"""
        if not self.converter.processed_image:
            return
        
        # Suggest output filename
        original_name = Path(self.current_file).stem
        output_format = self.format_var.get().lower()
        suggested_name = f"{original_name}_converted.{output_format}"
        
        file_path = filedialog.asksaveasfilename(
            title="Save Converted Image",
            initialfile=suggested_name,
            defaultextension=f".{output_format}",
            filetypes=[(f"{self.format_var.get()} files", f"*.{output_format}")]
        )
        
        if file_path:
            success, message = self.converter.save_image(
                file_path, 
                self.format_var.get(), 
                self.quality_var.get()
            )
            
            if success:
                messagebox.showinfo("Success", message)
            else:
                messagebox.showerror("Error", message)

# Run the application
if __name__ == "__main__":
    import customtkinter as ctk
    from converter import ImageConverter
    
    ctk.set_appearance_mode("Dark")
    root = ctk.CTk()
    app = ImageConverterGUI(root, ImageConverter())
    root.mainloop()