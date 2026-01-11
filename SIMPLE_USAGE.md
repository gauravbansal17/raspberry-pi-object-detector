# Simple Single-File Detectors

## Three Options - Pick What You Need

### 1. **basic_camera_test.py** - Just test if camera works
```bash
python basic_camera_test.py
```
- No AI, no complexity
- Just captures frames and prints status
- Use this first to verify camera works

### 2. **simple_detector.py** - Full detector in one file
```bash
python simple_detector.py
```
- OpenCV only
- Optional AI detection (YOLO)
- Audio announcements
- All in one file

### 3. **test_camera.py** - Diagnostic tool
```bash
python test_camera.py
```
- Tests multiple camera methods
- Shows detailed error messages

## Quick Start for Raspberry Pi 3

### Step 1: Enable Camera
```bash
bash enable_camera.sh
# OR manually edit config:
sudo nano /boot/config.txt
# Add: start_x=1 and gpu_mem=128
sudo reboot
```

### Step 2: Install OpenCV
```bash
sudo apt-get update
sudo apt-get install -y python3-opencv
```

### Step 3: Test Camera
```bash
python basic_camera_test.py
```
Should print: "Frame X captured" every second

### Step 4: Run Simple Detector
```bash
python simple_detector.py
```

## Optional: Add AI Detection

To enable AI object detection in `simple_detector.py`:

```bash
# Download tiny YOLO model (smaller, faster for Pi 3)
wget https://pjreddie.com/media/files/yolov3-tiny.weights
wget https://raw.githubusercontent.com/pjreddie/darknet/master/cfg/yolov3-tiny.cfg

# Now run detector
python simple_detector.py
```

## Optional: Enable Audio

```bash
# Install espeak for voice announcements
sudo apt-get install espeak

# Test it
espeak "Hello from Raspberry Pi"
```

## Troubleshooting

**Camera won't open?**
```bash
vcgencmd get_camera  # Should show: supported=1 detected=1
python test_camera.py  # Run diagnostics
```

**No module named 'cv2'?**
```bash
sudo apt-get install python3-opencv
```

**Permission denied?**
```bash
sudo usermod -aG video $USER
# Then logout/login or reboot
```

## File Comparison

| File | Lines | Dependencies | AI | Audio |
|------|-------|--------------|-----|-------|
| basic_camera_test.py | ~40 | cv2 only | ❌ | ❌ |
| simple_detector.py | ~200 | cv2 only | ✅ Optional | ✅ Optional |
| Full project | ~1000+ | Many | ✅ | ✅ |

**Recommendation for Pi 3:** Start with `basic_camera_test.py`, then use `simple_detector.py`.
