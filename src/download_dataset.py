from datasets import load_dataset

print("Downloading PlantVillage dataset...")

dataset = load_dataset("mohanty/PlantVillage")

print("\nDownload complete!")
print(dataset)