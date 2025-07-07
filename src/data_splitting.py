import os
import shutil
import random

# Параметры
source_images_dir = "data/augmented/images"
source_labels_dir = "data/augmented/labels"
target_base = "data/dataset"

# Пропорции
train_ratio = 0.7
val_ratio = 0.2 
# test = оставшиеся 0.1

# Создание целевой структуры
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(target_base, "images", split), exist_ok=True)
    os.makedirs(os.path.join(target_base, "labels", split), exist_ok=True)

# Получение всех изображений
image_files = [f for f in os.listdir(source_images_dir) if f.endswith(".jpg")]
random.shuffle(image_files)

n_total = len(image_files)
n_train = int(n_total * train_ratio)
n_val = int(n_total * val_ratio)

splits = {
    "train": image_files[:n_train],
    "val": image_files[n_train:n_train + n_val],
    "test": image_files[n_train + n_val:]
}

# Перемещение файлов
for split, files in splits.items():
    for img_file in files:
        label_file = img_file.replace(".jpg", ".txt")

        # Пути
        src_img = os.path.join(source_images_dir, img_file)
        src_lbl = os.path.join(source_labels_dir, label_file)

        dst_img = os.path.join(target_base, "images", split, img_file)
        dst_lbl = os.path.join(target_base, "labels", split, label_file)

        shutil.copyfile(src_img, dst_img)

        if os.path.exists(src_lbl):
            shutil.copyfile(src_lbl, dst_lbl)
        else:
            print(f"Аннотация отсутствует для {img_file}")

print("Разделение и структурирование завершено.")
