# Tapo webcam RTSP Screenshot Tool

A Python tool for capturing screenshots from Tapo C51A security cameras via RTSP protocol. Supports configuration files for easy credential management and offers both OpenCV and FFmpeg backends.

## Features

- 📸 Capture high-quality screenshots from Tapo C51A cameras
- 🔧 Configuration file support for secure credential storage
- 🎯 Two backend options: OpenCV and FFmpeg
- ⏰ Automatic timestamp-based file naming
- 🎛️ Configurable image quality and stream selection
- 🔒 Command-line credential override capability
- 📁 Automatic output directory creation

## Requirements

### For OpenCV Version
```bash
pip install opencv-python configparser
```

### For FFmpeg Version
- Python 3.6+
- FFmpeg installed on system

**Install FFmpeg:**
- **Ubuntu/Debian:** `sudo apt install ffmpeg`
- **CentOS/RHEL:** `sudo yum install ffmpeg`
- **macOS:** `brew install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/tapo-screenshot-tool.git
   cd tapo-screenshot-tool
   ```

2. Install dependencies:
   ```bash
   pip install opencv-python configparser
   ```

3. Create configuration file:
   ```bash
   python tapo_screenshot.py --create-config
   ```

4. Edit `tapo_config.ini` with your camera settings.

## Configuration

The tool uses an INI configuration file to store camera settings:

```ini
[camera]
ip = 192.168.1.100
username = admin
password = your_password_here
port = 554
stream = stream1

[settings]
timeout = 10
default_output_dir = ./screenshots
image_quality = 95
```

### Configuration Options

**Camera Settings:**
- `ip`: Camera IP address
- `username`: Camera login username
- `password`: Camera login password
- `port`: RTSP port (default: 554)
- `stream`: Stream quality (`stream1` = high, `stream2` = low)

**Application Settings:**
- `timeout`: Connection timeout in seconds
- `default_output_dir`: Directory to save screenshots
- `image_quality`: JPEG quality 0-100 (OpenCV) or high/medium/low (FFmpeg)

## Usage

### Basic Usage
```bash
# Use default config file (tapo_config.ini)
python tapo_screenshot.py

# Use custom config file
python tapo_screenshot.py --config my_camera.ini

# Specify output filename
python tapo_screenshot.py --output /path/to/screenshot.jpg
```

### Command Line Overrides
```bash
# Override config settings
python tapo_screenshot.py --ip 192.168.1.101 --password newpass

# Use low quality stream
python tapo_screenshot.py --stream stream2

# Set custom timeout
python tapo_screenshot.py --timeout 15
```

### Create Configuration File
```bash
python tapo_screenshot.py --create-config
python tapo_screenshot.py --create-config --config custom_config.ini
```

## Scripts

### 1. `tapo_screenshot.py` (OpenCV Backend)
Primary script using OpenCV for image capture. Best for most use cases.

### 2. `tapo_ffmpeg_screenshot.py` (FFmpeg Backend)
Alternative using FFmpeg for environments where OpenCV has issues.

Both scripts share the same command-line interface and configuration format.

## Troubleshooting

### OpenGL Library Error
If you encounter `ImportError: libGL.so.1: cannot open shared object file`:

**Solution 1 - Install OpenGL libraries:**
```bash
# Ubuntu/Debian
sudo apt install libgl1-mesa-glx libglib2.0-0

# CentOS/RHEL
sudo yum install mesa-libGL
```

**Solution 2 - Use headless OpenCV:**
```bash
pip uninstall opencv-python
pip install opencv-python-headless
```

**Solution 3 - Use FFmpeg backend:**
```bash
python tapo_ffmpeg_screenshot.py
```

### Common Issues

**Connection Timeout:**
- Verify camera IP and network connectivity
- Check if RTSP is enabled in camera settings
- Try increasing timeout value
- Test with `stream2` (lower bandwidth)

**Authentication Failed:**
- Verify username and password
- Ensure camera allows RTSP connections
- Check if multiple login attempts locked the account

**Empty/Corrupted Images:**
- Try different stream quality (`stream1` vs `stream2`)
- Increase timeout value
- Check camera's RTSP URL format

### RTSP URL Formats
Standard Tapo C51A RTSP URLs:
- High quality: `rtsp://username:password@ip:554/stream1`
- Low quality: `rtsp://username:password@ip:554/stream2`

## Security

- Store configuration files securely
- Set appropriate file permissions: `chmod 600 tapo_config.ini`
- Add `*.ini` to `.gitignore` to avoid committing credentials
- Use environment variables for CI/CD deployments

## Examples

### Automated Screenshots with Cron
```bash
# Take screenshot every hour
0 * * * * /usr/bin/python3 /path/to/tapo_screenshot.py

# Daily screenshot at 8 AM
0 8 * * * /usr/bin/python3 /path/to/tapo_screenshot.py --output /backups/daily_$(date +\%Y\%m\%d).jpg
```

### Multiple Cameras
Create separate config files for each camera:
```bash
python tapo_screenshot.py --config front_door.ini
python tapo_screenshot.py --config back_yard.ini
python tapo_screenshot.py --config garage.ini
```

### Integration with Home Automation
```bash
# Capture screenshot when motion detected
python tapo_screenshot.py --output /var/www/html/latest_motion.jpg
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Tapo camera RTSP implementation
- OpenCV and FFmpeg communities
- Contributors and testers

## Changelog

### v1.0.0
- Initial release with OpenCV backend
- Configuration file support
- Basic RTSP screenshot functionality

### v1.1.0
- Added FFmpeg backend alternative
- Improved error handling
- Enhanced documentation
- Multiple stream quality options

---

⭐ If this tool helps you, please consider starring the repository!

📧 For issues and feature requests, please use the GitHub Issues tab.
