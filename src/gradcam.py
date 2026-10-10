from pathlib import Path
import sys

import numpy as np
import torch
import torch.nn.functional as F

from PIL import Image
import matplotlib.pyplot as plt

from plant_model import create_model
from image_transforms import val_test_transforms


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "efficientnet_b0_finetuned.pth"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "gradcam_result.png"
)


# =========================================
# Check argument
# =========================================

if len(sys.argv) != 2:

    print()
    print("Usage:")
    print(
        'python src/gradcam.py "path\\to\\image.jpg"'
    )
    print()

    sys.exit(1)


image_path = Path(sys.argv[1])


if not image_path.exists():

    print()
    print(
        f"ERROR: Image not found:\n{image_path}"
    )
    print()

    sys.exit(1)


# =========================================
# Device
# =========================================

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


print("Device:", device)

if device.type == "cuda":

    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# =========================================
# Load checkpoint
# =========================================

print()
print("Loading model...")

checkpoint = torch.load(
    MODEL_FILE,
    map_location=device,
)


class_to_idx = checkpoint["class_to_idx"]

classes = [
    class_name
    for class_name, _ in sorted(
        class_to_idx.items(),
        key=lambda item: item[1],
    )
]


# =========================================
# Create model
# =========================================

model = create_model(
    num_classes=len(classes),
    freeze_backbone=False,
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(device)

model.eval()


# =========================================
# Grad-CAM storage
# =========================================

activations = None
gradients = None


# =========================================
# Hooks
# =========================================

def forward_hook(module, input, output):
    global activations
    activations = output


def backward_hook(module, grad_input, grad_output):
    global gradients
    gradients = grad_output[0]


# EfficientNet final feature block
target_layer = model.features[-1]


forward_handle = target_layer.register_forward_hook(
    forward_hook
)

backward_handle = target_layer.register_full_backward_hook(
    backward_hook
)


# =========================================
# Load original image
# =========================================

print("Loading image...")

original_image = Image.open(
    image_path
).convert("RGB")


# =========================================
# Transform
# =========================================

input_tensor = val_test_transforms(
    original_image
)

input_tensor = input_tensor.unsqueeze(0)
input_tensor = input_tensor.to(device)


# =========================================
# Forward pass
# =========================================

model.zero_grad()

output = model(input_tensor)

probabilities = torch.softmax(
    output,
    dim=1
)

predicted_index = output.argmax(
    dim=1
).item()

predicted_probability = (
    probabilities[0, predicted_index].item()
    * 100
)


predicted_class = classes[
    predicted_index
]


print()
print("Prediction:", predicted_class)

print(
    f"Confidence: {predicted_probability:.2f}%"
)


# =========================================
# Backward pass
# =========================================

target_score = output[
    0,
    predicted_index
]

target_score.backward()


# =========================================
# Grad-CAM calculation
# =========================================

# Remove batch dimension
activation = activations[0]

gradient = gradients[0]


# Global average pooling over
# spatial dimensions

weights = gradient.mean(
    dim=(1, 2)
)


# Weighted sum of feature maps

cam = torch.zeros(
    activation.shape[1:],
    device=device,
)


for channel in range(
    activation.shape[0]
):

    cam += (
        weights[channel]
        * activation[channel]
    )


# ReLU

cam = F.relu(cam)


# Normalize

cam -= cam.min()

if cam.max() > 0:

    cam /= cam.max()


# =========================================
# Convert heatmap to NumPy
# =========================================

cam = cam.detach().cpu().numpy()


# =========================================
# Resize heatmap
# =========================================

original_width, original_height = (
    original_image.size
)

heatmap = Image.fromarray(
    np.uint8(cam * 255)
)

heatmap = heatmap.resize(
    (
        original_width,
        original_height,
    ),
    Image.Resampling.BILINEAR,
)


heatmap = np.array(
    heatmap
) / 255.0


# =========================================
# Create visualization
# =========================================

fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 5),
)


# Original image

axes[0].imshow(
    original_image
)

axes[0].set_title(
    "Original Image"
)

axes[0].axis("off")


# Grad-CAM

axes[1].imshow(
    original_image
)

axes[1].imshow(
    heatmap,
    alpha=0.5,
    cmap="jet",
)

axes[1].set_title(
    f"Grad-CAM\n{predicted_class}"
)

axes[1].axis("off")


plt.tight_layout()


# =========================================
# Save
# =========================================

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

plt.savefig(
    OUTPUT_FILE,
    dpi=200,
    bbox_inches="tight",
)

plt.show()


# =========================================
# Remove hooks
# =========================================

forward_handle.remove()
backward_handle.remove()


print()
print("Grad-CAM generated successfully!")

print(
    "Saved to:",
    OUTPUT_FILE
)