import os
import shutil

source_dir = "data/frames"
destination_dir = "data/all_frames_keep"

os.makedirs(destination_dir, exist_ok=True)

for folder_name in sorted(os.listdir(source_dir)):
    folder_path = os.path.join(source_dir, folder_name)
    if not os.path.isdir(folder_path):
        continue

    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith(('.jpg', '.jpeg', '.png')):
            old_path = os.path.join(folder_path, file)

            # Create a new filename with folder prefix: e.g. "3_1_frame_00030.jpg"
            new_filename = f"{folder_name}_{file}"
            new_path = os.path.join(destination_dir, new_filename)

            shutil.copy2(old_path, new_path)

print(f"All frames copied and renamed to: {destination_dir}")
