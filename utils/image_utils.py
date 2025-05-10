# forum/image_utils.py
from PIL import Image
import io
from django.core.files.base import ContentFile

def optimize_image(image_file, max_size=(300, 300), format='JPEG', quality=85):
    """
    Resize and optimize an image file
    
    Args:
        image_file: Django UploadedFile instance
        max_size: Maximum dimensions (width, height)
        format: Output image format (JPEG, PNG)
        quality: JPEG quality (1-100)
        
    Returns:
        ContentFile with the optimized image
    """
    try:
        img = Image.open(image_file)
        
        # Convert to RGB if needed (for transparency handling)
        if img.mode != 'RGB' and format == 'JPEG':
            img = img.convert('RGB')
        
        # Calculate dimensions while maintaining aspect ratio
        img.thumbnail(max_size)
        
        # Save to in-memory file
        output = io.BytesIO()
        img.save(output, format=format, quality=quality)
        output.seek(0)
        
        return ContentFile(output.read())
    except Exception as e:
        print(f"Error optimizing image: {e}")
        return None

def create_favicon(image_field, sizes=[16, 32], format='ICO'):
    """
    Creates a favicon from an ImageField
    
    Args:
        image_field: Django ImageField instance
        sizes: List of favicon dimensions
        format: Output format (usually ICO)
        
    Returns:
        ContentFile with the favicon data
    """
    try:
        # Open the image
        with image_field.open('rb') as img_file:
            img = Image.open(img_file)
            
            # Create in-memory file for output
            output = io.BytesIO()
            
            # Convert to RGBA for transparency support
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
                
            # For ICO format, we create multiple sizes in one file
            img.save(output, format=format, sizes=[(s, s) for s in sizes])
            output.seek(0)
            
            return ContentFile(output.read())
    except Exception as e:
        print(f"Error creating favicon: {e}")
        return None