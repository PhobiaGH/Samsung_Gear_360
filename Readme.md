# Samsung Gear 360 Video Stitcher

A Python application that converts dual fisheye video from the Samsung Gear 360 camera into seamless equirectangular panoramic video with audio preservation.

## Features

- ✨ **Two-step workflow**: Calibrate once, stitch multiple videos (or use defaults)
- 📊 **Real-time progress tracking**: Progress bar, FPS counter, and ETA
- 🎬 **Any video length**: Streams frames efficiently without loading entire video into memory
- 🎯 **Customizable output**: Set your desired panorama resolution
- 💾 **Reusable calibration**: Save and reuse camera parameters across videos
- 🔊 **Audio preservation**: Automatically preserves audio from source video (requires ffmpeg)
- 💻 **Cross-platform**: Works on Windows, Linux, and macOS
- ⚡ **Fast processing**: Uses OpenCV's optimized undistortion functions

## How It Works

The Samsung Gear 360 records video with two fisheye lenses (front and back). This app:
1. Splits the dual fisheye video into left and right views
2. Applies lens distortion correction using camera matrix and distortion coefficients
3. Stitches the corrected views together into a seamless 360° panorama
4. Preserves the original audio track using ffmpeg
5. Outputs standard panoramic video compatible with YouTube, VR players, etc.

## Prerequisites

- **Operating System**: Windows 10/11, Linux, or macOS
- **Python**: 3.7 or higher
- **Camera**: Samsung Gear 360 (or similar dual fisheye camera)
- **ffmpeg**: Required for audio preservation (optional but recommended)

## Installation

### Windows Installation

#### Step 1: Install Python Dependencies

Open **Command Prompt** or **PowerShell** and run:

```bash
pip install opencv-python numpy
```

**Note:** If you encounter build errors with NumPy, use:
```bash
pip install --only-binary :all: opencv-python numpy
```

#### Step 2: Install ffmpeg (for audio preservation)

**Option A: Using Chocolatey (Recommended)**
```bash
choco install ffmpeg
```

**Option B: Manual Installation**
1. Download ffmpeg from https://ffmpeg.org/download.html
2. Extract the archive
3. Add the `bin` folder to your system PATH
4. Verify installation: `ffmpeg -version`

#### Step 3: Download the Application

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/PhobiaGH/Samsung_Gear_360.git
cd Samsung_Gear_360
```

**Option B: Manual Download**
1. Visit https://github.com/PhobiaGH/Samsung_Gear_360
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to your desired location
4. Navigate to the extracted folder

#### Step 4: Verify Installation

```bash
python -c "import cv2, numpy; print(f'OpenCV: {cv2.__version__}, NumPy: {numpy.__version__}')"
```

You should see version numbers without any errors.

---

### Linux Installation

#### Step 1: Install System Dependencies

On **Arch Linux**:
```bash
sudo pacman -S opencv python-opencv python-numpy ffmpeg
```

On **Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install python3-opencv python3-numpy ffmpeg
```

On **Fedora**:
```bash
sudo dnf install python3-opencv python3-numpy ffmpeg
```

#### Step 2: Download the Application

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/PhobiaGH/Samsung_Gear_360.git
cd Samsung_Gear_360
chmod +x gear360_stitcher.py
```

**Option B: Manual Download**
1. Visit https://github.com/PhobiaGH/Samsung_Gear_360
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to your desired location
4. Navigate to the extracted folder
5. Make the script executable:
   ```bash
   chmod +x gear360_stitcher.py
   ```

#### Step 3: Verify Installation

```bash
python3 -c "import cv2, numpy; print(f'OpenCV: {cv2.__version__}, NumPy: {numpy.__version__}')"
```

You should see version numbers without any errors.

---

### macOS Installation

#### Step 1: Install Python Dependencies

```bash
pip3 install opencv-python numpy
```

#### Step 2: Install ffmpeg

Using Homebrew:
```bash
brew install ffmpeg
```

#### Step 3: Download the Application

**Option A: Using Git (Recommended)**
```bash
git clone https://github.com/PhobiaGH/Samsung_Gear_360.git
cd Samsung_Gear_360
chmod +x gear360_stitcher.py
```

**Option B: Manual Download**
1. Visit https://github.com/PhobiaGH/Samsung_Gear_360
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file to your desired location
4. Navigate to the extracted folder
5. Make the script executable:
   ```bash
   chmod +x gear360_stitcher.py
   ```

#### Step 4: Verify Installation

```bash
python3 -c "import cv2, numpy; print(f'OpenCV: {cv2.__version__}, NumPy: {numpy.__version__}')"
```

---

## Usage

### Quick Start Guide

The app can be used in two ways:

1. **Quick stitch** (using default distortion parameters)
2. **Calibrate + stitch** (for fine-tuned results)

---

### Option 1: Quick Stitch (Recommended for Most Users)

You can stitch videos immediately without calibration using the default distortion coefficients:

**Command (Linux/macOS):**
```bash
./gear360_stitcher.py stitch -i input.mp4 -o output.mp4
```

**Command (Windows):**
```bash
python gear360_stitcher.py stitch -i input.mp4 -o output.mp4
```

**Parameters:**
- `-i, --input`: Input dual fisheye video file
- `-o, --output`: Output panoramic video file
- `-w, --width`: Output width in pixels (default: 3840)
- `-t, --height`: Output height in pixels (default: 1920)
- `--rotate`: Rotate the final panorama by 0, 90, 180, or 270 degrees (default: 0)

**Example Output:**
```
📹 Input Video Info:
   FPS: 29.97
   Total Frames: 1500
   Duration: 50.05s

