import hashlib
from pathlib import Path

def clean_and_rename(folder_path):
    folder = Path(folder_path)
    seen = set()
    unique_files = []

    # Step 1: Find all unique real images
    for img in folder.glob("*.*"):
        if img.suffix.lower() not in ['.jpg','.jpeg','.png','.webp']:
            continue
        if img.stat().st_size < 10240: # delete your 1KB fake files
            img.unlink()
            continue
            
        h = hashlib.md5(img.read_bytes()).hexdigest()
        if h in seen:
            img.unlink()
            print(f"Deleted duplicate: {img.name}")
        else:
            seen.add(h)
            unique_files.append(img)

    # Step 2: Rename all to temp first to avoid clash
    temp_files = []
    for i, img in enumerate(unique_files):
        temp_name = folder / f"temp_{i}.jpg"
        img.rename(temp_name)
        temp_files.append(temp_name)

    # Step 3: Now rename temp -> 1.jpg, 2.jpg, 3.jpg
    for count, temp_img in enumerate(temp_files, start=1):
        final_name = folder / f"{count}.jpg"
        temp_img.rename(final_name)
    
    print(f"Done! Renamed {len(temp_files)} images to 1 to {len(temp_files)}")

# CHANGE THIS PATH ONLY
folder = r"C:\ARUN\HOPE AI\11_Deep Learning\Snow Chain Detection\dataset\with_sc"
clean_and_rename(folder)