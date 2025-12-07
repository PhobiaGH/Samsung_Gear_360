#!/usr/bin/env python3
"""

                .                 .  .       .                                         .            
                                                                          ..                        
                                                              .   .                                 
                 ..                     ....      .                                .     .          
         ..   . .=%%+.       .    .    .-%%@.      .           .                                    
                .@@-+@@-.          ...#@%:@@=          .          .    .                            
                .@@#.:@@@=        .:%@@+.-@@*.                      .           .        .          
                :@@@:..%@@@=+#:++##@@@:..+@@*.   .               . .                               .
     .          .@@@#:..%@@@@@@@@@@@@-..##@@+.                                     .   .          . 
   .            .#@@#...%@@@@@@@@@@@@-..:@@@.                            .        .                 
            .    .@@-..-@@@@@@@@@@@@@*..:%@-     .                                             .    
     .            =@@@@@@@@@@@@@@@@@@@@@@@#.   .                   .  .                             
                .=@@@@@@@@@@@@@@@@@@@@@@@@@#.           .                                           
               .#%@@@@@%-::##@@@#@---*@@@@@@#-               .                     .                
          .   .*@@@@@@@@@#=*#@@@@++*@@@@@@@@@%.     .                .  .              .            
              .+@@*:....:+@@@@@@@@@*:....:=@@#..            .         .  .                         .
              :@+-+...    .#@@@@@@:  .. ..==:@+   . .   .      .            .                       
     .        -:+@@@+-..+*:.@%##@:.+*:.:=*@@%.-                          . .        .         .     
      ..      .-*+@%%@@@@:+:.%@@-.=.#@@@@%@%-#                    .            .                    
               ..*..*@@=...:%%@@%-...-@@@@==..       .                                            . 
        .          .@@*=. .        ..*=@@@%:                       .        .           ..          
                  =@@@@+.       .    -@@@@@@@:             .                         ...  .      .  
.                ..%@@@#+.         .*:@@@@@@@@=..                                    .     .   .    
              .   ==#@@#=.      . ..%*@@@@@@@@@#.     .                                             
                  .:@@@@%.     . ..=@@@@@@@@@@@@@=.                                             .   
                   -@@@@%..    .+@=@@@@@@@@@@@@@@@@=..                  .       .        .          
                   .@@@@@+-. ..%@@@@@@@@@@@@@@@@@@@@@*..                                            
             .  .  .+%@@@@#.  =@@@@@@@@@@@@@@@@@@@@@@@@%..   .          .                 .         
    .        .      .=@+@@@. .%@@@@@@@@@@@@@@@@@@@@@@@@@@%.                                         
     .              ..%:@@@= .%-@@@@@@@@@@@@@@@@@@@@@@@@@@@#.          .                            
      .               ..-@#*-.:.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@.. .    . .                 .          
                         -@--:  =@@@@@@@@%@@@@@@@@@@@@@@@@@@@@-..                          .      ..
                          ...    .@@@@@@@=@@@@@@@@@@@@@@@@@@@@@-.                                   
            .             .*#+-. .+@@@@@@=-@@@@@@@@@@@@@@@@@@@@@:                                   
                          .-@@@%.#-@@@@@%...=@@@@:.-++::#@@@@@@@@.          .       .        .      
             .  .         .:@@@@@*=@@@@@: .+@@*.%@@@@@@@@%*@@@@@@*.       .                         
               .           .@@@@*..@@@@%=  .%=+@@@@@@@@@@@@@@@@@@%.     ..-**#=. .  .               
  .     .           .      .@@@@% .@@@@#.  ..:@@@@@@@@@@@@@@@@@@@@:. .-%@@@@@@@@@@@@@*=..     .  .  
                           .@@@@+ .@@@@-:+. .%@@@@@@@@@@@@@@@@@@@@*.=@@@@@@@@@@@@@@@@@%*=.          
                          .:@@@@. :@@@#-@@@:.%@@@@@@@@@@@@@@@@@@@@@%@@@@@@@@@@@@@@@@@@@@@=.         
                 .        .*@@@@=.+@@@@:@@@@.%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@##@@@@@@@@@@@%..       
        .          .      .@@@@@..#@@@@.+@@@-*@@@@@@@@@@@@@@@@@#=--=*%@@@#=:.*@@@@@@@@@@@@@@.       
            .            .#@@@#. .@@@@...%@@#.%@@@@@@@@@@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@=       
           .             :@@@@%. -@@@@.. .*@@#.@@@@@@@@@@+:..  .-*@@@@@@@@@@@@@@@@@@@@@@@@@%*       
 .    .               .:+%@@@+--+@@@@*..=#%@#-..-#@@@@@-   .    .-@@@@@@@@@@@@@@@@@@@@@@@@@:-   .   
        .        .   .*@@@@@@-*@@@@@@- =%%@--@@@@@@@@@@+.      .=+--#@@@@@@@@@@@@@@@@@@@@@@.  .     
                     :%#@@@@*:%@@@@@=.    ..+%%@@%%%@*.         .:%@@@@@@@@@@@@@@@@@@@@@@@*   .     
                                   .              .@*. .  ..      ..=@@@@@@@@@@@@@@@@@@@@@.         
                                                 .*%.-#@@@#+......=#@@@@@@@@@@@@@@@@@*#@+..         
                                                 .#@=..   ..-*%#+--+@@@@@@@@@@@@@@@#::+..           
        .                                   . .  ....          ..-+*#%%%%*+-+@@@#-...               
                          .. .                              . .           .:...          .          
      .      .                                      .  .                            .        .      
                                                              . .        .       .              .   
                               .        .     . . ..                                      .    .    

Samsung Gear 360 Video Stitcher
Converts dual fisheye video into equirectangular panorama
"""

