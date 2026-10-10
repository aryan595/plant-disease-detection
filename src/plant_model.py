import torch
import torch.nn as nn

from torchvision.models import (
    efficientnet_b0,
    EfficientNet_B0_Weights,
)


NUM_CLASSES = 38


def create_model(num_classes=NUM_CLASSES, freeze_backbone=True):
    """
    Create an ImageNet-pretrained EfficientNet-B0
    and replace its classifier for our 38 plant-disease classes.
    """

    # Load ImageNet-pretrained EfficientNet-B0
    weights = EfficientNet_B0_Weights.DEFAULT

    model = efficientnet_b0(weights=weights)

    # ---------------------------------
    # Freeze backbone
    # ---------------------------------
    if freeze_backbone:
        for parameter in model.features.parameters():
            parameter.requires_grad = False

    # ---------------------------------
    # Replace final classifier
    # ---------------------------------
    input_features = model.classifier[1].in_features

    model.classifier[1] = nn.Linear(
        input_features,
        num_classes
    )

    return model