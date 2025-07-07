import os
import cv2
import albumentations as A
from tqdm import tqdm
import shutil

# Paths
images_dir = "data/data_to_augment/images"
labels_dir = "data/data_to_augment/labels"
aug_images_dir = "data/augmented/images"
aug_labels_dir = "data/augmented/labels"

# Number of augmented versions per original
n_aug = 3

# Class names (for reference only)
classes = [
    "daikon_salad",
    "greek_salad",
    "shashlik",
    "wrap",
    "green_tea",
    "Borscht",
    "cheese_soup",
    "fondue"
]

# Ensure output directories exist
os.makedirs(aug_images_dir, exist_ok=True)
os.makedirs(aug_labels_dir, exist_ok=True)

# Augmentation pipeline
augmentation = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.05, scale_limit=0.2, rotate_limit=15, p=0.7),
    A.MotionBlur(p=0.2),
    A.HueSaturationValue(p=0.3),
    A.Resize(640, 640)
], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))

# Process each image
image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(".jpg")]

for img_file in tqdm(image_files, desc="Augmenting"):
    name = os.path.splitext(img_file)[0]
    img_path = os.path.join(images_dir, img_file)
    label_path = os.path.join(labels_dir, name + ".txt")

    image = cv2.imread(img_path)
    if image is None:
        continue

    # Save original image with "_orig" suffix
    orig_img_name = f"{name}_orig.jpg"
    cv2.imwrite(os.path.join(aug_images_dir, orig_img_name), image)

    # Copy original label (if it exists)
    if os.path.isfile(label_path):
        orig_label_path = os.path.join(aug_labels_dir, f"{name}_orig.txt")
        shutil.copy(label_path, orig_label_path)

    # Load labels
    boxes = []
    labels_list = []
    if os.path.isfile(label_path):
        with open(label_path, "r") as lf:
            for line in lf:
                parts = line.strip().split()
                if len(parts) == 5:
                    cls_id = int(parts[0])
                    bbox = list(map(float, parts[1:]))
                    boxes.append(bbox)
                    labels_list.append(cls_id)

    # Apply augmentations
    for i in range(n_aug):
        aug = augmentation(image=image, bboxes=boxes, class_labels=labels_list)
        aug_img = aug["image"]
        aug_boxes = aug["bboxes"]
        aug_labels = aug["class_labels"]

        out_img_name = f"{name}_aug{i}.jpg"
        out_label_name = out_img_name.replace(".jpg", ".txt")

        cv2.imwrite(os.path.join(aug_images_dir, out_img_name), aug_img)

        with open(os.path.join(aug_labels_dir, out_label_name), "w") as out_f:
            for label, box in zip(aug_labels, aug_boxes):
                box_str = " ".join(f"{x:.6f}" for x in box)
                out_f.write(f"{label} {box_str}\n")

print("Done: Originals and augmentations saved.")
