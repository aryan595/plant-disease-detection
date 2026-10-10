from pathlib import Path
import json

from PIL import Image
from torch.utils.data import Dataset


class PlantDiseaseDataset(Dataset):
    """
    PyTorch Dataset for the PlantVillage dataset.

    Each line in the split file contains a relative image path,
    for example:

    raw/color/Tomato___Early_blight/image.JPG

    The folder name is used as the class label.
    """

    def __init__(
        self,
        split_file,
        dataset_root,
        class_to_idx=None,
        transform=None,
    ):
        self.split_file = Path(split_file)
        self.dataset_root = Path(dataset_root)
        self.transform = transform

        # ---------------------------------
        # Read image paths
        # ---------------------------------
        with open(self.split_file, "r", encoding="utf-8") as f:
            self.image_paths = [
                line.strip()
                for line in f
                if line.strip()
            ]

        # ---------------------------------
        # Create class mapping
        # ---------------------------------
        if class_to_idx is None:
            classes = sorted(
                self._get_class_name(path)
                for path in self.image_paths
            )

            self.classes = sorted(set(classes))

            self.class_to_idx = {
                class_name: index
                for index, class_name in enumerate(self.classes)
            }

        else:
            self.class_to_idx = class_to_idx
            self.classes = [
                class_name
                for class_name, _ in sorted(
                    class_to_idx.items(),
                    key=lambda item: item[1]
                )
            ]

        # ---------------------------------
        # Convert paths to labels
        # ---------------------------------
        self.labels = [
            self.class_to_idx[self._get_class_name(path)]
            for path in self.image_paths
        ]

    @staticmethod
    def _get_class_name(image_path):
        """
        Extract class name from:

        raw/color/Tomato___Early_blight/image.JPG

        → Tomato___Early_blight
        """

        parts = image_path.replace("\\", "/").split("/")

        if len(parts) < 4:
            raise ValueError(
                f"Unexpected image path: {image_path}"
            )

        return parts[2]

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, index):

        relative_path = self.image_paths[index]

        image_path = self.dataset_root / relative_path

        # ---------------------------------
        # Load image
        # ---------------------------------
        image = Image.open(image_path).convert("RGB")

        label = self.labels[index]

        # ---------------------------------
        # Apply transforms
        # ---------------------------------
        if self.transform is not None:
            image = self.transform(image)

        return image, label

    def save_class_mapping(self, output_file):

        output_file = Path(output_file)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.class_to_idx,
                f,
                indent=4
            )