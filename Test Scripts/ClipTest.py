import os
import clip
from PIL import Image
import torch
import torchvision.transforms as transforms

# Load the model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# # Prepare Image
# cifar100 = CIFAR100(root=os.path.expanduser("~/.cache"), download=True, train=False)

# Prepare the inputs
image_path = "Placeholder.png"  # Replace with the path to your image
image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)


# Prepare text descriptions for zero-shot classification
class_descriptions = ["describe this stock photo"]
text_inputs = clip.tokenize(class_descriptions).to(device)

# Calculate features
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text_inputs)

# Pick the top 5 most similar labels for the image
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)
similarity = (100.0 * image_features @ text_features.T).softmax(dim=-1)

# Print the result
print("\nAnalysis:\n" + similarity.item())
