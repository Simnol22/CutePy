from PIL import Image, ImageDraw
import os 

def create_circle_mask(size):
    # Créer une nouvelle image de taille 'size' avec un fond transparent
    mask = Image.new('L', size, 0)
    # Créer un dessin pour dessiner le cercle
    draw = ImageDraw.Draw(mask)
    # Dessiner un cercle blanc solide au centre de l'image
    draw.ellipse([(0, 0), size], fill=255)

    return mask

def apply_mask(image, mask):
    result = Image.new('RGBA', image.size)
    result.paste(image, (0, 0), mask)
    return result

def compass_mask(image):
    mask = create_circle_mask(image.size)
    image_with_mask = apply_mask(image, mask)
    return(image_with_mask)