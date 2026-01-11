#!/usr/bin/env python3
"""
Camera diagnostic script for Raspberry Pi.
Run this to test if your camera is working properly.
"""

import sys
import time

print("=" * 60)
print("Raspberry Pi Camera Diagnostic")
print("=" * 60)

# Test 1: Check picamera2
print("\n[1] Testing picamera2...")
try:
    from picamera2 import Picamera2
    print("✓ picamera2 is installed")
    
    try:
        camera = Picamera2()
        print("✓ Picamera2 object created")
        
        config = camera.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
        camera.configure(config)
        print("✓ Camera configured")
        
        camera.start()
        print("✓ Camera started")
        
        # Capture a test frame
        frame = camera.capture_array()
        print(f"✓ Frame captured: shape={frame.shape}, dtype={frame.dtype}")
        
        camera.stop()
        print("✓ Picamera2 working correctly!")
        
        print("\n✅ SUCCESS: Your camera is working with picamera2")
        sys.exit(0)
        
    except Exception as e:
        print(f"✗ Picamera2 error: {e}")
        
except ImportError:
    print("✗ picamera2 not installed")
    print("  Install with: sudo apt-get install python3-picamera2")

# Test 2: Check OpenCV
print("\n[2] Testing OpenCV...")
try:
    import cv2
    print(f"✓ OpenCV is installed (version {cv2.__version__})")
    
    for idx in [0, 1, -1]:
        print(f"\n  Trying camera index {idx}...")
        cap = cv2.VideoCapture(idx)
        
        if cap.isOpened():
            print(f"  ✓ Camera {idx} opened")
            
            ret, frame = cap.read()
            if ret:
                print(f"  ✓ Frame captured: shape={frame.shape}, dtype={frame.dtype}")
                cap.release()
                print(f"\n✅ SUCCESS: Your camera is working with OpenCV on index {idx}")
                sys.exit(0)
            else:
                print(f"  ✗ Could not read frame from camera {idx}")
                cap.release()
        else:
            print(f"  ✗ Camera {idx} could not be opened")
            
except ImportError:
    print("✗ OpenCV not installed")
    print("  Install with: pip install opencv-python")
except Exception as e:
    print(f"✗ OpenCV error: {e}")

# If we get here, nothing worked
print("\n" + "=" * 60)
print("❌ FAILED: Camera not working with any method")
print("=" * 60)
print("\nTroubleshooting steps:")
print("1. Enable camera: sudo raspi-config -> Interface Options -> Camera")
print("2. Check camera connection and cable")
print("3. Test with system command: libcamera-hello --list-cameras")
print("4. Add user to video group: sudo usermod -aG video $USER")
print("5. Install dependencies:")
print("   sudo apt-get install python3-picamera2 python3-opencv")
print("6. Reboot: sudo reboot")
print("7. Check camera is not in use: lsof | grep video")
print("\nFor more help, run: libcamera-hello -t 5000")
