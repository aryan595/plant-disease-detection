from pathlib import Path

import torch


# =========================================
# Find the existing fine-tuned checkpoint
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "models"
    / "efficientnet_b0_finetuned.pth"
)


def main():

    print("=" * 60)
    print("EXISTING MODEL CHECKPOINT INSPECTION")
    print("=" * 60)

    print("\nCheckpoint:", CHECKPOINT_PATH)

    if not CHECKPOINT_PATH.is_file():

        print("\nERROR: Checkpoint was not found.")

        print("Available model files:")

        models_dir = PROJECT_ROOT / "models"

        if models_dir.is_dir():

            for path in sorted(models_dir.glob("*.pth")):
                print("  ", path.name)

        return

    # Load checkpoint on CPU; do not modify it.
    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location="cpu",
    )

    print("\nCheckpoint loaded successfully.")
    print("Checkpoint type:", type(checkpoint).__name__)

    # -------------------------------------
    # Inspect checkpoint structure
    # -------------------------------------

    if not isinstance(checkpoint, dict):

        print("ERROR: Unexpected checkpoint format.")
        return

    print("\nTop-level keys:")

    for key in checkpoint.keys():
        print("  ", key)

    # -------------------------------------
    # Extract model weights
    # -------------------------------------

    state_dict = checkpoint.get(
        "model_state_dict",
        checkpoint.get("state_dict"),
    )

    if state_dict is None:

        # Handle a checkpoint that contains only model weights.
        if checkpoint and all(
            isinstance(value, torch.Tensor)
            for value in checkpoint.values()
        ):
            state_dict = checkpoint

        else:
            print(
                "\nERROR: Could not locate the model state dictionary."
            )
            return

    print("\nClassifier layer dimensions:")

    found_classifier = False

    for name, tensor in state_dict.items():

        if (
            "classifier" in name
            and name.endswith((".weight", ".bias"))
        ):

            print(
                f"  {name}: {tuple(tensor.shape)}"
            )

            found_classifier = True

    if not found_classifier:
        print("  No classifier parameters were found.")

    # -------------------------------------
    # Inspect class mapping
    # -------------------------------------

    class_to_idx = checkpoint.get("class_to_idx")

    print("\nSaved class mapping:")

    if not isinstance(class_to_idx, dict):

        print(
            "  No class_to_idx mapping found in the checkpoint."
        )

    else:

        print("  Number of classes:", len(class_to_idx))

        for class_name, index in sorted(
            class_to_idx.items(),
            key=lambda item: item[1],
        ):

            print(f"  {index:2d}: {class_name}")

    print("\nInspection completed.")
    print("The checkpoint was not modified.")


if __name__ == "__main__":
    main()