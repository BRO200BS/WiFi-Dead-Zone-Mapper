# WiFi Dead Zone Mapper

Map WiFi signal strength throughout your home and visualize dead zones with heat maps.
https://github.com/BRO200BS/WiFi-Dead-Zone-Mapper/blob/main/example_heatmap.png

## Features

- 📊 Collect WiFi signal strength data as you move around
- 🗺️ Generate beautiful heat map visualizations
- 📍 Manual position tracking (works better than GPS indoors)
- 🔍 Identify dead zones and areas with weak coverage
- 📈 3D surface visualization option
- 💾 Save and resume data collection sessions

## Requirements

Install the required Python packages:

```bash
pip install numpy matplotlib scipy --break-system-packages
```

### System Requirements

The tool automatically detects your operating system and uses the appropriate WiFi command:

- **Linux**: Uses `iwconfig` (usually pre-installed)
- **macOS**: Uses `airport` utility (built-in)
- **Windows**: Uses `netsh wlan` (built-in)

## Usage

### Step 1: Collect Data

Run the data collection script and walk around your home:

```bash
python3 wifi_mapper.py
```

**Instructions:**
1. Choose a reference point (e.g., your front door = 0,0)
2. Walk to different locations in your home
3. At each location, press Enter to log the signal
4. Enter your position relative to the reference point in meters
5. Optionally label the room/area
6. Type 'done' when finished

**Tips:**
- Collect at least 10-15 points for a good heat map
- Sample from different rooms and areas
- Include spots where you know WiFi is weak
- You can run the script multiple times - data accumulates

**Example session:**
```
Point #1 - Press Enter to log signal: [Enter]
X coordinate (meters from reference): 0
Y coordinate (meters from reference): 0
Room/Area name (optional): Living Room
✓ Logged: Signal = -45 dBm (Excellent) at position (0, 0)

Point #2 - Press Enter to log signal: [Enter]
X coordinate (meters from reference): 5
Y coordinate (meters from reference): 3
Room/Area name (optional): Kitchen
✓ Logged: Signal = -67 dBm (Fair) at position (5, 3)
```

### Step 2: Generate Heat Map

Create visualizations from your collected data:

```bash
python3 wifi_visualizer.py
```

This will:
- Analyze your data for dead zones
- Generate a heat map (`wifi_heatmap.png`)
- Show signal quality statistics

**Advanced options:**

```bash
# Use custom data file
python3 wifi_visualizer.py --data my_wifi_data.json

# Save heat map to specific file
python3 wifi_visualizer.py --output my_heatmap.png

# Also create 3D visualization
python3 wifi_visualizer.py --3d

# Change dead zone threshold (default: -75 dBm)
python3 wifi_visualizer.py --threshold -70
```

## Understanding Signal Strength

WiFi signal strength is measured in dBm (decibel-milliwatts):

| Signal (dBm) | Quality | Description |
|--------------|---------|-------------|
| -30 to -50   | Excellent | Maximum speed and reliability |
| -50 to -60   | Good | Very reliable, good speeds |
| -60 to -70   | Fair | Reliable, may see slower speeds |
| -70 to -80   | Poor | Unreliable, slow speeds |
| -80 to -90   | Very Poor | Minimal connectivity, frequent drops |

## Output Files

- `wifi_data.json` - Your collected data points (can be backed up/shared)
- `wifi_heatmap.png` - 2D heat map visualization
- `wifi_3d.png` - 3D surface plot (if using `--3d` flag)

## Tips for Best Results

1. **Collect more data**: 20-30 points give better interpolation
2. **Cover the space evenly**: Don't cluster all points in one area
3. **Multiple floors**: Run separately for each floor
4. **Time of day**: WiFi can vary with interference - test at different times
5. **Router placement**: Use the heat map to optimize router location

## Improving WiFi Coverage

Based on your heat map, you can:

1. **Reposition your router**: Move it closer to dead zones
2. **Elevate the router**: Higher placement often improves coverage
3. **Reduce obstacles**: Remove metal objects, mirrors, or dense furniture between router and dead zones
4. **Add a WiFi extender**: Place it in areas with fair coverage to boost dead zones
5. **Upgrade to mesh WiFi**: For large homes with multiple dead zones

## Troubleshooting

**"Could not detect WiFi signal"**
- Make sure you're connected to WiFi
- On Linux, install `wireless-tools`: `sudo apt-get install wireless-tools`
- On macOS, airport utility should be built-in
- Try running with sudo: `sudo python3 wifi_mapper.py`

**"No data points found"**
- Make sure you've run `wifi_mapper.py` first
- Check that `wifi_data.json` exists in the current directory

**Heat map looks strange**
- Collect more data points (aim for 15+)
- Make sure points are spread across your space
- Check for any outlier measurements

## Example Workflow

```bash
# 1. Install dependencies
pip install numpy matplotlib scipy --break-system-packages

# 2. Collect data (walk around and log 15-20 points)
python3 wifi_mapper.py

# 3. Generate heat map
python3 wifi_visualizer.py --3d

# 4. View your heat maps
# Open wifi_heatmap.png and wifi_3d.png
```

## Data Format

The `wifi_data.json` file stores data in this format:

```json
[
  {
    "timestamp": "2024-02-04T10:30:00",
    "signal_dbm": -55,
    "x": 0,
    "y": 0,
    "room": "Living Room"
  },
  {
    "timestamp": "2024-02-04T10:32:00",
    "signal_dbm": -72,
    "x": 5,
    "y": 3,
    "room": "Kitchen"
  }
]
```

You can manually edit this file or import data from other sources.

## License

Free to use and modify. No warranty provided.
