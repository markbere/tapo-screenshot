#!/usr/bin/env python3
"""
Tapo C51A RTSP Screenshot Script
Takes a screenshot from Tapo C51A camera via RTSP stream
Uses configuration file for camera settings
"""

import sys
import os
import configparser
from datetime import datetime
import argparse

# Handle OpenCV import with better error message
try:
    import cv2
except ImportError as e:
    if "libGL.so.1" in str(e):
        print("Error: OpenGL libraries not found.")
        print("Solutions:")
        print("1. Install OpenGL libraries:")
        print("   Ubuntu/Debian: sudo apt install libgl1-mesa-glx libglib2.0-0")
        print("   CentOS/RHEL: sudo yum install mesa-libGL")
        print("2. Or use headless OpenCV:")
        print("   pip uninstall opencv-python")
        print("   pip install opencv-python-headless")
        sys.exit(1)
    else:
        print(f"Error importing OpenCV: {e}")
        print("Please install OpenCV: pip install opencv-python")
        sys.exit(1)

def create_default_config(config_path):
    """Create a default configuration file"""
    config = configparser.ConfigParser()
    
    config['camera'] = {
        'ip': '192.168.1.100',
        'username': 'admin',
        'password': 'your_password_here',
        'port': '554',
        'stream': 'stream1'
    }
    
    config['settings'] = {
        'timeout': '10',
        'default_output_dir': './screenshots',
        'image_quality': '95'
    }
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(config_path) if os.path.dirname(config_path) else '.', exist_ok=True)
    
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    
    print(f"Default configuration file created: {config_path}")
    print("Please edit the file to set your camera credentials and settings.")

def load_config(config_path):
    """Load configuration from file"""
    if not os.path.exists(config_path):
        print(f"Configuration file not found: {config_path}")
        create_default_config(config_path)
        return None
    
    config = configparser.ConfigParser()
    config.read(config_path)
    
    # Validate required sections
    if 'camera' not in config or 'settings' not in config:
        print("Error: Invalid configuration file format")
        return None
    
    return config

def take_screenshot(rtsp_url, output_path=None, timeout=10, image_quality=95):
    """
    Capture a screenshot from RTSP stream
    
    Args:
        rtsp_url (str): RTSP stream URL
        output_path (str): Path to save screenshot (optional)
        timeout (int): Connection timeout in seconds
        image_quality (int): JPEG quality (0-100)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    # Create VideoCapture object
    cap = cv2.VideoCapture(rtsp_url)
    
    # Set timeout (in milliseconds)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, timeout * 1000)
    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, timeout * 1000)
    
    try:
        # Check if camera opened successfully
        if not cap.isOpened():
            print(f"Error: Could not open RTSP stream")
            return False
        
        print("Connected to RTSP stream, capturing frame...")
        
        # Capture frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame from stream")
            return False
        
        # Generate filename if not provided
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{timestamp}.jpg"
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set JPEG quality
        encode_params = [cv2.IMWRITE_JPEG_QUALITY, image_quality]
        
        # Save the frame
        success = cv2.imwrite(output_path, frame, encode_params)
        
        if success:
            print(f"Screenshot saved successfully: {output_path}")
            return True
        else:
            print("Error: Failed to save screenshot")
            return False
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False
        
    finally:
        # Release the capture
        cap.release()

def main():
    parser = argparse.ArgumentParser(description='Take screenshot from Tapo C51A camera')
    parser.add_argument('--config', '-c', default='tapo_config.ini', 
                       help='Configuration file path (default: tapo_config.ini)')
    parser.add_argument('--output', '-o', help='Output filename (optional)')
    parser.add_argument('--create-config', action='store_true',
                       help='Create a default configuration file and exit')
    
    # Override options (optional, will override config file values)
    parser.add_argument('--ip', help='Camera IP address (overrides config)')
    parser.add_argument('--username', help='Camera username (overrides config)')
    parser.add_argument('--password', help='Camera password (overrides config)')
    parser.add_argument('--port', type=int, help='RTSP port (overrides config)')
    parser.add_argument('--stream', choices=['stream1', 'stream2'], 
                       help='Stream quality (overrides config)')
    parser.add_argument('--timeout', type=int, help='Connection timeout in seconds (overrides config)')
    
    args = parser.parse_args()
    
    # Handle create-config option
    if args.create_config:
        create_default_config(args.config)
        sys.exit(0)
    
    # Load configuration
    config = load_config(args.config)
    if config is None:
        sys.exit(1)
    
    try:
        # Get camera settings from config or command line overrides
        ip = args.ip or config.get('camera', 'ip')
        username = args.username or config.get('camera', 'username')
        password = args.password or config.get('camera', 'password')
        port = args.port or config.getint('camera', 'port')
        stream = args.stream or config.get('camera', 'stream')
        timeout = args.timeout or config.getint('settings', 'timeout')
        image_quality = config.getint('settings', 'image_quality')
        default_output_dir = config.get('settings', 'default_output_dir')
        
        # Validate required settings
        if not all([ip, username, password]):
            print("Error: IP, username, and password must be specified in config file or command line")
            sys.exit(1)
            
    except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
        print(f"Error reading configuration: {str(e)}")
        print("Try running with --create-config to generate a default configuration file")
        sys.exit(1)
    
    # Construct RTSP URL
    rtsp_url = f"rtsp://{username}:{password}@{ip}:{port}/{stream}"
    
    print(f"Connecting to: rtsp://{username}:***@{ip}:{port}/{stream}")
    
    # Handle output path
    output_path = args.output
    if output_path is None and default_output_dir:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = os.path.join(default_output_dir, f"{timestamp}.jpg")
    
    # Take screenshot
    success = take_screenshot(rtsp_url, output_path, timeout, image_quality)
    
    if success:
        print("Screenshot captured successfully!")
        sys.exit(0)
    else:
        print("Failed to capture screenshot!")
        sys.exit(1)

if __name__ == "__main__":
    main()