🎬 Output: 3840x1920 @ 29.97 FPS (0° rotation)

⚙️ Processing video...
┌──────────────────────────────────────────────────┐
│ ████████████████████████████████████████ │ 100.0% │ 1500/1500 │ 12.3 fps │ ETA: 0s 
└──────────────────────────────────────────────────┘

✓ Video processing complete!
  Total time: 122.1s
  Average FPS: 12.3

🔊 Merging audio from original video...
✓ Audio merged successfully
  Output saved to: output.mp4
```

**Note about Audio:**
- If ffmpeg is installed, audio will be automatically preserved
- If ffmpeg is not found, the video will be saved without audio and you'll see a warning
- The stitching process itself is unchanged whether audio is preserved or not

---

### Option 2: Custom Calibration (Optional)

For fine-tuned results, you can create a custom calibration file. This is useful if:
- The default parameters don't work well for your camera
- You want to adjust distortion correction
- You're using a different dual fisheye camera

**Step 1: Calibrate Your Camera**

**Linux/macOS:**
```bash
./gear360_stitcher.py calibrate -i sample_video.mp4 -o calibration.json
```

**Windows:**
```bash
python gear360_stitcher.py calibrate -i sample_video.mp4 -o calibration.json
```

**Parameters:**
- `-i, --input`: Path to a sample video from your Gear 360
- `-o, --output`: Where to save calibration data (default: `calibration.json`)

**Example Output:**
```
🎯 Camera Calibration Tool
============================================================

📐 Video resolution: 3840x1920
✓ Sample frame saved to: calibration_sample.jpg

⚙️ Setting default calibration parameters for Gear 360...

✓ Calibration saved to: calibration.json

💡 Tips:
   - The default distortion coefficients work for most Gear 360 videos
   - If the output appears distorted, try adjusting 'distortion_k1' and 'distortion_k2'
   - Increase k1 (make less negative) if edges are too compressed
   - Decrease k1 (make more negative) if edges are too stretched
