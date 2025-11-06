#!/usr/bin/env python3
from PIL import Image
import os

def resize_image_keep_aspect(image_path, max_size=1024):
    """
    Redimensionne une image pour que le côté le plus long soit de max_size pixels
    en gardant le ratio d'aspect.
    """
    try:
        # Ouvrir l'image
        img = Image.open(image_path)

        # Obtenir les dimensions actuelles
        width, height = img.size

        # Déterminer le côté le plus long
        if width > height:
            # Le côté long est la largeur
            new_width = max_size
            new_height = int((height / width) * max_size)
        else:
            # Le côté long est la hauteur
            new_height = max_size
            new_width = int((width / height) * max_size)

        # Redimensionner l'image avec un bon filtre de qualité
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Sauvegarder l'image (écraser l'originale)
        img_resized.save(image_path, quality=95, optimize=True)

        return f"{os.path.basename(image_path)}: {width}x{height} -> {new_width}x{new_height}"

    except Exception as e:
        return f"Erreur pour {image_path}: {str(e)}"

# Redimensionner toutes les images de 1.jpg à 147.jpg
base_dir = '/home/user/aishahLora'
os.chdir(base_dir)

print("Début du redimensionnement des images...")
print("=" * 60)

for i in range(1, 148):
    image_path = os.path.join(base_dir, f"{i}.jpg")
    if os.path.exists(image_path):
        result = resize_image_keep_aspect(image_path, max_size=1024)
        print(result)
    else:
        print(f"Image {i}.jpg non trouvée")

print("=" * 60)
print("Redimensionnement terminé !")