import cv2
import numpy as np
import argparse
import json
import sys
import subprocess
import tempfile
import os
from pathlib import Path
from typing import Tuple, Optional, Dict
import time


class Gear360Stitcher:
    """Handles stitching of dual fisheye video from Samsung Gear 360"""
    
    def __init__(self, calibration_file: Optional[str] = None):
        self.calibration_data = None
        self.distortion_k1 = -0.28
        self.distortion_k2 = 0.05
        
        if calibration_file:
            self.load_calibration(calibration_file)
            if self.calibration_data:
                self.distortion_k1 = self.calibration_data.get('distortion_k1', -0.28)
                self.distortion_k2 = self.calibration_data.get('distortion_k2', 0.05)
                print(f"✓ Using distortion coefficients: K1={self.distortion_k1}, K2={self.distortion_k2}")
    
    def load_calibration(self, filepath: str) -> None:
        """Load calibration data from JSON file"""
        abs_filepath = Path(filepath).resolve()
        try:
            with open(abs_filepath, 'r') as f:
                self.calibration_data = json.load(f)
            print(f"✓ Loaded calibration data from {abs_filepath}")
        except FileNotFoundError:
            print(f"⚠ Calibration file not found: {abs_filepath}, using defaults")
            self.calibration_data = None
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON in calibration file: {abs_filepath}")
            sys.exit(1)
    
    def save_calibration(self, filepath: str, data: Dict) -> None:
        """Save calibration data to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"✓ Calibration data saved to {filepath}")
    
    def split_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """Split frame into left and right fisheye views"""
        h, w = frame.shape[:2]
        
        # Check if frame is wider than tall (horizontal split) or taller than wide (vertical split)
        if w > h:
            # Horizontal split (side by side)
            mid = w // 2
            left = frame[:, :mid]
            right = frame[:, mid:]
        else:
            # Vertical split (top and bottom)
            mid = h // 2
            left = frame[:mid, :]
            right = frame[mid:, :]
        
        return left, right
    
    def defish(self, img: np.ndarray, out_w: int, out_h: int) -> np.ndarray:
        """
        Convert fisheye image to rectilinear projection using camera matrix and distortion
        
        Args:
            img: Input fisheye image
            out_w: Output width
            out_h: Output height
        """
        w, h = img.shape[1], img.shape[0]
        
        # Camera intrinsic matrix
        K = np.array([[w/2, 0, w/2],
                      [0, w/2, h/2],
                      [0,   0,   1]], dtype=np.float32)
        
        # Distortion coefficients [k1, k2, p1, p2]
        D = np.array([self.distortion_k1, self.distortion_k2, 0, 0], dtype=np.float32)
        
        # Initialize undistortion maps
        map1, map2 = cv2.initUndistortRectifyMap(K, D, None, K, (out_w, out_h), cv2.CV_32FC1)
        
        # Remap the image
        return cv2.remap(img, map1, map2, cv2.INTER_LINEAR)
    
    def stitch_frame(self, frame: np.ndarray, pano_width: int = 3840, 
                    pano_height: int = 1920) -> np.ndarray:
        """Stitch a single frame from dual fisheye to panorama"""
        left, right = self.split_frame(frame)
        
        # Each hemisphere takes half the panorama width
        half_width = pano_width // 2
        
        # Defish both lenses
        left_eq = self.defish(left, out_w=half_width, out_h=pano_height)
        right_eq = self.defish(right, out_w=half_width, out_h=pano_height)
        
        # Stitch horizontally
        panorama = np.hstack([left_eq, right_eq])
        
        return panorama
    
    def check_ffmpeg(self) -> bool:
        """Check if ffmpeg is available"""
        try:
            subprocess.run(['ffmpeg', '-version'], 
                         stdout=subprocess.DEVNULL, 
                         stderr=subprocess.DEVNULL,
                         check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def merge_audio(self, video_no_audio: str, original_video: str, output_video: str) -> bool:
        """
        Merge audio from original video into the stitched video using ffmpeg
        
        Args:
            video_no_audio: Path to stitched video without audio
            original_video: Path to original video with audio
            output_video: Path for final output with audio
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print("\n🔊 Merging audio from original video...")
            
            # Use ffmpeg to copy video from stitched file and audio from original
            cmd = [
                'ffmpeg',
                '-i', video_no_audio,  # Video source (no audio)
                '-i', original_video,   # Audio source
                '-c:v', 'copy',         # Copy video stream without re-encoding
                '-c:a', 'aac',          # Encode audio as AAC
                '-map', '0:v:0',        # Map video from first input
                '-map', '1:a:0?',       # Map audio from second input (? means optional)
                '-shortest',            # Finish encoding when shortest stream ends
                '-y',                   # Overwrite output file
                output_video
            ]
            
            result = subprocess.run(cmd, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE,
                                  text=True)
            
            if result.returncode == 0:
                print("✓ Audio merged successfully")
                return True
            else:
                print(f"⚠ Warning: Could not merge audio (ffmpeg error)")
                print(f"  Video saved without audio: {video_no_audio}")
                return False
                
        except Exception as e:
            print(f"⚠ Warning: Error merging audio: {e}")
            print(f"  Video saved without audio: {video_no_audio}")
            return False
    
    def process_video(self, input_path: str, output_path: str, 
                     pano_width: int = 3840, pano_height: int = 1920,
                     rotate_angle: int = 0) -> None:
        """
        Process entire video file
        
        Args:
            input_path: Path to input dual fisheye video
            output_path: Path for output panoramic video
            pano_width: Width of stitched panorama (before rotation)
            pano_height: Height of stitched panorama (before rotation)
            rotate_angle: Angle to rotate the final panorama (0, 90, 180, 270)
        """
        # Check if ffmpeg is available
        has_ffmpeg = self.check_ffmpeg()
        if not has_ffmpeg:
            print("⚠ Warning: ffmpeg not found. Audio will not be preserved.")
            print("  Install ffmpeg to enable audio preservation.")
        
        # Open input video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            print(f"✗ Error: Could not open video file: {input_path}")
            sys.exit(1)
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Determine final output dimensions based on rotation
        output_w, output_h = pano_width, pano_height
        if rotate_angle in [90, 270]:
            output_w, output_h = pano_height, pano_width
            
        print(f"\n📹 Input Video Info:")
        print(f"   FPS: {fps:.2f}")
        print(f"   Total Frames: {total_frames}")
        print(f"   Duration: {total_frames/fps:.2f}s")
        print(f"\n🎬 Output: {output_w}x{output_h} @ {fps:.2f} FPS "
              f"({rotate_angle}° rotation)")
        
        # If ffmpeg is available, use a temporary file for video without audio
        if has_ffmpeg:
            temp_output = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False).name
            video_output = temp_output
        else:
            video_output = output_path
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_output, fourcc, fps, (output_w, output_h))
        
        if not out.isOpened():
            print(f"✗ Error: Could not create output video: {video_output}")
            cap.release()
            sys.exit(1)
        
        # Process frames
        frame_count = 0
        start_time = time.time()
        last_update = start_time
        
        print("\n⚙️ Processing video...")
        print("┌" + "─" * 50 + "┐")
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Stitch frame
            panorama = self.stitch_frame(frame, pano_width, pano_height)
            
            # Rotate panorama if requested
            if rotate_angle == 90:
                panorama = cv2.rotate(panorama, cv2.ROTATE_90_CLOCKWISE)
            elif rotate_angle == 180:
                panorama = cv2.rotate(panorama, cv2.ROTATE_180)
            elif rotate_angle == 270:
                panorama = cv2.rotate(panorama, cv2.ROTATE_90_COUNTERCLOCKWISE)

            out.write(panorama)
            
            frame_count += 1
            
            # Update progress every 0.5 seconds
            current_time = time.time()
            if current_time - last_update >= 0.5 or frame_count == total_frames:
                progress = (frame_count / total_frames) * 100
                elapsed = current_time - start_time
                fps_actual = frame_count / elapsed if elapsed > 0 else 0
                eta = (total_frames - frame_count) / fps_actual if fps_actual > 0 else 0
                
                # Progress bar
                bar_length = 40
                filled = int(bar_length * frame_count / total_frames)
                bar = "█" * filled + "░" * (bar_length - filled)
                
                print(f"\r│ {bar} │ {progress:5.1f}% │ {frame_count}/{total_frames} │ "
                      f"{fps_actual:.1f} fps │ ETA: {eta:.0f}s ", end='', flush=True)
                
                last_update = current_time
        
        print("\n└" + "─" * 50 + "┘")
        
        # Cleanup
        cap.release()
        out.release()
        
        total_time = time.time() - start_time
        print(f"\n✓ Video processing complete!")
        print(f"  Total time: {total_time:.1f}s")
        print(f"  Average FPS: {frame_count/total_time:.1f}")
        
        # Merge audio if ffmpeg is available
        if has_ffmpeg:
            audio_merged = self.merge_audio(video_output, input_path, output_path)
            
            # Clean up temporary file
            try:
                os.unlink(video_output)
            except:
                pass
            
            if audio_merged:
                print(f"  Output saved to: {output_path}")
            else:
                # If audio merge failed, rename temp file to output
                try:
                    os.rename(video_output, output_path)
                    print(f"  Output saved to: {output_path} (without audio)")
                except:
                    print(f"  Output saved to: {video_output} (without audio)")
        else:
            print(f"  Output saved to: {output_path} (without audio)")


