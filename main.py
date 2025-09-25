import customtkinter as ctk
from converter import ImageConverter
from gui import ImageConverterGUI

def main():
    # Appearance configuration
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    # Create main window
    root = ctk.CTk()
    root.title("Image Converter Pro")
    root.geometry("1000x750")
    root.minsize(900, 650)
    
    # Initialize application
    converter = ImageConverter()
    app = ImageConverterGUI(root, converter)
    
    # Center window
    root.eval('tk::PlaceWindow . center')
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main()