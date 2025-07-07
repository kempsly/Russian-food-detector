from PIL import Image
import imagehash
import os

def find_duplicates(image_dir):
    hashes = {}
    duplicates = []

    for filename in os.listdir(image_dir):
        if filename.endswith((".jpg", ".png")):
            filepath = os.path.join(image_dir, filename)
            with Image.open(filepath) as img:
                img_hash = str(imagehash.average_hash(img))
                if img_hash in hashes:
                    duplicates.append(filename)
                else:
                    hashes[img_hash] = filename

    return duplicates

# Пример использования 
image_dir = 'data/frames_/4_1'
duplicates = find_duplicates(image_dir)
print("Duplicates found:", duplicates)