def calibrate_camera(video_path: str, output_file: str) -> None:
    """
    Interactive calibration tool for Gear 360
    
    This is a simplified calibration that extracts a sample frame
    and allows user to set basic parameters.
    """
    print("\n🎯 Camera Calibration Tool")
    print("=" * 60)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"✗ Error: Could not open video: {video_path}")
        sys.exit(1)
    
    # Read first frame
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("✗ Error: Could not read frame from video")
        sys.exit(1)
    
    h, w = frame.shape[:2]
    print(f"\n📐 Video resolution: {w}x{h}")
    
    # Save sample frame for reference
    sample_path = "calibration_sample.jpg"
    cv2.imwrite(sample_path, frame)
    print(f"✓ Sample frame saved to: {sample_path}")
    
    # Basic calibration parameters
    print("\n⚙️ Setting default calibration parameters for Gear 360...")
    
    calibration = {
        "camera_model": "Samsung Gear 360",
        "video_resolution": [w, h],
        "distortion_k1": -0.28,
        "distortion_k2": 0.05,
        "notes": "Default distortion coefficients for Gear 360. Adjust if needed."
    }
    
    # Save calibration
    with open(output_file, 'w') as f:
        json.dump(calibration, f, indent=2)
    
    print(f"\n✓ Calibration saved to: {output_file}")
    print("\n💡 Tips:")
    print("   - The default distortion coefficients work for most Gear 360 videos")
    print("   - If the output appears distorted, try adjusting 'distortion_k1' and 'distortion_k2'")
    print("   - Increase k1 (make less negative) if edges are too compressed")
    print("   - Decrease k1 (make more negative) if edges are too stretched")


