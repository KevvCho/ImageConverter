from PIL import Image
import os
from io import BytesIO

class ImageConverter:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
        self.original_image = None
        self.processed_image = None
        self.current_quality = 85
        self.current_format = "JPEG"
        
    def load_image(self, file_path):
        """Load image and verify format"""
        try:
            self.original_image = Image.open(file_path)
            self.original_image.filename = file_path  # Store original filename
            return True, "Image loaded successfully"
        except Exception as e:
            return False, f"Error loading image: {str(e)}"
    
    def get_image_info(self):
        """Get information about the loaded image"""
        if not self.original_image:
            return None
        
        try:
            file_size = os.path.getsize(self.original_image.filename) if self.original_image.filename else 0
            info = {
                'format': self.original_image.format,
                'size': self.original_image.size,
                'mode': self.original_image.mode,
                'file_size': f"{file_size / 1024:.1f} KB",
                'filename': os.path.basename(self.original_image.filename) if self.original_image.filename else "Unknown"
            }
            return info
        except:
            return None
    
    def convert_image(self, output_format, quality=85, resize=None, maintain_aspect=True):
        """Convert image to desired format with quality applied to preview"""
        if not self.original_image:
            return False, "No image loaded"
        
        try:
            # Store current settings
            self.current_quality = quality
            self.current_format = output_format
            
            # Create copy of original image
            converted = self.original_image.copy()
            
            # Resize if needed
            if resize and resize != converted.size:
                if maintain_aspect:
                    # Maintain aspect ratio
                    converted.thumbnail(resize, Image.Resampling.LANCZOS)
                else:
                    # Force exact size
                    converted = converted.resize(resize, Image.Resampling.LANCZOS)
            
            # Handle format-specific conversions
            if output_format.upper() in ['JPEG', 'JPG']:
                if converted.mode in ['RGBA', 'P']:
                    converted = converted.convert('RGB')
            
            # Apply quality settings for preview by saving to buffer and reloading
            # This ensures the preview reflects the actual quality compression
            buffer = BytesIO()
            save_kwargs = {}
            
            if output_format.upper() in ['JPEG', 'JPG']:
                save_kwargs = {'quality': quality, 'optimize': True}
            elif output_format.upper() == 'WEBP':
                save_kwargs = {'quality': quality, 'method': 6}
            elif output_format.upper() == 'PNG':
                save_kwargs = {'optimize': True}
            
            # Save with quality settings to buffer
            converted.save(buffer, format=output_format.upper(), **save_kwargs)
            
            # Reload from buffer to get the compressed version
            buffer.seek(0)
            self.processed_image = Image.open(buffer)
            
            return True, f"Conversion to {output_format} successful"
            
        except Exception as e:
            return False, f"Conversion error: {str(e)}"
    
    def save_image(self, output_path, output_format=None, quality=None):
        """Save processed image"""
        if not self.processed_image:
            return False, "No processed image to save"
        
        # Use current settings if not specified
        if output_format is None:
            output_format = self.current_format
        if quality is None:
            quality = self.current_quality
        
        try:
            save_kwargs = {}
            
            if output_format.upper() in ['JPEG', 'JPG']:
                save_kwargs = {'quality': quality, 'optimize': True}
                # Ensure RGB mode for JPEG
                image_to_save = self.processed_image
                if image_to_save.mode in ['RGBA', 'P']:
                    image_to_save = image_to_save.convert('RGB')
            elif output_format.upper() == 'WEBP':
                save_kwargs = {'quality': quality, 'method': 6}
                image_to_save = self.processed_image
            elif output_format.upper() == 'PNG':
                save_kwargs = {'optimize': True}
                image_to_save = self.processed_image
            else:
                image_to_save = self.processed_image
            
            image_to_save.save(output_path, format=output_format.upper(), **save_kwargs)
            return True, f"Image saved to: {output_path}"
            
        except Exception as e:
            return False, f"Save error: {str(e)}"
    
    def get_preview_images(self, max_size=(300, 300)):
        """Get images for preview - now reflects actual quality"""
        if not self.original_image:
            return None, None
        
        # Original preview
        original_preview = self.original_image.copy()
        original_preview.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Processed preview - use the actual processed image with quality applied
        processed_preview = None
        if self.processed_image:
            processed_preview = self.processed_image.copy()
            processed_preview.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        return original_preview, processed_preview
    
    def estimate_file_size(self, output_format=None, quality=None):
        """Estimate output file size"""
        if not self.processed_image:
            return "N/A"
        
        # Use current settings if not specified
        if output_format is None:
            output_format = self.current_format
        if quality is None:
            quality = self.current_quality
        
        try:
            buffer = BytesIO()
            save_kwargs = {}
            
            if output_format.upper() in ['JPEG', 'JPG']:
                save_kwargs = {'quality': quality}
            elif output_format.upper() == 'WEBP':
                save_kwargs = {'quality': quality}
            
            self.processed_image.save(buffer, format=output_format.upper(), **save_kwargs)
            size_kb = len(buffer.getvalue()) / 1024
            return f"{size_kb:.1f} KB"
            
        except Exception:
            return "N/A"