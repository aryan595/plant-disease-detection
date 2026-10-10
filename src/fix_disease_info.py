
import json
import re
import shutil
from pathlib import Path

import torch

from update_disease_info import NEW_DISEASE_INFO


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INFO_FILE = PROJECT_ROOT / "app" / "disease_info.json"

CHECKPOINT_FILE = (
    PROJECT_ROOT
    / "models"
    / "efficientnet_b0_combined_55class.pth"
)

BACKUP_FILE = (
    PROJECT_ROOT
    / "app"
    / "disease_info.backup.json"
)


# =========================================
# Normalize class names
# =========================================

def normalize_name(name):
    return re.sub(
        r"[^a-z0-9]",
        "",
        name.lower(),
    )


# =========================================
# Generic fallback information
# =========================================

def make_generic_info(class_name):

    plant, separator, disease = class_name.partition("___")

    plant = plant.replace("_", " ").strip()
    disease = disease.replace("_", " ").strip()

    if not separator:
        disease = "Unknown"

    if disease.lower() == "healthy":

        description = (
            f"The model classified this image as a healthy "
            f"{plant} leaf. This prediction does not rule out "
            "every possible plant health problem."
        )

        symptoms = [
            "No major disease symptoms were identified by the model.",
            "Inspect the leaf for unusual spots, discoloration, "
            "wilting, or distortion.",
        ]

        management = [
            "Continue routine crop scouting.",
            "Maintain suitable growing conditions.",
        ]

        prevention = [
            "Use healthy planting material.",
            "Monitor plants regularly.",
            "Maintain appropriate crop-management practices.",
        ]

    else:

        description = (
            f"The model classified this image as {disease} "
            f"on {plant}. This is an AI prediction, not a "
            "confirmed diagnosis."
        )

        symptoms = [
            "Inspect the leaf for spots, discoloration, "
            "lesions, or other unusual changes.",
            "Symptoms can overlap with other diseases or "
            "environmental problems.",
        ]

        management = [
            "Confirm the suspected condition before treatment.",
            "Consult a qualified local agricultural specialist.",
            "Follow regionally appropriate crop-management guidance.",
        ]

        prevention = [
            "Use healthy planting material.",
            "Monitor plants regularly.",
            "Maintain suitable crop and field sanitation practices.",
        ]

    return {
        "plant": plant,
        "disease": disease,
        "description": description,
        "symptoms": symptoms,
        "management": management,
        "prevention": prevention,
    }


# =========================================
# Main
# =========================================

def main():

    if not INFO_FILE.is_file():
        raise FileNotFoundError(
            f"Disease information file not found: {INFO_FILE}"
        )

    if not CHECKPOINT_FILE.is_file():
        raise FileNotFoundError(
            f"Model checkpoint not found: {CHECKPOINT_FILE}"
        )

    # -------------------------------------
    # Load the exact model class mapping
    # -------------------------------------

    checkpoint = torch.load(
        CHECKPOINT_FILE,
        map_location="cpu",
        weights_only=False,
    )

    class_to_idx = {
        name: int(index)
        for name, index in checkpoint["class_to_idx"].items()
    }

    model_classes = set(class_to_idx)

    print("Model classes:", len(model_classes))

    # -------------------------------------
    # Load existing information
    # -------------------------------------

    with open(
        INFO_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        original_info = json.load(file)

    if not isinstance(original_info, dict):
        raise ValueError(
            "disease_info.json must contain a JSON object."
        )

    # Work on a separate in-memory copy.
    updated_info = dict(original_info)

    # -------------------------------------
    # Validate new entries
    # -------------------------------------

    unknown_new = (
        set(NEW_DISEASE_INFO) - model_classes
    )

    if unknown_new:
        raise ValueError(
            "New information entries do not match the model: "
            f"{sorted(unknown_new)}"
        )

    # Add new crop information without overwriting existing entries.
    added_new_entries = 0

    for class_name, information in NEW_DISEASE_INFO.items():

        if class_name not in updated_info:
            updated_info[class_name] = information
            added_new_entries += 1

    print(
        "New crop entries added:",
        added_new_entries,
    )

    # -------------------------------------
    # Reconcile formatting mismatches
    # -------------------------------------

    aliases_fixed = 0

    for class_name in sorted(model_classes):

        if class_name in updated_info:
            continue

        normalized_target = normalize_name(class_name)

        aliases = [
            existing_name
            for existing_name in updated_info
            if normalize_name(existing_name) == normalized_target
        ]

        if len(aliases) == 1:

            old_name = aliases[0]

            updated_info[class_name] = updated_info.pop(
                old_name
            )

            print(
                f"Reconciled class label:\n"
                f"  {old_name}\n"
                f"  -> {class_name}"
            )

            aliases_fixed += 1

        else:

            # Do not guess disease-specific facts when no clear
            # existing label matches.
            updated_info[class_name] = make_generic_info(
                class_name
            )

            print(
                "Added generic fallback information:",
                class_name,
            )

    # -------------------------------------
    # Final validation
    # -------------------------------------

    missing = (
        model_classes - set(updated_info)
    )

    if missing:
        raise ValueError(
            f"Missing model class information: {sorted(missing)}"
        )

    if not BACKUP_FILE.exists():

        shutil.copy2(
            INFO_FILE,
            BACKUP_FILE,
        )

        print("\nBackup created:", BACKUP_FILE)

    # -------------------------------------
    # Write safely
    # -------------------------------------

    temporary_file = INFO_FILE.with_suffix(".tmp")

    with open(
        temporary_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            updated_info,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write("\n")

    temporary_file.replace(INFO_FILE)

    # -------------------------------------
    # Summary
    # -------------------------------------

    extra_keys = (
        set(updated_info) - model_classes
    )

    print("\n" + "=" * 60)
    print("DISEASE INFORMATION UPDATE COMPLETE")
    print("=" * 60)

    print("Model classes:", len(model_classes))
    print("Total information entries:", len(updated_info))
    print("New crop entries added:", added_new_entries)
    print("Formatting mismatches reconciled:", aliases_fixed)
    print("Extra non-model entries retained:", len(extra_keys))
    print("Updated file:", INFO_FILE)
    print("Backup file:", BACKUP_FILE)


if __name__ == "__main__":
    main()
