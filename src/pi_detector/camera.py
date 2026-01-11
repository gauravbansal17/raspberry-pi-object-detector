"""
Camera handling module for Raspberry Pi camera.
"""

import logging
from typing import Optional, Tuple
import numpy as np

try:
    from picamera2 import Picamera2
    PICAMERA_AVAILABLE = True
except ImportError:
    PICAMERA_AVAILABLE = False
    logging.warning("picamera2 not available. Using fallback OpenCV camera.")

import cv2

logger = logging.getLogger(__name__)


class CameraHandler:
    """Handles camera operations for the Raspberry Pi."""
    
    def __init__(self, resolution: Tuple[int, int] = (640, 480), framerate: int = 30):
        """
        Initialize camera handler.
        
        Args:
            resolution: Camera resolution as (width, height)
            framerate: Camera framerate
        """
        self.resolution = resolution
        self.framerate = framerate
        self.camera = None
        self.use_picamera = PICAMERA_AVAILABLE
        
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize the camera based on available libraries."""
        try:
            if self.use_picamera:
                logger.info("Initializing Picamera2...")
                try:
                    self.camera = Picamera2()
                    
                    # Configure camera
                    config = self.camera.create_preview_configuration(
                        main={"size": self.resolution, "format": "RGB888"}
                    )
                    self.camera.configure(config)
                    self.camera.start()
                    
                    logger.info("Picamera2 initialized successfully")
                    return
                except Exception as pic_error:
                    logger.warning(f"Picamera2 failed: {pic_error}. Trying OpenCV fallback...")
                    self.use_picamera = False
            
            # Try OpenCV (either as primary or fallback)
            logger.info("Initializing OpenCV camera...")
            
            # Try different camera indices
            for camera_idx in [0, 1, -1]:
                logger.info(f"Trying camera index {camera_idx}...")
                self.camera = cv2.VideoCapture(camera_idx)
                
                if self.camera.isOpened():
                    # Set camera properties
                    self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
                    self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
                    self.camera.set(cv2.CAP_PROP_FPS, self.framerate)
                    
                    # Test if we can actually read a frame
                    ret, test_frame = self.camera.read()
                    if ret:
                        logger.info(f"OpenCV camera initialized successfully on index {camera_idx}")
                        return
                    else:
                        self.camera.release()
                        logger.warning(f"Camera {camera_idx} opened but cannot read frames")
                else:
                    logger.warning(f"Camera {camera_idx} could not be opened")
            
            raise RuntimeError(
                "Failed to open camera. Please check:\n"
                "1. Camera is connected properly\n"
                "2. Camera is enabled in raspi-config:\n"
                "   - Pi 4/5: Interface Options -> Camera\n"
                "   - Pi 3/older: Interface Options -> Legacy Camera\n"
                "3. Required packages installed:\n"
                "   - Pi 4/5: sudo apt-get install python3-picamera2\n"
                "   - Pi 3/older: sudo apt-get install python3-opencv\n"
                "4. User has video group access: sudo usermod -aG video $USER\n"
                "5. Test camera:\n"
                "   - Pi 4/5: libcamera-hello --list-cameras\n"
                "   - Pi 3/older: raspistill -o test.jpg\n"
                "6. Reboot after making changes: sudo reboot"
            )
                
        except Exception as e:
            logger.error(f"Failed to initialize camera: {e}")
            raise
    
    def capture_frame(self) -> Optional[np.ndarray]:
        """
        Capture a single frame from the camera.
        
        Returns:
            Frame as numpy array (RGB format) or None if capture fails
        """
        try:
            if self.use_picamera and self.camera:
                # Capture from Picamera2
                frame = self.camera.capture_array()
                return frame
            elif self.camera:
                # Capture from OpenCV
                ret, frame = self.camera.read()
                if ret:
                    # Convert BGR to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    return frame
                else:
                    logger.warning("Failed to read frame from camera")
                    return None
            else:
                logger.error("Camera not initialized")
                return None
                
        except Exception as e:
            logger.error(f"Error capturing frame: {e}")
            return None
    
    def close(self):
        """Release camera resources."""
        try:
            if self.camera:
                if self.use_picamera:
                    self.camera.stop()
                else:
                    self.camera.release()
                logger.info("Camera closed successfully")
        except Exception as e:
            logger.error(f"Error closing camera: {e}")
    
    def is_available(self) -> bool:
        """
        Check if camera is available and working.
        
        Returns:
            True if camera is available, False otherwise
        """
        return self.camera is not None
