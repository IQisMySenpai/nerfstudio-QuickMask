import json
import math
from pydantic import BaseModel
from fastapi import FastAPI
import os
from PIL import Image, ImageDraw
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import numpy as np
import io
import copy
import uvicorn

app = FastAPI()


def load_dataset(path, make_safety_copy=True):
    # Load the transforms.json file
    try:
        with open(os.path.join(path, 'transforms.json'), 'r') as f:
            transform = json.load(f)
    except:
        return None

    if make_safety_copy and not os.path.exists(os.path.join(path, 'backup_masks')):
        print('Making a safety copy of the masks and transforms.json')
        transform_copy = copy.deepcopy(transform)
        # Create a backup folder
        os.makedirs(os.path.join(path, 'backup_masks'), exist_ok=True)

        # Loop through each frame and save the mask as a backup
        for i, frame in enumerate(transform_copy['frames']):
            if 'mask_path' in frame:
                mask_path = os.path.join(path, frame['mask_path'])
                mask_extension = os.path.splitext(mask_path)[1]
                backup_path = os.path.join(path, 'backup_masks', f'mask_{i}{mask_extension}')
                os.system(f'cp {mask_path} {backup_path}')
                frame['mask_path'] = os.path.relpath(backup_path, path)

        # Save the backup transforms.json
        with open(os.path.join(path, 'backup_transforms.json'), 'w') as f:
            json.dump(transform_copy, f, indent=4)

    dataset = {
        'framecount': len(transform['frames']),
        'frames': []
    }

    empty_masks = set()

    # Loop through each frame and load the data with index and path
    for i, frame in enumerate(transform['frames']):
        if 'file_path' not in frame:
            return None

        f = {
            'index': i,
            'image_path': os.path.join(path, frame['file_path']),
            'quickmask_path': None,
            'reference': frame
        }

        if 'mask_path' in frame:
            # Check if the mask image is completely white: if so, it's not a mask
            mask_path = os.path.join(path, frame['mask_path'])
            mask = Image.open(mask_path).convert('L')
            if mask.getextrema() == (255, 255):
                # Get width and height of the image
                image = Image.open(f['image_path'])
                width, height = image.size
                image.close()
                empty_masks.add(f'{width}x{height}')
                f['quickmask_path'] = os.path.relpath(
                    os.path.join(path, 'empty_masks', f'empty_mask_{width}x{height}.jpeg'), path)
            else:
                f['mask_path'] = mask_path
            mask.close()
        else:
            # Get width and height of the image
            image = Image.open(f['image_path'])
            width, height = image.size
            image.close()
            empty_masks.add(f'{width}x{height}')
            f['quickmask_path'] = os.path.relpath(os.path.join(path, 'empty_masks', f'empty_mask_{width}x{height}.jpeg'), path)

        dataset['frames'].append(f)

    if len(empty_masks) > 0:
        os.makedirs(os.path.join(path, 'empty_masks'), exist_ok=True)

        for size in empty_masks:
            # Create a white mask image
            width, height = map(int, size.split('x'))
            mask = Image.new("L", (width, height), 255)
            mask_path = os.path.join(path, 'empty_masks', f'empty_mask_{size}.jpeg')

            # Save as jpeg
            mask.save(mask_path, "JPEG")
            mask.close()

    # Write the empty masks into the transforms.json
    for i, frame in enumerate(dataset['frames']):
        if 'quickmask_path' in frame and frame['quickmask_path'] is not None:
            transform['frames'][i]['mask_path'] = frame['quickmask_path']

    with open(os.path.join(path, 'transforms.json'), 'w') as f:
        json.dump(transform, f, indent=4)

    return dataset
api_app = FastAPI()
api_app.nerfstudio_dataset_path = None
api_app.loaded_dataset = None

@api_app.post("/current-dataset")
async def current_dataset():
    if api_app.loaded_dataset is None or api_app.nerfstudio_dataset_path is None:
        return {'error': 'No dataset loaded'}

    frames_have_masks = map(lambda f: 'mask_path' in f, api_app.loaded_dataset['frames'])
    return {
        'path': api_app.nerfstudio_dataset_path,
        'framecount': api_app.loaded_dataset['framecount'],
        'frames_have_masks': list(frames_have_masks)
    }

class SetDatasetPathRequest(BaseModel):
    path: str
    makeSafetyCopy: bool = True

@api_app.post("/set-dataset-path")
async def set_dataset_path(request: SetDatasetPathRequest):
    # Check the path is valid, an absolute path, and links to a transforms.json file
    if not os.path.isabs(request.path):
        return {'error': 'Path must be absolute'}

    if not os.path.exists(request.path):
        return {'error': 'Path does not exist'}

    if not os.path.isfile(os.path.join(request.path, 'transforms.json')):
        return {'error': 'Path does not contain a transforms.json file'}

    api_app.nerfstudio_dataset_path = request.path
    api_app.loaded_dataset = load_dataset(request.path, request.makeSafetyCopy)

    if api_app.loaded_dataset is None:
        api_app.nerfstudio_dataset_path = None
        return {'error': 'Failed to load dataset'}

    frames_have_masks = map(lambda f: 'mask_path' in f, api_app.loaded_dataset['frames'])
    return {
        'path': api_app.nerfstudio_dataset_path,
        'framecount': api_app.loaded_dataset['framecount'],
        'frames_have_masks': list(frames_have_masks)
    }


