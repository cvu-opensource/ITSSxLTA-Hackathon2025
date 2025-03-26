from transformers import AutoModelForImageClassification, TrainingArguments, Trainer
import PIL
from transformers import AutoImageProcessor
from torchvision.transforms import Compose, Normalize, ToTensor, Resize
import torch

# --- MODEL STUFF ---

checkpoint = "my_awesome_model_more_balanced/checkpoint-1915"
image_processor = AutoImageProcessor.from_pretrained(checkpoint)
model = AutoModelForImageClassification.from_pretrained(
    checkpoint,
    # num_labels=2,
)
maximum_softness = torch.nn.Softmax(dim=1)

# --- DATA PREPROCESSING STUFF ---
img_size = 384  # only this size works rn sorry
normalize = Normalize(mean=image_processor.image_mean, std=image_processor.image_std)
resize = Resize((img_size, img_size))
_transforms = Compose([ToTensor(), resize, normalize])

def silly_collate(list_of_inputs: list):
    # print(list_of_inputs)
    assert isinstance(list_of_inputs, list), 'you gotta send in a list buddy'
    assert False not in [isinstance(input, torch.Tensor) for input in list_of_inputs], 'ayo smth ain a tensor here buddy'
    assert False not in [len(input.shape) == 3 for input in list_of_inputs], 'why ur input in list_of_inputs not 3 dim buddy'
    return torch.stack(list_of_inputs, dim=0)

# --- PUMP SOMETHING THRU ---
fps = ['my_awesome_model/0.jpg',
       '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/000329/0.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/001202/169.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/000342/58.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/000342/59.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/000342/20.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/000342/14.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/000342/57.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/000342/50.jpg',
      '/mnt/e/data/cadp/extracted_frames-002/extracted_frames/001202/163.jpg',
      ]
inputs = []
for fp in fps:
    img = PIL.Image.open(fp)
    input = _transforms(img)
    inputs.append(input)

collated = silly_collate(inputs)
print('collated shape', collated.shape)

output = model(collated)
print(output)
print(output['logits'])
print(maximum_softness(output['logits']))