```

**Step 2: Stitch Using Your Calibration**

**Linux/macOS:**
```bash
./gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -c calibration.json
```

**Windows:**
```bash
python gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -c calibration.json
```

---

### Common Use Cases

**Custom Resolution:**

Linux/macOS:
```bash
./gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -w 4096 -t 2048
```

Windows:
```bash
python gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -w 4096 -t 2048
```

**Rotation:**
If the stitched video appears sideways, use `--rotate` to correct it.

Linux/macOS:
```bash
./gear360_stitcher.py stitch -i input.mp4 -o output.mp4 --rotate 270
```

Windows:
```bash
python gear360_stitcher.py stitch -i input.mp4 -o output.mp4 --rotate 270
```

**With Custom Calibration:**

Linux/macOS:
```bash
./gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -c my_calibration.json -w 4096 -t 2048
```

Windows:
```bash
python gear360_stitcher.py stitch -i input.mp4 -o output.mp4 -c my_calibration.json -w 4096 -t 2048
```

---

## Command Reference

### View Help

**Linux/macOS:**
```bash
./gear360_stitcher.py --help
./gear360_stitcher.py calibrate --help
./gear360_stitcher.py stitch --help
```

**Windows:**
```bash
python gear360_stitcher.py --help
python gear360_stitcher.py calibrate --help
python gear360_stitcher.py stitch --help
```

### Calibrate Command (Optional)

**Linux/macOS:**
```bash
./gear360_stitcher.py calibrate -i <input.mp4> -o <calibration_file>
```

**Windows:**
```bash
python gear360_stitcher.py calibrate -i <input.mp4> -o <calibration_file>
```

### Stitch Command

**Linux/macOS:**
```bash
./gear360_stitcher.py stitch -i <input.mp4> -o <output.mp4> [-c <calibration_file>] [-w WIDTH] [-t HEIGHT] [--rotate ANGLE]
```

**Windows:**
```bash
python gear360_stitcher.py stitch -i <input.mp4> -o <output.mp4> [-c <calibration_file>] [-w WIDTH] [-t HEIGHT] [--rotate ANGLE]
```

---

## Troubleshooting

### Issue: Audio is not preserved in output video

**Cause:** ffmpeg is not installed or not in system PATH

**Solution:**

**Windows:**
- Install ffmpeg using Chocolatey: `choco install ffmpeg`
- Or download from https://ffmpeg.org/download.html and add to PATH
- Verify installation: `ffmpeg -version`

**Linux:**
- Install via package manager (see Installation section)
- Verify installation: `ffmpeg -version`

**macOS:**
- Install via Homebrew: `brew install ffmpeg`
- Verify installation: `ffmpeg -version`

If you see this message during processing:
```
⚠ Warning: ffmpeg not found. Audio will not be preserved.
  Install ffmpeg to enable audio preservation.
