from gpiozero import DistanceSensor
from time import sleep

# Initialize sensor with echo on GPIO 18 and trigger on GPIO 17
sensor = DistanceSensor(echo=18, trigger=17)

print("Starting distance measurement...")
while True:
    # .distance gives distance in meters
    # Multiply by 100 for centimeters
    distance_cm = sensor.distance * 100
    print(f"Distance: {distance_cm:.2f} cm")
    sleep(1) # Wait for a second before next reading