def main():
    parser = argparse.ArgumentParser(
        description="Samsung Gear 360 Video Stitcher - Convert dual fisheye to panorama",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # First, calibrate your camera (optional)
  %(prog)s calibrate -i input.mp4 -o calibration.json
  
  # Then stitch video using calibration
  %(prog)s stitch -i input.mp4 -o output.mp4 -c calibration.json
  
  # Stitch without calibration (uses defaults)
  %(prog)s stitch -i input.mp4 -o output.mp4
  
  # Custom output resolution
  %(prog)s stitch -i input.mp4 -o output.mp4 -w 4096 -t 2048

  # Rotate the final panorama by 90 degrees clockwise
  %(prog)s stitch -i input.mp4 -o output.mp4 --rotate 90

Note: Audio preservation requires ffmpeg to be installed.
      Install with: 'pip install ffmpeg-python' or download from ffmpeg.org
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Calibration command
    calib_parser = subparsers.add_parser('calibrate', help='Calibrate camera')
    calib_parser.add_argument('-i', '--input', required=True, help='Input video file')
    calib_parser.add_argument('-o', '--output', default='calibration.json',
                             help='Output calibration file (default: calibration.json)')
    
    # Stitching command
    stitch_parser = subparsers.add_parser('stitch', help='Stitch video to panorama')
    stitch_parser.add_argument('-i', '--input', required=True, help='Input video file')
    stitch_parser.add_argument('-o', '--output', required=True, help='Output video file')
    stitch_parser.add_argument('-c', '--calibration', default=None,
                              help='Calibration file (optional)')
    stitch_parser.add_argument('-w', '--width', type=int, default=3840,
                              help='Output width in pixels (default: 3840)')
    stitch_parser.add_argument('-t', '--height', type=int, default=1920,
                              help='Output height in pixels (default: 1920)')
    stitch_parser.add_argument('--rotate', type=int, default=0, choices=[0, 90, 180, 270],
                              help='Rotate the final panorama (default: 0)')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    # Execute command
    if args.command == 'calibrate':
        calibrate_camera(args.input, args.output)
    
    elif args.command == 'stitch':
        stitcher = Gear360Stitcher(args.calibration)
        stitcher.process_video(args.input, args.output, args.width, args.height,
                               rotate_angle=args.rotate)


if __name__ == "__main__":
    main()


# Special thanks to a certain kitty who wished to remain un-named, for contributing her math skills to this project.

#   /\_/\
#  ( o.o )
#   > ^ 
#  /|   |\
# (_|   |_)