```

Then ffmpeg needs to be installed for audio to work.

### Issue: Output video is sideways or upside-down

The camera's orientation during recording may not match the default projection, causing the final panorama to be incorrectly oriented.

**Solution:**
Use the `--rotate` flag with the `stitch` command to correct the final orientation.
- If people or objects appear sideways, try `--rotate 90` or `--rotate 270`.
- If the video is upside-down, use `--rotate 180`.

**Example (Windows):**
```bash
python gear360_stitcher.py stitch -i input.mp4 -o output.mp4 --rotate 270
```

**Example (Linux/macOS):**
```bash
./gear360_stitcher.py stitch -i input.mp4 -o output.mp4 --rotate 270
```

### Issue: Output appears distorted or warped

The distortion coefficients may need adjustment for your specific camera.

**Solution:**
1. Create a calibration file: 
   - Windows: `python gear360_stitcher.py calibrate -i input.mp4 -o calibration.json`
   - Linux/macOS: `./gear360_stitcher.py calibrate -i input.mp4 -o calibration.json`
2. Open `calibration.json` in a text editor
3. Adjust the distortion parameters:
   - **`distortion_k1`** (default: -0.28): Controls radial distortion
     - Increase (make less negative, e.g., -0.25) if edges are too compressed
     - Decrease (make more negative, e.g., -0.30) if edges are too stretched
   - **`distortion_k2`** (default: 0.05): Fine-tunes distortion correction
4. Save and re-run the stitch command with `-c calibration.json`

**Example calibration.json:**
```json
{
  "camera_model": "Samsung Gear 360",
  "video_resolution": [3840, 1920],
  "distortion_k1": -0.28,
  "distortion_k2": 0.05,
  "notes": "Default distortion coefficients for Gear 360. Adjust if needed."
}
```

### Issue: Black areas or gaps in output

This usually indicates the distortion correction is too aggressive.

**Solution:**
Increase `distortion_k1` (make it less negative) in your calibration file:
- Try values like -0.25, -0.22, -0.20
- Test with a short clip after each adjustment

### Issue: Seam visible between front and back hemispheres

This is normal for basic stitching. The seam should be minimal with correct distortion parameters.

**Solutions:**
1. Ensure you're using appropriate distortion coefficients
2. Try adjusting `distortion_k1` slightly (±0.02)
3. Position subjects away from the seam line when recording

### Issue: "Could not open video file"

**Possible causes:**
- File doesn't exist or path is incorrect
- Video format not supported by OpenCV
- File permissions issue

**Solutions:**
- Verify the file path is correct (use quotes for paths with spaces)
- Try converting video to MP4 format: `ffmpeg -i input.mov -c copy output.mp4`
- Check file permissions

**Windows specific:**
- Use forward slashes or double backslashes in paths: `C:/Videos/input.mp4` or `C:\\Videos\\input.mp4`
- Or use quotes for paths with spaces: `"C:\My Videos\input.mp4"`

### Issue: Slow processing speed

Processing speed depends on your CPU and video resolution.

**Tips to improve speed:**
- Use a lower output resolution (`-w 1920 -t 960` for half resolution)
- Close other applications to free up CPU
- Consider processing shorter clips and concatenating them later

**Expected performance:**
- Modern CPU: 10-20 FPS
- Older CPU: 5-10 FPS

### Issue: Output video won't play

**Solution:**
The default MP4V codec may not be compatible with all players. Re-encode with H.264:

```bash
ffmpeg -i panorama_output.mp4 -c:v libx264 -preset medium -crf 23 final_output.mp4
```

### Issue: Python installation errors on Windows

**Error:** NumPy build failures or "compiler not found"

**Solution:**
Force installation of pre-built binary wheels:
```bash
pip install --only-binary :all: opencv-python numpy
```

Or install specific compatible versions:
```bash
pip install opencv-python numpy==1.26.4
```

---

## Understanding Output Formats

### Equirectangular Projection

The output video uses equirectangular projection, which is the standard format for 360° content. This format:
- Maps the entire sphere onto a rectangular image
- Is compatible with YouTube 360, Facebook 360, VR headsets
- Can be viewed in panorama viewers

### Recommended Resolutions

| Quality | Resolution | Use Case |
|---------|------------|----------|
| Standard | 3840×1920 (4K) | Default, good balance |
| High | 4096×2048 | Better quality, larger file |
| Medium | 2880×1440 | Faster processing |
| Low | 1920×960 | Testing, quick previews |

---

## Tips for Best Results

### 1. Use Good Source Footage
- Ensure your Gear 360 lenses are clean
- Avoid extreme lighting conditions (very bright/dark)
- Keep the camera as still as possible for better stitching

### 2. Test First
- Process a short 10-second clip first to verify stitching quality
- Adjust distortion coefficients if needed before processing long videos
- Check the output in a 360° video player

### 3. Calibration Best Practices
- Most users can skip calibration and use the defaults
- Only create a custom calibration if you notice distortion issues
- Use a video with good lighting and detail for calibration
- Keep the calibration file for future videos from the same camera
- Recalibrate if you notice changes in video quality or if you get a new camera

### 4. Audio Preservation
- Install ffmpeg to automatically preserve audio tracks
- Audio is copied without re-encoding when using ffmpeg's copy codec
- If audio sync issues occur, the source video may have variable frame rate
- The app will notify you if ffmpeg is not available

### 5. Uploading to Platforms
After stitching, your video is ready for:
- **YouTube**: Upload as 360° video (automatically detected)
- **Facebook**: Upload as 360° video
- **VR Players**: Compatible with most 360° video players

---

## Advanced Usage

### Batch Processing Multiple Videos

**Windows (PowerShell):**
```powershell
Get-ChildItem *.mp4 | ForEach-Object {
    $output = "panorama_$($_.Name)"
    python gear360_stitcher.py stitch -i $_.Name -o $output
}
```

**Windows (Command Prompt):**
```batch
for %%f in (*.mp4) do (
    python gear360_stitcher.py stitch -i "%%f" -o "panorama_%%f"
)
```

**Linux/macOS (Bash):**
```bash
#!/bin/bash
for video in *.mp4; do
    output="panorama_${video}"
    ./gear360_stitcher.py stitch -i "$video" -o "$output"
done
```

Or with custom calibration:

**Windows (PowerShell):**
```powershell
Get-ChildItem *.mp4 | ForEach-Object {
    $output = "panorama_$($_.Name)"
    python gear360_stitcher.py stitch -i $_.Name -o $output -c calibration.json
}
```

**Linux/macOS (Bash):**
```bash
#!/bin/bash
for video in *.mp4; do
    output="panorama_${video}"
    ./gear360_stitcher.py stitch -i "$video" -o "$output" -c calibration.json
