#!/bin/bash
# Camera Enable Script for Raspberry Pi 3
# Run with: bash enable_camera.sh

echo "========================================"
echo "Raspberry Pi 3 Camera Enable Script"
echo "========================================"

# Check which config file exists
if [ -f /boot/firmware/config.txt ]; then
    CONFIG_FILE="/boot/firmware/config.txt"
    echo "Found config at: $CONFIG_FILE (newer OS)"
elif [ -f /boot/config.txt ]; then
    CONFIG_FILE="/boot/config.txt"
    echo "Found config at: $CONFIG_FILE"
else
    echo "ERROR: Cannot find config.txt"
    exit 1
fi

echo ""
echo "Backing up config file..."
sudo cp "$CONFIG_FILE" "${CONFIG_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

echo "Enabling camera in $CONFIG_FILE..."

# Check if start_x exists
if grep -q "^start_x=1" "$CONFIG_FILE"; then
    echo "✓ start_x=1 already set"
elif grep -q "^#start_x=1" "$CONFIG_FILE"; then
    echo "Uncommenting start_x=1..."
    sudo sed -i 's/^#start_x=1/start_x=1/' "$CONFIG_FILE"
elif grep -q "^start_x=0" "$CONFIG_FILE"; then
    echo "Changing start_x=0 to start_x=1..."
    sudo sed -i 's/^start_x=0/start_x=1/' "$CONFIG_FILE"
else
    echo "Adding start_x=1..."
    echo "start_x=1" | sudo tee -a "$CONFIG_FILE"
fi

# Check if gpu_mem exists
if grep -q "^gpu_mem=128" "$CONFIG_FILE"; then
    echo "✓ gpu_mem=128 already set"
elif grep -q "^gpu_mem=" "$CONFIG_FILE"; then
    echo "Updating gpu_mem to 128..."
    sudo sed -i 's/^gpu_mem=.*/gpu_mem=128/' "$CONFIG_FILE"
else
    echo "Adding gpu_mem=128..."
    echo "gpu_mem=128" | sudo tee -a "$CONFIG_FILE"
fi

# Add camera_auto_detect for newer systems
if ! grep -q "camera_auto_detect" "$CONFIG_FILE"; then
    echo "Adding camera_auto_detect=1..."
    echo "camera_auto_detect=1" | sudo tee -a "$CONFIG_FILE"
fi

echo ""
echo "========================================"
echo "✓ Camera configuration updated!"
echo "========================================"
echo ""
echo "Current camera settings in $CONFIG_FILE:"
grep -E "start_x|gpu_mem|camera_auto_detect" "$CONFIG_FILE"
echo ""
echo "⚠️  IMPORTANT: You must reboot for changes to take effect!"
echo ""
read -p "Do you want to reboot now? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Rebooting in 3 seconds..."
    sleep 3
    sudo reboot
else
    echo "Please reboot manually with: sudo reboot"
fi
