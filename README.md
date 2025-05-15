# Vector Data Collection Walk-Through

This repository contains the scripts used to generate a custom dataset for training a computer vision model to recognize an Anki Vector robot. If you're looking to create your own dataset using multiple Vectors, this walkthrough will guide you through the setup and usage.

## Overview
This project uses **two Anki Vector robots** connected to the **same laptop** to collect training data for a computer vision model.

### 🤖 Roles

- **Vector #1 (Camera Bot)**  
  Acts as the **photographer**. It captures images when signaled by the second Vector.

- **Vector #2 (Target Bot)**  
  Navigates to **random positions** within a defined **equilateral triangle**, performs a **random rotation**, then signals when ready to be photographed.

---

### 🔄 Workflow

1. **Vector #2** moves to a **random point** within a defined **equilateral triangle** and performs a **random rotation**.
2. It sends a signal to **Vector #1** using **socket communication**, indicating it is ready for a photo.
3. **Vector #1**, which is listening for the signal, captures an image.
4. **Vector #2** returns to its **starting position**.
5. The process **repeats**, generating images with varying positions and orientations.

## Dataset Recommendations

- **Transfer Learning with YOLOv8**: YOLOv8 is a model pre-trained on thousands of images and classes with conditioned weights. By leveraging transfer learning, we can train a model with a relatively smaller dataset. I successfully trained my model with around **300 images**, but more data is always better for improving model performance.
  
- **Triangle Setup for Better Data Capture**: In `moving.py`, I recommend using an **11-inch equilateral triangle**. This smaller distance helps the camera and model better recognize and classify the Vector. Since the Vector is primarily black, it can be hard to distinguish from the background at larger distances, which can make it challenging for the model to recognize and draw a bounding box.
  
- **Include True Negatives**: Adding **True Negatives** to your dataset makes it more robust. Instead of only including images with the Vector in different positions and rotations, include images where no Vector is present. I suggest collecting at least **75 True Negative images**, but more would be better.

- **Use CVAT for Annotation**: I used [CVAT](https://www.cvat.ai/) to annotate my images. It’s a great tool for labeling bounding boxes and annotating your dataset effectively.
  
- **Add Noise to the Dataset**: Adding noise (such as other black objects or random objects in the background) helps the model generalize better. I recommend taking pictures with objects visible in the environment, not just the Vector.


## Get Started

1. Install Python
Make sure you have **Python 3.11.x or higher** installed.

2. Set Up a Virtual Environment

Open a terminal and run:
```
python -m venv .venv
.\.venv\Scripts\activate
```
3. Install Dependencies
Once the environment is activated, install the required packages:
```
pip install -r requirements.txt
```

5. 🤖 Vector SDK Setup

You’ll need **two Anki Vector robots** configured with the SDK in order to run the data collection scripts.

Follow these setup guides:

- 📦 [Vector Setup by mparekh99](https://github.com/mparekh99/Vector-Setup)
- 🔌 [WIREPOD Installation Guide](https://github.com/kercre123/wire-pod/wiki/Installation)
- 🧠 [Wirepod Python SDK for Vector](https://github.com/kercre123/wirepod-vector-python-sdk)

> ⚠️ Make sure both Vectors are paired and configured via the WIREPOD and SDK before running any scripts.


# Usage
On Vector #1, run the data collection script:
```
python datacollect.py
```

Before starting, position **Vector #2** exactly **11 inches in front of Vector #1**, facing it. This spot will serve as Vector #2’s starting position and is considered the origin `(0, 0)`.

Make sure Vector #2 has at least **11 inches of free space to both its left and right**. It will use this space to navigate randomly within a triangular area measuring approximately 11 inches by 11 inches by 11 inches. This triangle extends forward and side-to-side from Vector #2’s starting point to ensure varied movement and data capture.

In a **separate terminal**, activate the virtual environment again and run the following command on **Vector #2** to begin its movement:
```
python moving.py
``` 

This setup lets one Vector capture images while the other one moves, enabling dynamic data collection.

### 📷 Optional: Manual Photography Mode

If you prefer more control over the image capture process, you can use `photographer.py`.

This script allows you to manually control a Vector robot using your keyboard:

- Use the **arrow keys** to move the robot.
- Press **Spacebar** to take a photo using the front-facing camera.

To run the manual capture mode:
```
python photographer.py
```
