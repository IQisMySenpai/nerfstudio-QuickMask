# Nerfstudio QuickMask

![Nerfstudio QuickMask Logo](frontend/public/logo.png)

**Nerfstudio QuickMask** is an tool designed to quickly generate masks for your Nerfstudio dataset using rectangles. It simplifies the masking process compared to other methods, making it ideal for testing new datasets.

## Features
- **Fast Masking**: Quickly create masks using simple rectangular selections.
- **Automatic Mask Generation**: Automatically generates mask files for your dataset.
- **Optimized Workflow**: Streamlines the process of preparing data for Nerfstudio.

## Installation
Ensure you have Python 3 and Node.js installed.

```sh
pip3 install -r requirements.txt
```

### Building the Frontend
```sh
cd frontend
npm install
npm run build
```

## Usage
Run the `backend/api.py` to host the webinterface on your local machine
```sh
python3 backend/api.py
```
1. Load your Nerfstudio dataset with the webinterface
2. Use the rectangle tool to select areas to mask.
3. The masks are then automatically added to your nerfstudio dataset

## Contributing
Contributions are welcome! Feel free to submit issues and pull requests.