@api_app.get('/image/{index}')
async def get_image(index: int):
    if api_app.loaded_dataset is None:
        return {'error': 'No dataset loaded'}

    if index < 0 or index >= api_app.loaded_dataset['framecount']:
        return {'error': 'Index out of bounds'}

    return FileResponse(os.path.join(api_app.nerfstudio_dataset_path, api_app.loaded_dataset['frames'][index]['file_path']))

@api_app.get('/mask/{index}')
async def get_mask(index: int):
    if api_app.loaded_dataset is None:
        return {'error': 'No dataset loaded'}

    if index < 0 or index >= api_app.loaded_dataset['framecount']:
        return {'error': 'Index out of bounds'}

    if 'mask_path' not in api_app.loaded_dataset['frames'][index]:
        return {'error': 'No mask available for this frame'}

    image = Image.open(os.path.join(api_app.nerfstudio_dataset_path, api_app.loaded_dataset['frames'][index]['mask_path'])).convert('L')

    # Convert to numpy array
    mask = np.array(image)

    # Create an RGBA image (initialize with zeros)
    output = np.zeros((mask.shape[0], mask.shape[1], 4), dtype=np.uint8)

    # Define threshold
    threshold = 128

    # Set blue where the mask is black
    output[mask < threshold] = [0, 0, 255, 255]

    # Set alpha to 0 where the mask is white
    output[mask >= threshold] = [0, 0, 0, 0]

    # Convert back to an image
    result = Image.fromarray(output, "RGBA")
    # Save the image as a PNG
    imgio = io.BytesIO()
    result.save(imgio, "PNG")
    imgio.seek(0)
    image.close()
    result.close()
    return StreamingResponse(media_type="image/png", content=imgio)

class Rectangle(BaseModel):
    x: float
    y: float
    width: float
    height: float
    img_width: float
    img_height: float

class GenerateMaskRequest(BaseModel):
    rectangles: list[Rectangle]
    keep_mask: bool

@api_app.post('/generate-mask/{index}')
async def generate_mask(index: int, request: GenerateMaskRequest):
    # Check if the dataset is loaded
    if api_app.loaded_dataset is None:
        return {'error': 'No dataset loaded'}

    # Check if the index is valid
    if index < 0 or index >= api_app.loaded_dataset['framecount']:
        return {'error': 'Index out of bounds'}

    # Load the image
    image_path = os.path.join(api_app.nerfstudio_dataset_path, api_app.loaded_dataset['frames'][index]['image_path'])
    image = Image.open(image_path)
    width, height = image.size
    image.close()

    # Create a black mask
    mask = Image.new("L", (width, height), 255)

    # If an old mask exists add the black parts to the mask
    if 'mask_path' in api_app.loaded_dataset['frames'][index] and request.keep_mask:
        old_mask_path = os.path.join(api_app.nerfstudio_dataset_path, api_app.loaded_dataset['frames'][index]['mask_path'])
        old_mask = Image.open(old_mask_path).convert('L')
        mask.paste(old_mask, (0, 0))
        old_mask.close()

    # Draw the rectangles
    draw = ImageDraw.Draw(mask)
    for rect in request.rectangles:
        # Scale the rectangle from the canvas size to the image size
        scale_x = width / rect.img_width
        scale_y = height / rect.img_height

        x = math.floor(rect.x * scale_x)
        y = math.floor(rect.y * scale_y)
        w = math.floor(rect.width * scale_x)
        h = math.floor(rect.height * scale_y)
        draw.rectangle([x, y, x + w, y + h], fill=0)

    os.makedirs(os.path.join(api_app.nerfstudio_dataset_path, 'generated_masks'), exist_ok=True)

    # Save the mask
    mask_path = os.path.join(api_app.nerfstudio_dataset_path, 'generated_masks', f'generated_mask_{index}.jpeg')
    mask.save(mask_path, "JPEG")

    # Update the dataset and transforms.json
    frame = api_app.loaded_dataset['frames'][index]
    frame['quickmask_path'] = os.path.relpath(mask_path, api_app.nerfstudio_dataset_path)
    frame['reference']['mask_path'] = frame['quickmask_path']

    with open(os.path.join(api_app.nerfstudio_dataset_path, 'transforms.json'), 'r') as f:
        transform = json.load(f)

    transform['frames'][index]['mask_path'] = frame['quickmask_path']

    with open(os.path.join(api_app.nerfstudio_dataset_path, 'transforms.json'), 'w') as f:
        json.dump(transform, f, indent=4)

    return {'success': True}


app.mount("/api", api_app)

app.mount('/', StaticFiles(directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../frontend/dist'), html=True))

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)