done
```

### Different Gear 360 Models

This app works with:
- Samsung Gear 360 (2016 model)
- Samsung Gear 360 (2017 model)
- Other dual fisheye cameras (may need distortion coefficient adjustment)

---

## Technical Details

### Processing Pipeline

1. **Frame Extraction**: Video frames read sequentially (streaming)
2. **Frame Splitting**: Each frame split into left/right fisheye views
3. **Distortion Correction**: Each fisheye view corrected using camera matrix and distortion coefficients
4. **Stitching**: Left and right corrected views combined horizontally
5. **Video Encoding**: Output written to video file with same FPS as input
6. **Audio Merging**: Audio track extracted from source and merged with stitched video (requires ffmpeg)

### Audio Handling

The application uses a two-pass approach for audio preservation:
1. **Pass 1**: Stitch video frames to a temporary file (video only)
2. **Pass 2**: Use ffmpeg to merge audio from original video with stitched video
3. The temporary file is automatically deleted after successful audio merge

If ffmpeg is not available:
- The app continues without audio preservation
- A warning message is displayed
- The video-only output is saved to the specified output path

### Distortion Model

The app uses OpenCV's camera calibration model with:
- **Camera Matrix (K)**: Defines the intrinsic camera parameters
- **Distortion Coefficients**: [k1, k2, p1, p2]
  - `k1`, `k2`: Radial distortion coefficients
  - `p1`, `p2`: Tangential distortion coefficients (set to 0 for fisheye)

Default values for Gear 360:
- `k1 = -0.28` (radial distortion)
- `k2 = 0.05` (secondary radial distortion)

### Memory Usage

The app streams frames one at a time, so memory usage is minimal (typically under 500MB) regardless of video length.

### Dependencies

- **OpenCV**: Image processing, video I/O, and lens distortion correction
- **NumPy**: Numerical operations for matrix calculations
- **Python 3**: Core application logic
- **ffmpeg**: Audio extraction and merging (optional but recommended)

---

## FAQ

**Q: Do I need to calibrate before stitching?**  
A: No! The app includes default distortion parameters that work well for most Gear 360 videos. Only calibrate if you notice distortion issues.

**Q: Will audio be preserved from my source video?**  
A: Yes, if ffmpeg is installed. The app automatically detects ffmpeg and preserves audio. Without ffmpeg, only the video will be processed.

**Q: How long does processing take?**  
A: A 5-minute video typically takes 20-40 minutes depending on CPU speed and resolution. The distortion-based approach is significantly faster than older FOV-based methods.

**Q: Can I use this on Windows?**  
A: Yes! The application is fully cross-platform and works on Windows, Linux, and macOS.

**Q: Can I use this with other 360 cameras?**  
A: Yes, if they output dual fisheye video. You'll likely need to create a custom calibration with adjusted distortion coefficients.

**Q: Does this support 3D 360 video?**  
A: No, only 2D 360° panoramic video.

**Q: Why is the output file so large?**  
A: The default MP4V codec doesn't compress well. Re-encode with H.264 (see Troubleshooting).

**Q: Can I preview the output while processing?**  
A: Not currently, but you can cancel anytime (Ctrl+C) and the partial output may be playable.

**Q: What's the difference between distortion coefficients and FOV?**  
A: This version uses camera distortion coefficients (k1, k2) which is more accurate than FOV-based projection. It produces better results and is faster.

**Q: Does the audio merging re-encode the audio?**  
A: The video stream is copied without re-encoding for speed. Audio is encoded to AAC format for broad compatibility.

---

## License

License
This project is licensed under the GNU General Public License v3.0 (GPL-3.0).
This means you are free to:

Use this software for any purpose
Study and modify the source code
Share the software with others
Distribute modified versions

Under the following conditions:

Any modified versions must also be open source under GPL-3.0
You must include the original copyright and license notices
You must state any significant changes made to the software
If you distribute this software, you must make the source code available

For the full license text, see the LICENSE file in this repository or visit:
https://www.gnu.org/licenses/gpl-3.0.en.html

---

## Contributing

Found a bug or want to improve the app? Feel free to modify the source code. Some ideas for enhancements:
- Add GPU acceleration support
- Implement advanced blending for smoother seams
- Support for different output codecs (H.264, HEVC)
- Preview mode for testing parameters
- GUI interface for easier calibration
- Real-time preview during processing

---

## Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all dependencies are installed correctly (including ffmpeg for audio)
3. Test with a short sample video first
4. Try adjusting distortion coefficients if output looks warped
5. Check that your video file is valid and readable

---

**Happy Stitching! 🎥✨**