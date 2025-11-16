#!/usr/bin/env python3
"""
Convert GitHub Avatar to ASCII Art
Run this locally to generate ASCII art from your GitHub avatar
"""

import requests
from PIL import Image, ImageEnhance
import io

GITHUB_USERNAME = "alaeddinedaly"

# ASCII characters from darkest to lightest
ASCII_CHARS = ['@', '#', '%', '*', '+', '=', '-', ':', '.', ' ']

def download_avatar(username):
    """Download GitHub avatar"""
    print(f"📥 Downloading avatar for {username}...")
    user_url = f"https://api.github.com/users/{username}"
    user_data = requests.get(user_url).json()
    avatar_url = user_data['avatar_url']
    
    response = requests.get(avatar_url)
    img = Image.open(io.BytesIO(response.content))
    print(f"✅ Avatar downloaded: {img.size}")
    return img

def image_to_ascii(img, width=50, contrast=1.5):
    """Convert image to ASCII art"""
    print(f"🎨 Converting to ASCII (width={width}, contrast={contrast})...")
    
    # Convert to grayscale
    img = img.convert('L')
    
    # Calculate new height maintaining aspect ratio
    aspect_ratio = img.height / img.width
    new_height = int(aspect_ratio * width * 0.55)  # 0.55 adjusts for character height
    
    # Resize image
    img = img.resize((width, new_height), Image.Resampling.LANCZOS)
    
    # Enhance contrast for better detail
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(contrast)
    
    # Convert to ASCII
    pixels = img.getdata()
    ascii_lines = []
    
    for i in range(0, len(pixels), width):
        line = ''
        for pixel in list(pixels[i:i+width]):
            # Map pixel brightness to ASCII character
            ascii_index = min(pixel // 26, len(ASCII_CHARS) - 1)
            line += ASCII_CHARS[ascii_index]
        ascii_lines.append(line)
    
    return ascii_lines

def print_ascii_art(ascii_lines):
    """Print ASCII art"""
    print("\n" + "="*60)
    print("YOUR ASCII ART:")
    print("="*60)
    for line in ascii_lines:
        print(line)
    print("="*60)

def generate_python_code(ascii_lines):
    """Generate Python code to paste into your script"""
    print("\n" + "="*60)
    print("COPY THIS INTO generate_svg.py:")
    print("="*60)
    print("\ndef get_custom_avatar_art() -> List[str]:")
    print('    """Your custom ASCII art avatar"""')
    print("    return [")
    for line in ascii_lines:
        # Escape quotes and format as Python string
        escaped_line = line.replace('"', '\\"')
        print(f'        "{escaped_line}",')
    print("    ]")
    print("="*60)

def main():
    """Main function with multiple size options"""
    print("🚀 GitHub Avatar to ASCII Converter")
    print("="*60)
    
    # Download avatar
    img = download_avatar(GITHUB_USERNAME)
    
    print("\n📐 Generating different sizes...\n")
    
    # Generate multiple sizes
    sizes = [
        (30, 1.5, "Small (compact)"),
        (40, 1.5, "Medium (balanced)"),
        (50, 1.5, "Large (detailed)"),
        (40, 2.0, "Medium with high contrast"),
    ]
    
    for width, contrast, description in sizes:
        print(f"\n{'='*60}")
        print(f"Option {sizes.index((width, contrast, description)) + 1}: {description}")
        print('='*60)
        ascii_lines = image_to_ascii(img, width=width, contrast=contrast)
        print_ascii_art(ascii_lines)
        print(f"\nLines: {len(ascii_lines)} | Width: {width} chars")
    
    # Generate code for the best option (you can change this)
    print("\n\n" + "🎯 RECOMMENDED: Option 2 (Medium - 40 chars)")
    ascii_lines = image_to_ascii(img, width=40, contrast=1.5)
    generate_python_code(ascii_lines)
    
    print("\n💡 TIP: Try different options and pick the one that looks best!")
    print("💡 Copy the Python code above and replace get_custom_avatar_art() in generate_svg.py")

if __name__ == "__main__":
    main()
