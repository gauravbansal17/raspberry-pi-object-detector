#!/usr/bin/env python3
"""
Ultra Simple Camera Test
Just captures and shows frames - no AI needed
"""

import cv2
import time

print("Starting camera test...")
print("Press Ctrl+C to stop")

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot open camera!")
    exit(1)

print("Camera opened successfully!")
print("Capturing frames...")

frame_count = 0

try:
    while True:
        ret, frame = cap.read()
        
        if ret:
            frame_count += 1
            if frame_count % 30 == 0:  # Print every 30 frames (~1 second)
                print(f"✓ Frame {frame_count} captured - Size: {frame.shape}")
        else:
            print("Failed to read frame")
        
        time.sleep(0.033)  # ~30 FPS
        
except KeyboardInterrupt:
    print(f"\nStopped. Captured {frame_count} frames total.")

finally:
    cap.release()
    print("Camera released.")
