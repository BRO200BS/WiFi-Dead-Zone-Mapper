#!/usr/bin/env python3
"""
WiFi Heat Map Visualizer
Creates heat map visualizations from collected WiFi signal strength data.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.interpolate import griddata
from pathlib import Path

def load_data(data_file='wifi_data.json'):
    """Load WiFi data from JSON file."""
    if not Path(data_file).exists():
        print(f"Error: {data_file} not found.")
        print("Run wifi_mapper.py first to collect data.")
        return None
    
    with open(data_file, 'r') as f:
        data = json.load(f)
    
    if len(data) == 0:
        print("No data points found in file.")
        return None
    
    return data

def create_heatmap(data, output_file='wifi_heatmap.png', resolution=100):
    """
    Create a heat map visualization from WiFi data.
    
    Args:
        data: List of data points with x, y, and signal_dbm
        output_file: Output filename for the heat map image
        resolution: Grid resolution for interpolation
    """
    # Extract coordinates and signal strengths
    x_coords = [point['x'] for point in data]
    y_coords = [point['y'] for point in data]
    signals = [point['signal_dbm'] for point in data]
    
    print(f"Creating heat map from {len(data)} data points...")
    print(f"Signal range: {min(signals)} to {max(signals)} dBm")
    
    # Create grid for interpolation
    x_min, x_max = min(x_coords) - 1, max(x_coords) + 1
    y_min, y_max = min(y_coords) - 1, max(y_coords) + 1
    
    grid_x, grid_y = np.meshgrid(
        np.linspace(x_min, x_max, resolution),
        np.linspace(y_min, y_max, resolution)
    )
    
    # Interpolate signal strength across the grid
    grid_signal = griddata(
        (x_coords, y_coords), 
        signals, 
        (grid_x, grid_y), 
        method='cubic',
        fill_value=min(signals)
    )
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Custom colormap: red (weak) -> yellow -> green (strong)
    colors = ['#d62728', '#ff7f0e', '#ffff00', '#90ee90', '#2ca02c']
    n_bins = 100
    cmap = LinearSegmentedColormap.from_list('wifi', colors, N=n_bins)
    
    # Create heat map
    heatmap = ax.contourf(grid_x, grid_y, grid_signal, levels=20, cmap=cmap, alpha=0.8)
    
    # Add contour lines
    contours = ax.contour(grid_x, grid_y, grid_signal, levels=10, colors='black', alpha=0.3, linewidths=0.5)
    ax.clabel(contours, inline=True, fontsize=8, fmt='%d dBm')
    
    # Plot actual measurement points
    scatter = ax.scatter(x_coords, y_coords, c=signals, cmap=cmap, 
                        s=100, edgecolors='black', linewidths=2, 
                        marker='o', zorder=5, alpha=0.9)
    
    # Add room labels if available
    for point in data:
        if point.get('room'):
            ax.annotate(point['room'], 
                       (point['x'], point['y']),
                       xytext=(5, 5), 
                       textcoords='offset points',
                       fontsize=8,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
    
    # Add colorbar
    cbar = plt.colorbar(heatmap, ax=ax, label='Signal Strength (dBm)')
    
    # Add reference markers for signal quality
    quality_levels = {
        -50: 'Excellent',
        -60: 'Good',
        -70: 'Fair',
        -80: 'Poor'
    }
    
    for level, label in quality_levels.items():
        if min(signals) <= level <= max(signals):
            cbar.ax.plot([0, 1], [level, level], 'k--', linewidth=1, alpha=0.5)
            cbar.ax.text(1.1, level, label, va='center', fontsize=8)
    
    # Labels and title
    ax.set_xlabel('X Position (meters)', fontsize=12)
    ax.set_ylabel('Y Position (meters)', fontsize=12)
    ax.set_title('WiFi Signal Strength Heat Map', fontsize=16, fontweight='bold', pad=20)
    
    # Grid
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_aspect('equal')
    
    # Add statistics box
    stats_text = f"Data Points: {len(data)}\n"
    stats_text += f"Best Signal: {max(signals)} dBm\n"
    stats_text += f"Worst Signal: {min(signals)} dBm\n"
    stats_text += f"Average: {np.mean(signals):.1f} dBm"
    
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ Heat map saved to {output_file}")
    
    return fig

def create_3d_visualization(data, output_file='wifi_3d.png'):
    """Create a 3D surface plot of WiFi signal strength."""
    from mpl_toolkits.mplot3d import Axes3D
    
    x_coords = [point['x'] for point in data]
    y_coords = [point['y'] for point in data]
    signals = [point['signal_dbm'] for point in data]
    
    # Create grid
    x_min, x_max = min(x_coords) - 1, max(x_coords) + 1
    y_min, y_max = min(y_coords) - 1, max(y_coords) + 1
    
    grid_x, grid_y = np.meshgrid(
        np.linspace(x_min, x_max, 50),
        np.linspace(y_min, y_max, 50)
    )
    
    grid_signal = griddata(
        (x_coords, y_coords), 
        signals, 
        (grid_x, grid_y), 
        method='cubic',
        fill_value=min(signals)
    )
    
    # Create 3D plot
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Surface plot
    surf = ax.plot_surface(grid_x, grid_y, grid_signal, cmap='RdYlGn', 
                          alpha=0.8, edgecolor='none')
    
    # Scatter plot of actual points
    ax.scatter(x_coords, y_coords, signals, c='black', s=50, alpha=0.6)
    
    # Labels
    ax.set_xlabel('X Position (meters)', fontsize=10)
    ax.set_ylabel('Y Position (meters)', fontsize=10)
    ax.set_zlabel('Signal Strength (dBm)', fontsize=10)
    ax.set_title('WiFi Signal Strength - 3D View', fontsize=14, fontweight='bold', pad=20)
    
    # Colorbar
    fig.colorbar(surf, ax=ax, label='Signal Strength (dBm)', shrink=0.5)
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"✓ 3D visualization saved to {output_file}")
    
    return fig

def analyze_dead_zones(data, threshold=-75):
    """
    Analyze and report dead zones (areas with signal below threshold).
    
    Args:
        data: WiFi data points
        threshold: Signal strength threshold for dead zones (default: -75 dBm)
    """
    print(f"\n{'='*60}")
    print("Dead Zone Analysis")
    print(f"{'='*60}")
    print(f"Threshold: {threshold} dBm")
    
    dead_zones = [point for point in data if point['signal_dbm'] < threshold]
    good_zones = [point for point in data if point['signal_dbm'] >= -60]
    
    print(f"\n📊 Signal Quality Breakdown:")
    print(f"   Excellent (≥-50 dBm): {len([p for p in data if p['signal_dbm'] >= -50])}")
    print(f"   Good (-50 to -60 dBm): {len([p for p in data if -60 <= p['signal_dbm'] < -50])}")
    print(f"   Fair (-60 to -70 dBm): {len([p for p in data if -70 <= p['signal_dbm'] < -60])}")
    print(f"   Poor (-70 to -80 dBm): {len([p for p in data if -80 <= p['signal_dbm'] < -70])}")
    print(f"   Very Poor (<-80 dBm): {len([p for p in data if p['signal_dbm'] < -80])}")
    
    if dead_zones:
        print(f"\n⚠️  Found {len(dead_zones)} dead zone location(s):")
        for i, point in enumerate(dead_zones, 1):
            location = f"({point['x']}, {point['y']})"
            room = f" - {point['room']}" if point.get('room') else ""
            print(f"   {i}. {location}{room}: {point['signal_dbm']} dBm")
    else:
        print(f"\n✓ No dead zones found! All areas have signal ≥ {threshold} dBm")
    
    if good_zones:
        print(f"\n✓ Best coverage areas:")
        # Sort by signal strength
        good_zones_sorted = sorted(good_zones, key=lambda x: x['signal_dbm'], reverse=True)[:3]
        for i, point in enumerate(good_zones_sorted, 1):
            location = f"({point['x']}, {point['y']})"
            room = f" - {point['room']}" if point.get('room') else ""
            print(f"   {i}. {location}{room}: {point['signal_dbm']} dBm")
    
    print(f"\n{'='*60}\n")

def main():
    """Main visualization function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Visualize WiFi signal strength data')
    parser.add_argument('--data', default='wifi_data.json', help='Input data file')
    parser.add_argument('--output', default='wifi_heatmap.png', help='Output image file')
    parser.add_argument('--3d', action='store_true', help='Also create 3D visualization')
    parser.add_argument('--threshold', type=int, default=-75, help='Dead zone threshold (dBm)')
    
    args = parser.parse_args()
    
    # Load data
    data = load_data(args.data)
    if data is None:
        return
    
    # Analyze dead zones
    analyze_dead_zones(data, args.threshold)
    
    # Create heat map
    create_heatmap(data, args.output)
    
    # Create 3D visualization if requested
    if args.__dict__.get('3d', False):
        create_3d_visualization(data, 'wifi_3d.png')
    
    print("\n✓ Visualization complete!")
    print(f"  View your heat map: {args.output}")

if __name__ == '__main__':
    main()
