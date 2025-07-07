import os
import cv2

def extract_frames(video_dir="data/videos", output_dir="data/frames", step=30):
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported video extensions (case-insensitive)
    valid_extensions = {".mp4", ".mov", ".avi", ".mkv"}

    for file in os.listdir(video_dir):
        ext = os.path.splitext(file)[1].lower()
        if ext in valid_extensions:
            video_path = os.path.join(video_dir, file)
            cap = cv2.VideoCapture(video_path)
            
            if not cap.isOpened():
                print(f"Could not open {file}")
                continue

            video_name = os.path.splitext(file)[0]
            save_dir = os.path.join(output_dir, video_name)
            os.makedirs(save_dir, exist_ok=True)

            frame_id = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_id % step == 0:
                    frame_file = f"frame_{frame_id:05d}.jpg"
                    cv2.imwrite(os.path.join(save_dir, frame_file), frame)
                frame_id += 1

            cap.release()
            print(f"Extracted frames from {file} to {save_dir}")

if __name__ == "__main__":
    extract_frames()
