import os
from PIL import Image, ImageFilter

try:
    import cv2
    import numpy as np
    USE_OPENCV = True
except ImportError:
    USE_OPENCV = False
    print("OpenCV not found. Using Pillow for all operations.")

def is_image_file(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))

def apply_blur(input_path, output_path, blur_strength=25):
    # Open the image with Pillow
    img = Image.open(input_path).convert("RGBA")
    
    if USE_OPENCV:
        # Convert to cv2 image for advanced processing
        cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGBA2BGRA)
        
        # Ensure blur_strength is odd
        blur_strength = blur_strength if blur_strength % 2 == 1 else blur_strength + 1
        
        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(cv_img, (blur_strength, blur_strength), 0)
        
        # Convert back to Pillow image
        final_img = Image.fromarray(cv2.cvtColor(blurred, cv2.COLOR_BGRA2RGBA))
    else:
        # Use Pillow's blur if OpenCV is not available
        final_img = img.filter(ImageFilter.GaussianBlur(blur_strength / 2))
    
    # Save the result
    final_img.save(output_path)

def process_images(input_dir='output', output_dir='OUTPUT_BLURRED'):
    if not os.path.exists(input_dir):
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    processed_count = 0
    
    for filename in os.listdir(input_dir):
        if is_image_file(filename):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, f"blurred_{filename}")
            
            try:
                apply_blur(input_path, output_path, blur_strength=41)  # You can change this value
                processed_count += 1
                print(f"Processed: {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    
    print(f"\nBlur effect applied. Processed {processed_count} images.")

if __name__ == "__main__":
    process_images()