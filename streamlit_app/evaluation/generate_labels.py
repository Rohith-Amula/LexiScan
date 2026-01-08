import os
import pandas as pd

# Base directory where digit subfolders (0 to 9) are stored
base_dir = 'evaluation/digit_test_data'
labels = []

# Go through each digit folder (0–9)
for label in range(10):
    label_folder = os.path.join(base_dir, str(label))
    if not os.path.exists(label_folder):
        print(f"⚠️ Skipping missing folder: {label_folder}")
        continue

    for file in os.listdir(label_folder):
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            relative_path = os.path.join(str(label), file)  # store subfolder too
            labels.append({'filename': relative_path, 'label': label})

# Save to CSV
df = pd.DataFrame(labels)
output_csv = os.path.join(base_dir, 'labels.csv')
df.to_csv(output_csv, index=False)

print(f"✅ labels.csv created with {len(df)} entries at {output_csv}")
