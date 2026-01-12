#!/usr/bin/env python3
"""
Ultrasonic Sensor Hardware Diagnostic
Tests GPIO pins and checks for common wiring issues
"""
import RPi.GPIO as GPIO
import time

TRIG_PIN = 23
ECHO_PIN = 24

print("=" * 60)
print("HC-SR04 Hardware Diagnostic Tool")
print("=" * 60)

# Test 1: Check GPIO access
print("\n[Test 1] Checking GPIO access...")
try:
    GPIO.setmode(GPIO.BCM)
    print("✓ GPIO access OK")
except Exception as e:
    print(f"✗ GPIO access failed: {e}")
    exit(1)

# Test 2: Setup pins
print("\n[Test 2] Setting up GPIO pins...")
try:
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.5)
    print(f"✓ TRIG pin (GPIO{TRIG_PIN}) configured as OUTPUT")
    print(f"✓ ECHO pin (GPIO{ECHO_PIN}) configured as INPUT")
except Exception as e:
    print(f"✗ Pin setup failed: {e}")
    GPIO.cleanup()
    exit(1)

# Test 3: Check initial ECHO state
print("\n[Test 3] Checking ECHO pin initial state...")
echo_state = GPIO.input(ECHO_PIN)
if echo_state == 0:
    print("✓ ECHO pin is LOW (correct idle state)")
else:
    print("✗ ECHO pin is HIGH (PROBLEM!)")
    print("\n  Possible causes:")
    print("  1. No voltage divider or wrong values")
    print("  2. Sensor not powered correctly")
    print("  3. Wiring issue or loose connection")
    print("  4. Damaged sensor")
    print("\n  Expected wiring:")
    print("  HC-SR04 ECHO → 1kΩ → GPIO24 → 2kΩ → GND")

# Test 4: Toggle trigger pin
print("\n[Test 4] Testing TRIG pin control...")
for i in range(3):
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.1)
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.1)
print("✓ TRIG pin toggling works")

# Test 5: Try a measurement
print("\n[Test 5] Attempting distance measurement...")
measurement_ok = False

for attempt in range(3):
    print(f"  Attempt {attempt + 1}/3...")
    
    # Send trigger pulse
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.01)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    
    # Wait for echo with short timeout
    start_time = time.time()
    timeout = start_time + 0.05
    
    # Wait for HIGH
    while GPIO.input(ECHO_PIN) == 0 and time.time() < timeout:
        pass
    
    if time.time() >= timeout:
        print("    ✗ ECHO never went HIGH (sensor not responding)")
        continue
    
    pulse_start = time.time()
    
    # Wait for LOW
    timeout = time.time() + 0.05
    while GPIO.input(ECHO_PIN) == 1 and time.time() < timeout:
        pass
    
    if time.time() >= timeout:
        print("    ✗ ECHO stuck HIGH (voltage divider issue?)")
        # Try to reset
        GPIO.setup(ECHO_PIN, GPIO.OUT)
        GPIO.output(ECHO_PIN, False)
        time.sleep(0.01)
        GPIO.setup(ECHO_PIN, GPIO.IN)
        continue
    
    pulse_end = time.time()
    duration = pulse_end - pulse_start
    distance = (duration * 34300) / 2
    
    if 2 < distance < 400:
        print(f"    ✓ Distance: {distance:.1f} cm")
        measurement_ok = True
        break
    else:
        print(f"    ⚠️  Invalid reading: {distance:.1f} cm")

print("\n" + "=" * 60)
print("DIAGNOSTIC SUMMARY")
print("=" * 60)

if measurement_ok:
    print("✅ Sensor working correctly!")
else:
    print("❌ Sensor has issues. Check:")
    print("\n1. VOLTAGE DIVIDER (most common issue):")
    print("   ECHO → 1kΩ resistor → GPIO24")
    print("              └→ 2kΩ resistor → GND")
    print("\n2. POWER:")
    print("   VCC → 5V (NOT 3.3V)")
    print("   GND → GND")
    print("\n3. WIRING:")
    print("   TRIG → GPIO23 directly")
    print("   ECHO → GPIO24 through divider")
    print("\n4. Try different sensor if available")

GPIO.cleanup()
print("\n✓ GPIO cleaned up")
