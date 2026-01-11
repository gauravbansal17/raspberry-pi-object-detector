#!/usr/bin/env python3
"""
Simple Raspberry Pi Object Detector
Single file, OpenCV only, easy to use
"""

import cv2
import numpy as np
import time
import os

# Configuration - Edit these values as needed
CONFIDENCE_THRESHOLD = 0.5
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
DISPLAY_WINDOW = False  # Set to True if you have a display connected

# COCO class names (objects the model can detect)
CLASSES = [
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
    'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat',
    'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack',
    'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair',
    'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
]

# Interesting animals and humans to announce
ANNOUNCE_CLASSES = ['person', 'dog', 'cat', 'bird', 'horse', 'cow', 'sheep', 'bear', 'elephant']


def speak(text):
    """Announce text through speaker (optional)"""
    try:
        # Try espeak (common on Raspberry Pi)
        os.system(f'espeak "{text}" 2>/dev/null')
    except:
        print(f"🔊 {text}")


def detect_objects(frame, net, output_layers):
    """Detect objects in frame using YOLO"""
    height, width = frame.shape[:2]
    
    # Prepare image for YOLO
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)
    
    # Process detections
    boxes = []
    confidences = []
    class_ids = []
    
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > CONFIDENCE_THRESHOLD:
                # Get box coordinates
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w/2)
                y = int(center_y - h/2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Apply non-max suppression to remove overlapping boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD, 0.4)
    
    detected_objects = []
    if len(indices) > 0:
        for i in indices.flatten():
            detected_objects.append({
                'class': CLASSES[class_ids[i]],
                'confidence': confidences[i],
                'box': boxes[i]
            })
    
    return detected_objects


def draw_detections(frame, detections):
    """Draw boxes and labels on frame"""
    for det in detections:
        x, y, w, h = det['box']
        label = f"{det['class']}: {det['confidence']:.2f}"
        
        # Draw box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Draw label background
        cv2.rectangle(frame, (x, y-20), (x+w, y), (0, 255, 0), -1)
        
        # Draw label text
        cv2.putText(frame, label, (x+5, y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    
    return frame


def main():
    print("=" * 50)
    print("Simple Raspberry Pi Object Detector")
    print("=" * 50)
    
    # Initialize camera
    print("Initializing camera...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Cannot open camera!")
        print("Try: sudo apt-get install python3-opencv")
        print("Or run: python test_camera.py for diagnostics")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
    print("✓ Camera initialized")
    
    # Load YOLO model (optional - requires model files)
    try:
        print("Loading AI model...")
        # Download these files from: https://pjreddie.com/darknet/yolo/
        # yolov3-tiny.weights, yolov3-tiny.cfg
        net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
        use_ai = True
        print("✓ AI model loaded (YOLOv3-tiny)")
    except:
        print("⚠️  AI model not found - using motion detection only")
        print("To use AI detection, download:")
        print("  wget https://pjreddie.com/media/files/yolov3-tiny.weights")
        print("  wget https://github.com/pjreddie/darknet/raw/master/cfg/yolov3-tiny.cfg")
        use_ai = False
    
    print("\n✓ Starting detection...")
    print("Press Ctrl+C to stop\n")
    
    last_announcement = {}
    frame_count = 0
    
    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("⚠️  Failed to read frame")
                time.sleep(0.1)
                continue
            
            frame_count += 1
            
            # Run detection every 30 frames (about 1 second)
            if use_ai and frame_count % 30 == 0:
                detections = detect_objects(frame, net, output_layers)
                
                # Announce interesting detections
                for det in detections:
                    obj_class = det['class']
                    if obj_class in ANNOUNCE_CLASSES:
                        # Only announce if not announced in last 5 seconds
                        current_time = time.time()
                        if obj_class not in last_announcement or \
                           current_time - last_announcement[obj_class] > 5:
                            
                            print(f"✓ Detected: {obj_class} ({det['confidence']:.2%})")
                            speak(f"Detected {obj_class}")
                            last_announcement[obj_class] = current_time
                
                # Draw detections if display enabled
                if DISPLAY_WINDOW and detections:
                    frame = draw_detections(frame, detections)
            
            # Show frame if display connected
            if DISPLAY_WINDOW:
                cv2.imshow('Object Detection', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
    except KeyboardInterrupt:
        print("\n\nStopping detection...")
    
    finally:
        cap.release()
        if DISPLAY_WINDOW:
            cv2.destroyAllWindows()
        print("✓ Done!")


if __name__ == "__main__":
    main()
