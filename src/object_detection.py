import torch
import torchvision.models.detection as detection
import torchvision.transforms as transforms
from PIL import Image
from pycocotools.coco import COCO
import requests

# load COCO categories
COCO_INSTANCE_CATEGORY_URL = "https://raw.githubusercontent.com/amikelive/coco-labels/master/coco-labels-paper.txt"
response = requests.get(COCO_INSTANCE_CATEGORY_URL)
COCO_LABELS = [name.strip() for name in response.text.splitlines()]

# import R-CNN object detection model
model = detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# processing transformations
preprocess = transforms.Compose([
    transforms.Resize((800, 1333)), # Resize while maintaining aspect ratio
    transforms.ToTensor()
])

def detect_objects(image_path):
    image = Image.open(image_path)

    # process the image
    image_tensor = preprocess(image)
    image_tensor = image_tensor.unsqueeze(0)

    # object detection
    with torch.no_grad():
        prediction = model(image_tensor)

    # labels, confidence scores, and bounding boxes
    labels = prediction[0]['labels']
    scores = prediction[0]['scores']
    boxes = prediction[0]['boxes']

    # convert to lists for simplicity
    detected_objects = [{'label': COCO_LABELS[label.item()], 'confidence': score.item(), 'bbox': box.tolist()} for label, score, box in zip(labels, scores, boxes) if score.item() > 0.9]  # Confidence threshold
    
    return detected_objects