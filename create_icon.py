from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # Create a 256x256 image with transparent background
    size = (256, 256)
    img = Image.new('RGBA', size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Draw rounded square (Blue)
    # Color: #1F6AA5 (CustomTkinter Blueish)
    blue_color = (31, 106, 165)
    rect_coords = [10, 10, 246, 246]
    draw.rounded_rectangle(rect_coords, radius=40, fill=blue_color, outline=None)

    # Draw Text "CE" (Customs Extractor)
    # Try to use a default font
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except IOError:
        font = ImageFont.load_default()

    text = "CE"
    
    # Calculate text position to center it
    # getbbox returns (left, top, right, bottom)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size[0] - text_width) / 2
    y = (size[1] - text_height) / 2 - 10 # Adjust slightly up

    draw.text((x, y), text, fill="white", font=font)

    # Save as .ico containing multiple sizes
    img.save('app_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("app_icon.ico created successfully!")

if __name__ == "__main__":
    try:
        create_icon()
    except ImportError:
        print("Pillow not found. Creating a dummy file...")
        # Fallback if Pillow is missing (unlikely since we use customtkinter which often has PIL)
        with open("app_icon.ico", "wb") as f:
            f.write(b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00\x68\x05\x00\x00\x16\x00\x00\x00')
