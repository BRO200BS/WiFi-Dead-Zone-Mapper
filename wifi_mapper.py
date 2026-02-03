#!/usr/bin/env python3
"""
WiFi Dead Zone Mapper
Logs WiFi signal strength as you move around and creates a heat map visualization.
"""

import subprocess
import time
import json
import re
from datetime import datetime
from pathlib import Path

def get_wifi_signal_strength():
    """
    Get current WiFi signal strength for different operating systems.
    Returns signal strength in dBm (typically -30 to -90, where -30 is excellent, -90 is poor)
    """
    try:
        # For Linux
        result = subprocess.run(
            ['iwconfig'], 
            capture_output=True, 
            text=True,
            timeout=5
        )
        
        # Look for signal level in the output
        match = re.search(r'Signal level[=:](-?\d+)', result.stdout)
        if match:
            return int(match.group(1))
        
        # Alternative format
        match = re.search(r'Link Quality[=:](\d+)/(\d+)', result.stdout)
        if match:
            quality = int(match.group(1))
            max_quality = int(match.group(2))
            # Convert to approximate dBm (rough estimation)
            signal_dbm = -100 + (quality / max_quality) * 70
            return int(signal_dbm)
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # For macOS
        result = subprocess.run(
            ['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        match = re.search(r'agrCtlRSSI: (-?\d+)', result.stdout)
        if match:
            return int(match.group(1))
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    try:
        # For Windows (using netsh)
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'interfaces'],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        match = re.search(r'Signal\s*:\s*(\d+)%', result.stdout)
        if match:
            percentage = int(match.group(1))
            # Convert percentage to approximate dBm
            signal_dbm = -100 + (percentage / 100) * 70
            return int(signal_dbm)
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    return None

def get_manual_position():
    """
    Get manual position input from user (since GPS doesn't work well indoors).
    Returns (x, y) coordinates in meters or feet from a reference point.
    """
    print("\n--- Enter your current position ---")
    print("Use a reference point (e.g., front door = 0,0)")
    
    try:
        x = float(input("X coordinate (meters from reference): "))
        y = float(input("Y coordinate (meters from reference): "))
        return (x, y)
    except ValueError:
        print("Invalid input. Using (0, 0)")
        return (0, 0)

def collect_data(data_file='wifi_data.json', interval=2):
    """
    Continuously collect WiFi signal strength and position data.
    """
    print("=" * 60)
    print("WiFi Dead Zone Mapper - Data Collection Mode")
    print("=" * 60)
    print("\nInstructions:")
    print("1. Choose a reference point in your home (e.g., front door)")
    print("2. Walk to different locations")
    print("3. Press Enter at each location to log the signal")
    print("4. Enter your position relative to the reference point")
    print("5. Type 'done' when finished\n")
    
    data_points = []
    
    # Load existing data if available
    if Path(data_file).exists():
        with open(data_file, 'r') as f:
            data_points = json.load(f)
        print(f"Loaded {len(data_points)} existing data points.\n")
    
    point_num = len(data_points) + 1
    
    while True:
        user_input = input(f"\nPoint #{point_num} - Press Enter to log signal (or 'done' to finish): ").strip().lower()
        
        if user_input == 'done':
            break
        
        # Get WiFi signal
        signal = get_wifi_signal_strength()
        
        if signal is None:
            print("⚠️  Could not detect WiFi signal. Make sure you're connected to WiFi.")
            retry = input("Try again? (y/n): ").strip().lower()
            if retry != 'y':
                continue
            else:
                signal = get_wifi_signal_strength()
                if signal is None:
                    print("Still no signal detected. Skipping this point.")
                    continue
        
        # Get position
        x, y = get_manual_position()
        
        # Optional: add a room label
        room = input("Room/Area name (optional): ").strip()
        
        # Create data point
        data_point = {
            'timestamp': datetime.now().isoformat(),
            'signal_dbm': signal,
            'x': x,
            'y': y,
            'room': room if room else None
        }
        
        data_points.append(data_point)
        
        # Display signal quality
        if signal >= -50:
            quality = "Excellent"
        elif signal >= -60:
            quality = "Good"
        elif signal >= -70:
            quality = "Fair"
        else:
            quality = "Poor"
        
        print(f"✓ Logged: Signal = {signal} dBm ({quality}) at position ({x}, {y})")
        
        # Save after each point
        with open(data_file, 'w') as f:
            json.dump(data_points, f, indent=2)
        
        point_num += 1
    
    print(f"\n✓ Collected {len(data_points)} total data points")
    print(f"✓ Data saved to {data_file}")
    return data_points

def main():
    """Main entry point for data collection."""
    print("\nChecking WiFi connection...")
    signal = get_wifi_signal_strength()
    
    if signal is None:
        print("⚠️  Warning: Could not detect WiFi signal.")
        print("Make sure you are connected to a WiFi network.")
        print("\nSupported systems: Linux (iwconfig), macOS (airport), Windows (netsh)")
    else:
        print(f"✓ WiFi detected: {signal} dBm\n")
    
    collect_data()

if __name__ == '__main__':
    main()
