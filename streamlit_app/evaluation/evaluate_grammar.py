import os
import sys
import difflib
import pandas as pd

# Add root directory to sys.path for module import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from utils.corrector import correct_text
except ImportError:
    print("❌ Could not import 'correct_text' from utils.corrector.")
    sys.exit(1)

# Path to the grammar test CSV file
csv_file = "evaluation/test_data/grammar.csv"

# Validate file existence
if not os.path.exists(csv_file):
    print(f"❌ File not found: {csv_file}")
    sys.exit(1)

# Load test dataset
df = pd.read_csv(csv_file)

# Ensure necessary columns exist
if "input" not in df.columns or "expected" not in df.columns:
    print("❌ CSV must contain 'input' and 'expected' columns.")
    sys.exit(1)

accuracies = []

print("🔍 Evaluating Grammar Correction Accuracy:\n")

# Iterate over all samples
for idx, row in df.iterrows():
    raw_text = str(row["input"]).strip()
    expected = str(row["expected"]).strip()

    try:
        corrected = correct_text(raw_text).strip()
        similarity = difflib.SequenceMatcher(None, corrected.lower(), expected.lower()).ratio()
        accuracies.append(similarity)

        print(f"✅ Sample {idx + 1}:")
        print(f"   Input     : {raw_text}")
        print(f"   Corrected : {corrected}")
        print(f"   Expected  : {expected}")
        print(f"   Similarity: {similarity * 100:.2f}%\n")

    except Exception as e:
        print(f"❌ Error at Sample {idx + 1}: {e}")

# Final average accuracy
if accuracies:
    avg_acc = sum(accuracies) / len(accuracies)
    print(f"\n📊 Average Grammar Correction Accuracy: {avg_acc * 100:.2f}%")
else:
    print("⚠️ No valid data samples evaluated.")
