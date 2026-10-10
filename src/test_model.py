import torch

from plant_model import create_model


# ---------------------------------
# Device
# ---------------------------------
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)

if device.type == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))


# ---------------------------------
# Create model
# ---------------------------------
model = create_model(
    num_classes=38,
    freeze_backbone=True
)

model = model.to(device)

model.eval()


# ---------------------------------
# Create dummy input
# ---------------------------------
dummy_input = torch.randn(
    2,
    3,
    224,
    224
).to(device)


# ---------------------------------
# Forward pass
# ---------------------------------
with torch.no_grad():
    output = model(dummy_input)


# ---------------------------------
# Print results
# ---------------------------------
print()
print("Model created successfully!")

print("Input shape :", dummy_input.shape)
print("Output shape:", output.shape)

print()
print("Expected output shape:")
print("[batch_size, number_of_classes]")
print("[2, 38]")