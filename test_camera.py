#!/usr/bin/env python3
"""
Camera diagnostic script for Raspberry Pi.
Run this to test if your camera is working properly.
"""

import sys
import time
import subprocess
import os

print("=" * 60)
print("Raspberry Pi Camera Diagnostic")
print("=" * 60)

# Test 0: Check Raspberry Pi version and camera stack
print("\n[0] Detecting Raspberry Pi model...")
try:
    with open('/proc/device-tree/model', 'r') as f:
        model = f.read().strip()
    print(f"Model: {model}")
    
    # Check if running on Pi 3 or older
    is_pi3_or_older = 'Pi 3' in model or 'Pi 2' in model or 'Pi 1' in model or 'Zero' in model
    
    if is_pi3_or_older:
        print("\n⚠️  Older Raspberry Pi detected (Pi 3 or earlier)")
        print("   Recommendation: Use legacy camera (raspistill) or OpenCV")
        print("\n   Testing legacy camera with raspistill...")
        try:
            result = subprocess.run(['raspistill', '-o', '/dev/null', '-t', '1000'], 
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print("   ✓ Legacy camera works! Use OpenCV method.")
            else:
                print(f"   ✗ raspistill failed: {result.stderr.decode()}")
        except FileNotFoundError:
            print("   ℹ️  raspistill not found. Will try OpenCV...")
        except Exception as e:
            print(f"   ℹ️  Cannot test raspistill: {e}")
    else:
        print("✓ Modern Raspberry Pi detected (Pi 4 or newer)")
        
except Exception as e:
    print(f"Could not detect Pi model: {e}")

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
print("\nTroubleshooting steps for Raspberry Pi 3:")
print("1. Enable camera: sudo raspi-config -> Interface Options -> Legacy Camera -> Enable")
print("2. Check camera connection and cable")
print("3. Test with legacy command: raspistill -o test.jpg")
print("4. Install OpenCV: pip install opencv-python")
print("5. Add user to video group: sudo usermod -aG video $USER")
print("6. Reboot: sudo reboot")
print("7. Check camera is not in use: lsof | grep video")
print("\nFor Raspberry Pi 3, OpenCV method is recommended.")
print("libcamera is not available on Pi 3 - use legacy camera stack.")
print("\nNote: If using Raspberry Pi camera module v1 or v2,")
print("      ensure you've enabled 'Legacy Camera' in raspi-config")
