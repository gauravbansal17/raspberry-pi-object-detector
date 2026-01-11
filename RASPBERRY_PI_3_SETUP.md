# Raspberry Pi 3 Camera Setup Guide

## Important: Pi 3 uses Legacy Camera Stack

Raspberry Pi 3 does **not** support libcamera. You need to use the legacy camera interface with OpenCV.

## Setup Steps for Raspberry Pi 3

### 1. Enable Camera

#### Method A: Using raspi-config
```bash
sudo raspi-config
```
Look for one of these options (varies by OS version):
- **Interface Options** → **Camera** → Enable
- **Interface Options** → **Legacy Camera** → Enable  
- **Interfacing Options** → **Camera** → Enable

Then reboot: `sudo reboot`

#### Method B: Edit config.txt directly (if no camera option in raspi-config)
```bash
# Edit the boot config
sudo nano /boot/config.txt

# Add this line (or make sure it's not commented out):
start_x=1
gpu_mem=128

# If the line exists with a # in front, remove the #
# Save with Ctrl+X, then Y, then Enter

# Reboot
sudo reboot
```

#### Method C: Edit firmware config (newer OS)
```bash
# For newer Raspberry Pi OS
sudo nano /boot/firmware/config.txt

# Add these lines:
start_x=1
gpu_mem=128
camera_auto_detect=1

# Save and reboot
sudo reboot
```

### 2. Install Required Packages
```bash
sudo apt-get update
sudo apt-get install -y python3-opencv python3-pip
```

### 3. Install Python Dependencies
```bash
cd ~/venv_project  # or wherever you cloned the project
pip install -r requirements.txt
```

### 4. Add User to Video Group
```bash
sudo usermod -aG video $USER
```
Then logout and login again (or reboot)

### 5. Test Camera with Legacy Tools
```bash
# Test with raspistill (should capture an image)
raspistill -o test.jpg

# If that works, test the diagnostic script
python test_camera.py
```

### 6. Run the Detection Application

If the diagnostic passes, you can run the detector:

```bash
# Install the package
pip install -e .

# Run the detector
pi-detector
```

Or use the run script:
```bash
python run.py
```

## Troubleshooting

### Camera Not Found
- Ensure camera cable is properly connected
- Camera ribbon cable should be connected to CSI port (not display port)
- Check with: `vcgencmd get_camera` (should show `detected=1`)

### Permission Denied
```bash
# Add user to video group
sudo usermod -aG video $USER
# Logout and login, or reboot
sudo reboot
```

### Still Not Working?
```bash
# Check if anything is using the camera
lsof | grep video

# Check camera status
vcgencmd get_camera

# Should show: supported=1 detected=1
```

## Notes for Pi 3 Users

- **picamera2 is NOT available** on Raspberry Pi 3 - this is normal
- The application will automatically use **OpenCV** as fallback
- **libcamera-hello** command does not exist on Pi 3 - use **raspistill** instead
- Legacy camera must be enabled in raspi-config
- Pi 3 works great with OpenCV method - no need for picamera2!

## Camera Module Compatibility

| Camera Module | Raspberry Pi 3 |
|---------------|---------------|
| Camera Module v1 (OV5647) | ✅ Works (Legacy) |
| Camera Module v2 (IMX219) | ✅ Works (Legacy) |
| Camera Module v3 (IMX708) | ⚠️ Limited support |
| HQ Camera (IMX477) | ✅ Works (Legacy) |

For best results on Pi 3, use Camera Module v1 or v2.
