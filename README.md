# Image Converter

A modern Python application for converting images between different formats with a beautiful GUI.

## Features

- **Multiple Formats**: Convert between JPG, PNG, WEBP, BMP
- **Quality Control**: Adjust compression quality (1-100%)
- **Resize Options**: Custom dimensions with aspect ratio preservation
- **Real-time Preview**: Before/after comparison
- **File Size Estimation**: See output size before saving
- **Modern GUI**: Dark theme with intuitive controls

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```
2. Run the application:
```bash
python main.py
```

## Usage

1. Click "Load Image" to select a file

2. Choose output format and quality settings

3. Adjust resize options if needed

4. Click "Convert Image" to see preview

5. Click "Save Image" to export

## Supported Formats

- Input: JPG, JPEG, PNG, WEBP, BMP, TIFF

- Output: JPG, PNG, WEBP, BMP

## Technical Details

- Built with CustomTkinter for modern UI

- Uses PIL/Pillow for image processing