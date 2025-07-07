# import os
# from PIL import Image
# import imagehash

# def remove_duplicate_images(folder, threshold=5):
#     images = sorted(os.listdir(folder))
#     prev_hash = None
#     for img in images:
#         img_path = os.path.join(folder, img)
#         try:
#             hash = imagehash.average_hash(Image.open(img_path))
#         except Exception as e:
#             print(f"Skipping unreadable file: {img_path} ({e})")
#             continue

#         if prev_hash and abs(hash - prev_hash) < threshold:
#             print(f"Deleting duplicate: {img_path}")
#             os.remove(img_path)
#         else:
#             prev_hash = hash

# def remove_duplicates_in_all_subfolders(base_folder="data/frames", threshold=5):
#     for subfolder in os.listdir(base_folder):
#         subfolder_path = os.path.join(base_folder, subfolder)
#         if os.path.isdir(subfolder_path):
#             print(f"\n Processing folder: {subfolder_path}")
#             remove_duplicate_images(subfolder_path, threshold=threshold)

# if __name__ == "__main__":
#     remove_duplicates_in_all_subfolders()

import os
from PIL import Image
import imagehash

def remove_duplicate_images(folder, threshold=5):
    """
    Remove near-duplicate images from a given folder using perceptual hashing.
    
    Args:
        folder (str): Path to the folder containing images.
        threshold (int): Maximum hash difference to consider images as duplicates.
    """
    images = sorted(os.listdir(folder))
    prev_hash = None
    deleted_count = 0
    total_images = len(images)

    for img in images:
        img_path = os.path.join(folder, img)

        try:
            hash = imagehash.average_hash(Image.open(img_path))
        except Exception as e:
            print(f"Skipping unreadable file: {img_path} ({e})")
            continue

        if prev_hash and abs(hash - prev_hash) < threshold:
            print(f"Deleting duplicate: {img_path}")
            os.remove(img_path)
            deleted_count += 1
        else:
            prev_hash = hash

    print(f"Processed {folder}: {total_images} images → {total_images - deleted_count} kept, {deleted_count} deleted.")

def remove_duplicates_in_all_subfolders(base_folder="data/frames", threshold=5):
    """
    Apply duplicate image removal to all subfolders inside a base folder.
    
    Args:
        base_folder (str): Base directory containing subfolders of frames.
        threshold (int): Hash difference threshold for similarity.
    """
    for subfolder in sorted(os.listdir(base_folder)):
        subfolder_path = os.path.join(base_folder, subfolder)
        if os.path.isdir(subfolder_path):
            print(f"\n🔍 Processing folder: {subfolder_path}")
            remove_duplicate_images(subfolder_path, threshold=threshold)

if __name__ == "__main__":
    remove_duplicates_in_all_subfolders()

