from tensorflow.keras.datasets import mnist
import matplotlib.pyplot as plt

(x_train, y_train), _ = mnist.load_data()
img = x_train[0]  # Pick the first digit image
plt.imsave("sample_digit.png", img, cmap='gray')
print("Saved sample digit as sample_digit.png")
