# 🎥 Samsung Gear 360 Video Stitcher

Convert dual fisheye video from Samsung Gear 360 cameras into beautiful equirectangular panoramas with an easy-to-use GUI.

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-GPL--3.0-blue)

---

## ✨ Features

- 🎬 **Single Video Processing** - Convert individual videos with custom settings
- 📁 **Batch Processing** - Process multiple videos at once
- 👁️ **Live Preview** - See what your output will look like before processing
- 🎯 **Advanced Calibration** - Fine-tune distortion correction
- 💾 **Preset Management** - Save and load your favorite settings
- 🔄 **Rotation Support** - Rotate output by 0°, 90°, 180°, or 270°
- 🎵 **Audio Preservation** - Keeps original audio (requires ffmpeg)
- 🖥️ **Cross-Platform** - Works on Windows, macOS, and Linux
- 🌙 **Dark Mode** - Easy on the eyes during long processing sessions

---

## 📋 Table of Contents

- [System Requirements](#-system-requirements)
- [Installation](#-installation)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Quick Start](#-quick-start)
- [User Guide](#-user-guide)
- [Adding to Start Menu](#-adding-to-start-menu)
- [Command Line Usage](#-command-line-usage)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Contributing](#-contributing)
- [License](#-license)

---

## 💻 System Requirements

- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended for 4K video)
- **Storage**: Depends on video size (output is typically similar to input)
- **OS**: Windows 10+, macOS 10.14+, or Linux (Ubuntu 20.04+)

---

## 📦 Installation

### Windows

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ⚠️ **Important**: Check "Add Python to PATH" during installation
4. Click "Install Now"

#### Step 2: Install Dependencies

Open Command Prompt (Win + R, type `cmd`, press Enter) and run:

```batch
pip install opencv-python numpy pillow
```

**Alternative using Chocolatey:**
```batch
choco install python opencv numpy pillow
```

#### Step 3: Install FFmpeg (Optional - for audio support)

**Option A: Using Chocolatey (Recommended)**
```batch
choco install ffmpeg
```

**Option B: Using winget**
```batch
winget install FFmpeg
```

**Option C: Manual Installation**
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to your System PATH:
   - Right-click "This PC" → Properties
   - Advanced System Settings → Environment Variables
   - Edit "Path" under System Variables
   - Add new entry: `C:\ffmpeg\bin`

#### Step 4: Download Gear 360 Stitcher

**Option A: Using Git (Recommended)**

1. Open Command Prompt
2. Navigate to where you want to install (e.g., `cd C:\`)
3. Clone the repository:
```batch
git clone -b GUI https://github.com/PhobiaGH/Samsung_Gear_360.git
cd Samsung_Gear_360
```

*Note: If you don't have Git installed, download it from [git-scm.com](https://git-scm.com/download/win)*

**Option B: Download ZIP**

1. Go to the [GitHub repository](https://github.com/PhobiaGH/Samsung_Gear_360)
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract to a folder (e.g., `C:\Gear360Stitcher`)

#### Step 5: Run the Application

Double-click `gear360_gui.py` or open Command Prompt in the folder and run:
```batch
python gear360_gui.py
```

---

### macOS

#### Step 1: Install Python

macOS comes with Python, but we recommend installing the latest version:

**Option A: Using Homebrew (Recommended)**
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

**Option B: Using MacPorts**
```bash
sudo port install python311
```

**Option C: Official Installer**
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer package

#### Step 2: Install Dependencies

**Option A: Using Homebrew (Recommended)**
```bash
brew install opencv numpy python-pillow
```

**Option B: Using MacPorts**
```bash
sudo port install py311-opencv py311-numpy py311-pillow
```

**Option C: Using pip (if preferred)**
```bash
pip3 install opencv-python numpy pillow
```

#### Step 3: Install FFmpeg (Optional - for audio support)

**Using Homebrew:**
```bash
brew install ffmpeg
```

**Using MacPorts:**
```bash
sudo port install ffmpeg
```

#### Step 4: Download Gear 360 Stitcher

**Option A: Using Git (Recommended)**

Open Terminal and run:
```bash
cd ~/Applications  # or your preferred location
git clone -b GUI https://github.com/PhobiaGH/Samsung_Gear_360.git
cd Samsung_Gear_360
```

*Note: macOS 10.9+ includes Git. If needed, install with: `brew install git`*

**Option B: Download ZIP**

1. Go to the [GitHub repository](https://github.com/PhobiaGH/Samsung_Gear_360)
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract to a folder (e.g., `~/Applications/Gear360Stitcher`)

#### Step 5: Run the Application

Open Terminal in the folder and run:
```bash
python3 gear360_gui.py
```

---

### Linux

#### Step 1: Install Python

Most Linux distributions include Python. To ensure you have Python 3.8+:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3 python3-tkinter
```

**Arch Linux:**
```bash
sudo pacman -S python tk
```

**openSUSE:**
```bash
sudo zypper install python3 python3-tk
```

#### Step 2: Install Dependencies

⚠️ **Important**: Using system package managers is strongly recommended on Linux to avoid breaking your system. Only use pip in a virtual environment if system packages aren't available.

**Ubuntu/Debian:**
```bash
sudo apt install python3-opencv python3-numpy python3-pil python3-pil.imagetk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-opencv python3-numpy python3-pillow python3-pillow-tk
```

**Arch Linux:**
```bash
sudo pacman -S python-opencv python-numpy python-pillow
```

**openSUSE:**
```bash
sudo zypper install python3-opencv python3-numpy python3-Pillow
```

**Alpine Linux:**
```bash
sudo apk add py3-opencv py3-numpy py3-pillow
```

**Gentoo:**
```bash
sudo emerge dev-python/opencv-python dev-python/numpy dev-python/pillow
```

**Alternative: Using pip in a virtual environment (if system packages unavailable)**

⚠️ **Only use this method if the above package manager options don't work:**

```bash
# Create a virtual environment
python3 -m venv ~/gear360-venv

# Activate it
source ~/gear360-venv/bin/activate

# Install dependencies
pip install opencv-python numpy pillow

# Note: You'll need to activate this environment each time you run the app
```

#### Step 3: Install FFmpeg (Optional - for audio support)

**Ubuntu/Debian:**
```bash
sudo apt install ffmpeg
```

**Fedora/RHEL:**
```bash
sudo dnf install ffmpeg
```

**Arch Linux:**
```bash
sudo pacman -S ffmpeg
```

**openSUSE:**
```bash
sudo zypper install ffmpeg
```

**Alpine Linux:**
```bash
sudo apk add ffmpeg
```

**Gentoo:**
```bash
sudo emerge media-video/ffmpeg
```

#### Step 4: Download Gear 360 Stitcher

**Option A: Using Git (Recommended)**

```bash
cd ~  # or your preferred location
git clone -b GUI https://github.com/PhobiaGH/Samsung_Gear_360.git
cd Samsung_Gear_360
chmod +x gear360_gui.py gear360_stitcher.py
```

*Note: Install Git if needed:*
```bash
sudo apt install git        # Ubuntu/Debian
sudo dnf install git        # Fedora/RHEL
sudo pacman -S git          # Arch Linux
sudo zypper install git     # openSUSE
sudo apk add git            # Alpine
sudo emerge dev-vcs/git     # Gentoo
```

**Option B: Download ZIP**

1. Go to the [GitHub repository](https://github.com/PhobiaGH/Samsung_Gear_360)
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract to a folder (e.g., `~/Samsung_Gear_360`)
5. Make scripts executable:
```bash
chmod +x gear360_gui.py gear360_stitcher.py
```

#### Step 5: Run the Application

```bash
python3 gear360_gui.py
```

**If you used a virtual environment:**
```bash
source ~/gear360-venv/bin/activate
python3 gear360_gui.py
```

---

## 🚀 Quick Start

### Processing Your First Video

1. **Launch the application**
   - Run `gear360_gui.py` using your preferred method
   
2. **Single Video Tab**
   - Click "Browse..." next to "Input Video"
   - Select your Gear 360 dual fisheye video
   - Click "Browse..." next to "Output Video" (or use auto-suggested name)
   
3. **Adjust Settings (Optional)**
   - Output Width: 3840px (4K) is default
   - Output Height: 1920px (4K) is default
   - Rotation: 0° (no rotation) is default
   
4. **Generate Preview (Recommended)**
   - Click "👁 Generate Preview"
   - Switch to "Preview" tab to see the result
   - If satisfied, return to "Single Video" tab
   
5. **Stitch Video**
   - Click "🎬 Stitch Video"
   - Wait for processing to complete
   - Find your stitched video in the output location

### Using Presets

1. Configure your preferred settings (width, height, rotation)
2. Click "Save Current as Preset"
3. Enter a name (e.g., "My 4K Setup")
4. Next time, just select it from the dropdown!

---

## 📖 User Guide

### Single Video Processing

The main tab for processing individual videos.

**Settings:**
- **Output Width/Height**: Resolution of the final panorama
  - 3840x1920 = 4K
  - 1920x960 = Full HD
  - 7680x3840 = 8K (requires powerful hardware)
  
- **Rotation**: Rotate the final output
  - 0° = No rotation (landscape)
  - 90° = Portrait mode
  - 180° = Upside down
  - 270° = Portrait (opposite)

- **Calibration**: Optional JSON file with lens correction data

**Workflow:**
1. Select input video
2. Choose output location
3. Adjust settings or load preset
4. Generate preview (optional but recommended)
5. Click "Stitch Video"

---

### Batch Processing

Process multiple videos with the same settings.

**How to Use:**
1. Switch to "📁 Batch Processing" tab
2. Click "➕ Add Videos" to select multiple files
3. Choose an output directory for all stitched videos
4. Configure settings in the "Single Video" tab (settings apply to all)
5. Click "🚀 Process All Videos"

**Tips:**
- Output files are automatically named `[original_name]_stitched.mp4`
- Progress shows current video and overall completion
- All videos use the same calibration and settings

---

### Preview Feature

Test your settings before processing the entire video.

**How to Use:**
1. Select an input video in "Single Video" tab
2. Configure your settings
3. Click "👁 Generate Preview"
4. Switch to "👁 Preview" tab
5. Use scrollbars to navigate the preview image
6. Click "💾 Save Preview" to export the frame

**Benefits:**
- Saves time by testing settings first
- See exactly what the output will look like
- Adjust calibration without processing full video

---

### Advanced Calibration

Fine-tune lens distortion correction for optimal results.

**Settings:**
- **K1 (Radial Distortion)**: Primary barrel/pincushion correction
  - More negative (e.g., -0.35): Less edge stretching
  - Less negative (e.g., -0.20): More edge coverage
  - Default: -0.28
  
- **K2 (Secondary Radial)**: Fine-tuning correction
  - Positive: Outward correction
  - Negative: Inward correction
  - Default: 0.05

**When to Adjust:**
- Edges appear stretched: Make K1 more negative
- Edges appear compressed: Make K1 less negative
- Fine distortion issues: Adjust K2 slightly

**Workflow:**
1. Switch to "🎯 Calibration" tab
2. Select input video
3. Adjust K1 and K2 values
4. Click "💾 Save Calibration File"
5. Load this file in "Single Video" tab when stitching

---

## 🔧 Adding to Start Menu

### Windows

#### Method 1: Create Desktop Shortcut (Easiest)

1. Right-click on `gear360_gui.py`
2. Select "Create shortcut"
3. Right-click the shortcut → Properties
4. In "Target" field, change to:
   ```
   C:\Users\YourUsername\AppData\Local\Programs\Python\Python311\pythonw.exe "C:\Samsung_Gear_360\gear360_gui.py"
   ```
   (Adjust Python path and script path based on your installation location)
5. Click "Change Icon..." to add a custom icon (optional)
6. Click OK
7. Drag shortcut to Desktop or pin to Start Menu

#### Method 2: Create Windows Batch File

1. Create a new file called `Gear360Stitcher.bat` in the same folder:
   ```batch
   @echo off
   cd /d "%~dp0"
   pythonw gear360_gui.py
   ```
2. Right-click the `.bat` file → "Send to" → "Desktop (create shortcut)"
3. Right-click the shortcut → "Pin to Start"

#### Method 3: Add to Start Menu Folder

1. Press Win + R, type `shell:programs`, press Enter
2. Create a new folder called "Gear360 Stitcher"
3. Create a shortcut to `gear360_gui.py` inside this folder
4. The app will now appear in your Start Menu

---

### macOS

#### Method 1: Create Application Bundle (Recommended)

1. Open **Automator** (Applications → Utilities → Automator)
2. Choose "Application" as document type
3. Search for "Run Shell Script" action
4. Add this script:
   ```bash
   cd ~/Applications/Samsung_Gear_360
   /usr/bin/python3 gear360_gui.py
   ```
5. Save as "Gear360 Stitcher" in Applications folder
6. Now accessible from Launchpad and Spotlight

*Note: Adjust the path if you cloned to a different location*

#### Method 2: Create Alias

1. Right-click `gear360_gui.py`
2. Select "Make Alias"
3. Rename to "Gear 360 Stitcher"
4. Drag to Applications folder
5. Double-click to run (may need to select Python as default application)

#### Method 3: Add to Dock

1. Open Terminal in the script folder
2. Run: `python3 gear360_gui.py`
3. While running, right-click the Python icon in Dock
4. Options → Keep in Dock

---

### Linux

#### Method 1: Create Desktop Entry (Ubuntu/GNOME)

1. Create a file called `gear360-stitcher.desktop`:
   ```bash
   nano ~/.local/share/applications/gear360-stitcher.desktop
   ```

2. Add this content:
   ```ini
   [Desktop Entry]
   Type=Application
   Name=Gear 360 Stitcher
   Comment=Stitch Samsung Gear 360 videos
   Exec=python3 /home/YOUR_USERNAME/Samsung_Gear_360/gear360_gui.py
   Icon=video-x-generic
   Terminal=false
   Categories=AudioVideo;Video;
   ```

3. Replace `YOUR_USERNAME` with your actual username and adjust the path if you cloned to a different location
4. Save and close (Ctrl + X, Y, Enter)
5. Make it executable:
   ```bash
   chmod +x ~/.local/share/applications/gear360-stitcher.desktop
   ```

6. The app will now appear in your application menu

**If you used a virtual environment**, modify the Exec line:
```ini
Exec=/bin/bash -c 'source ~/gear360-venv/bin/activate && python3 /home/YOUR_USERNAME/Samsung_Gear_360/gear360_gui.py'
```

#### Method 2: Create Shell Script

1. Create a launcher script:
   ```bash
   nano ~/bin/gear360-stitcher
   ```

2. Add this content:
   ```bash
   #!/bin/bash
   cd ~/Samsung_Gear_360
   python3 gear360_gui.py
   ```

   **If using virtual environment:**
   ```bash
   #!/bin/bash
   source ~/gear360-venv/bin/activate
   cd ~/Samsung_Gear_360
   python3 gear360_gui.py
   ```

3. Make it executable:
   ```bash
   chmod +x ~/bin/gear360-stitcher
   ```

4. Run from terminal with: `gear360-stitcher`

*Note: Adjust the path if you cloned to a different location*

#### Method 3: Add to Favorites (GNOME)

1. Create desktop entry (Method 1)
2. Open Activities/Show Applications
3. Find "Gear 360 Stitcher"
4. Right-click → "Add to Favorites"

---

## 💻 Command Line Usage

For advanced users or server environments without GUI:

### Basic Stitching
```bash
python3 gear360_stitcher.py stitch -i input.mp4 -o output.mp4
```

### With Custom Resolution
```bash
python3 gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -w 4096 -t 2048
```

### With Rotation
```bash
python3 gear360_stitcher.py stitch -i input.mp4 -o output.mp4 --rotate 90
```

### With Calibration File
```bash
python3 gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -c calibration.json
```

### Create Calibration File
```bash
python3 gear360_stitcher.py calibrate -i input.mp4 -o calibration.json
```

### Complete Example
```bash
# First, calibrate (optional)
python3 gear360_stitcher.py calibrate -i sample.mp4 -o my_calibration.json

# Then stitch with custom settings
python3 gear360_stitcher.py stitch \
  -i input.mp4 \
  -o output.mp4 \
  -c my_calibration.json \
  -w 3840 \
  -t 1920 \
  --rotate 90
```

### Get Help
```bash
python3 gear360_stitcher.py --help
python3 gear360_stitcher.py stitch --help
python3 gear360_stitcher.py calibrate --help
```

---

## 🔍 Troubleshooting

### "Module not found" errors

**Problem**: Python can't find required packages

**Solution**:

**Linux (Recommended)**: Use system package manager (see installation section)

**Windows/macOS/Linux (alternative)**:
```bash
# Reinstall all dependencies
pip3 install --upgrade opencv-python numpy pillow
```

**Linux (if system packages don't work)**: Use a virtual environment:
```bash
python3 -m venv ~/gear360-venv
source ~/gear360-venv/bin/activate
pip install opencv-python numpy pillow
```

### "No module named 'tkinter'"

**Problem**: Tkinter is not installed

**Solution**:
- **Windows**: Reinstall Python with "tcl/tk and IDLE" option checked
- **macOS**: Already included with Python
- **Linux**: 
  ```bash
  sudo apt install python3-tk        # Ubuntu/Debian
  sudo dnf install python3-tkinter   # Fedora/RHEL
  sudo pacman -S tk                  # Arch Linux
  sudo zypper install python3-tk     # openSUSE
  ```

### Video has no audio

**Problem**: FFmpeg is not installed

**Solution**: Install FFmpeg following the installation instructions for your platform above

### Preview shows distorted image

**Problem**: Default calibration doesn't match your camera

**Solution**: 
1. Go to "Calibration" tab
2. Adjust K1 and K2 values
3. Generate preview again
4. Save calibration when satisfied

### "Could not open video file"

**Problem**: Video file is corrupted or unsupported format

**Solution**:
- Check if video plays in a media player
- Try converting to MP4 with VLC or similar
- Ensure file path doesn't contain special characters

### Application runs slowly

**Problem**: Insufficient system resources

**Solution**:
- Reduce output resolution (try 1920x960 instead of 3840x1920)
- Close other applications
- Ensure you have enough free disk space (2x video size)

### "Permission denied" errors (Linux/macOS)

**Problem**: Script doesn't have execute permission

**Solution**:
```bash
chmod +x gear360_gui.py gear360_stitcher.py
```

### ImportError on Linux after using pip

**Problem**: Mixed pip and system packages causing conflicts

**Solution**:
1. Uninstall pip-installed packages:
   ```bash
   pip3 uninstall opencv-python numpy pillow
   ```
2. Install using system package manager (see Linux installation section)
3. Or use a virtual environment to isolate pip packages

---

## ❓ FAQ

### Q: What video formats are supported?
**A**: MP4, MOV, and AVI files. MP4 is recommended for best compatibility.

### Q: How long does processing take?
**A**: Depends on video length and resolution. A 5-minute 4K video typically takes 15-30 minutes on modern hardware.

### Q: Can I process videos from other 360° cameras?
**A**: This tool is optimized for Samsung Gear 360 dual fisheye format. Other cameras may not work correctly.

### Q: Will the output work with VR headsets?
**A**: Yes! The equirectangular format is compatible with most VR players and platforms (YouTube 360, Facebook 360, Oculus).

### Q: How do I improve quality?
**A**: 
- Use higher output resolution (4K or 8K)
- Adjust calibration settings
- Ensure input video is high quality
- Use ffmpeg for audio to avoid re-encoding

### Q: Can I cancel processing?
**A**: Yes, click the "❌ Cancel" button. Processing will stop at the next frame.

### Q: Where are presets saved?
**A**: In `stitcher_presets.json` in the same folder as the scripts.

### Q: Can I run this on a server without GUI?
**A**: Yes! Use the command-line interface. See the [Command Line Usage](#-command-line-usage) section for examples.

### Q: Should I use pip or system packages on Linux?
**A**: Always prefer system package managers (apt, dnf, pacman, etc.) on Linux. They prevent dependency conflicts and system breakage. Only use pip in a virtual environment if system packages aren't available.

### Q: How do I clone from a specific branch?
**A**: Use `git clone -b BRANCH_NAME URL`. For example:
```bash
git clone -b GUI https://github.com/PhobiaGH/Samsung_Gear_360.git
```

---

## 🤝 Contributing

Found a bug or want to add a feature? Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

### What this means:
- ✅ You can use this software for any purpose
- ✅ You can modify the source code
- ✅ You can distribute the software
- ✅ You can distribute your modifications
- ⚠️ You must disclose the source code when distributing
- ⚠️ You must license your modifications under GPL-3.0
- ⚠️ You must include the original license and copyright notice

For more information, visit [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html)

---

## 🙏 Credits

Special thanks to a certain anonymous kitty for mathematical contributions.

```
  /\_/\
 ( o.o )
  > ^ <
 /|   |\
(_|   |_)
```

---

## 📞 Support

Having issues? Check the [Troubleshooting](#-troubleshooting) section first.

For additional help:
- Review the [User Guide](#-user-guide)
- Check that all dependencies are installed correctly
- Ensure your Python version is 3.8 or higher

---

**Happy Stitching! 🎥✨**
