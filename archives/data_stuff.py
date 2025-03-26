import torch
import torchvision
from torch.utils.data import Dataset
import pandas as pd
from PIL import Image

from torchvision.transforms import Compose, Normalize, ToTensor, Resize


class Transforms:

    def __init__(self, image_processor, img_size):
        normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)
        # _transforms = Compose([RandomResizedCrop(size), ToTensor(), normalize])
        resize = Resize((img_size, img_size))
        self._transforms = Compose([ToTensor(), normalize, resize])
        self.img_size = img_size

    def __call__(self, image):
        return self._transforms(image)


class CSVDataset(Dataset):

    def __init__(self, csv_path, transforms):
        self.df = pd.read_csv(csv_path)
        self.transforms = transforms

        self.samples = list(zip(
            self.df['image'],
            self.df['label'],
            self.df['video'],
            self.df['split'],
        ))

    def __getitem__(self, index):
        success = False
        while not success:
            try:
                fp, label, video, _ = self.samples[index]
                image = Image.open(fp)
                image = self.transforms(image)
                success = True
            except Exception as e:
                print(f'Failed to extract or transform image {fp} at index {index}, \
                      desperately attempting a new index:')
                if index == len(self.samples) - 1:
                    index -= 1
                else:
                    index += 1
                print('New index', index)

        return {
            'pixel_values': image,
            'label': label,
        }
    
    def __len__(self):
        return len(self.samples)
    
# class Dataset(CSVHFDataset):
#     pass 
    # to satiate hf evaluator's stupid demands