import os
import sys
import difflib
from PIL import Image

# Add project root to path so we can import utils.ocr
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.ocr import perform_ocr

# Folder containing printed test images and ground truth text files
printed_folder = "evaluation/test_data/printed"

# Collect all image files (jpg, png)
image_files = [f for f in os.listdir(printed_folder) if f.lower().endswith((".jpg", ".png", ".jpeg"))]

# Track accuracy results
accuracies = []

print("🔍 Evaluating OCR Accuracy on Printed Text Images:\n")

for img_file in image_files:
    # Paths
    img_path = os.path.join(printed_folder, img_file)
    gt_path = os.path.join(printed_folder, os.path.splitext(img_file)[0] + ".txt")

    # Read ground truth
    if not os.path.exists(gt_path):
        print(f"⚠️ Skipping {img_file} – Ground truth file not found.")
        continue

    with open(gt_path, "r", encoding="utf-8") as f:
        ground_truth = f.read().strip()

    # Perform OCR
    try:
        image = Image.open(img_path)
        _, predicted_text, _ = perform_ocr(image)

        # Compute similarity
        similarity = difflib.SequenceMatcher(None, ground_truth.lower(), predicted_text.lower()).ratio()
        accuracies.append(similarity)

        print(f"✅ {img_file} Accuracy: {similarity * 100:.2f}%")
    except Exception as e:
        print(f"❌ Error processing {img_file}: {e}")

# Final average
if accuracies:
    avg_accuracy = sum(accuracies) / len(accuracies)
    print(f"\n📊 Average OCR Accuracy: {avg_accuracy * 100:.2f}%")
else:
    print("\n⚠️ No valid image/text pairs evaluated.")
