import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

# Define the Model
class DigitClassifier(nn.Module):
    def __init__(self):
        super(DigitClassifier, self).__init__()
        
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        
        self.fc1_input_size = 64 * 7 * 7  # Adjust this based on input image size
        
        self.fc1 = nn.Linear(self.fc1_input_size, 128)
        self.fc2 = nn.Linear(128, 10)
    
    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.max_pool2d(x, 2)
        x = torch.relu(self.conv2(x))
        x = torch.max_pool2d(x, 2)
        
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        
        return x

# Load the trained model
model = DigitClassifier()
model.load_state_dict(torch.load("models/mnist_digit_classifier.pth"))
model.eval()

# Preprocessing transformations for the digit images
transform = transforms.Compose([
    transforms.Grayscale(num_output_channels=1),
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

def classify_digit_image(image: Image):
    # Preprocess the image
    digit_tensor = transform(image).unsqueeze(0)
    
    # Predict the digit
    with torch.no_grad():
        output = model(digit_tensor)
        _, predicted = torch.max(output, 1)
    
    return predicted.item()

