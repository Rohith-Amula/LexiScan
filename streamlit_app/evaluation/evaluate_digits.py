import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, accuracy_score

# ✅ Correct test data path
test_dir = 'evaluation/digit_test_data/'

# Load the trained digit model
model = load_model('saved_model/model.h5')

y_true = []
y_pred = []

print("🔍 Evaluating handwritten digit images...\n")

# Loop through folders named 0 to 9
for label in sorted(os.listdir(test_dir)):
    label_path = os.path.join(test_dir, label)
    if not os.path.isdir(label_path):
        continue  # skip files

    for file in os.listdir(label_path):
        file_path = os.path.join(label_path, file)
        try:
            img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (28, 28))
            img = img / 255.0
            if np.mean(img) > 0.5:
                img = 1 - img
            img = img.reshape(1, 28, 28, 1)

            prediction = model.predict(img)
            predicted_label = np.argmax(prediction)

            y_true.append(int(label))
            y_pred.append(predicted_label)
        except Exception as e:
            print(f"⚠️ Skipping {file}: {e}")

# Accuracy
if y_true:
    acc = accuracy_score(y_true, y_pred)
    print(f"\n✅ Digit Classifier Accuracy: {acc:.2%}")

    # Bar Chart
    labels_unique = list(range(10))
    correct = [sum((np.array(y_true) == lbl) & (np.array(y_pred) == lbl)) for lbl in labels_unique]

    plt.figure(figsize=(8, 5))
    plt.bar([str(i) for i in labels_unique], correct, color='skyblue')
    plt.title("Correct Predictions Per Digit")
    plt.xlabel("Digit")
    plt.ylabel("Correct Predictions")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("evaluation/digit_accuracy_bar.png")
    plt.show()

    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels_unique)
    disp.plot(cmap=plt.cm.Blues)
    plt.title("Confusion Matrix - Handwritten Digit Classifier")
    plt.tight_layout()
    plt.savefig("evaluation/confusion_matrix.png")
    plt.show()
else:
    print("❌ No valid test data found. Please check your folder structure and images.")
