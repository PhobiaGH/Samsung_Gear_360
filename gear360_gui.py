#!/usr/bin/env python3
"""
Samsung Gear 360 Video Stitcher - Advanced GUI Version
With preview, batch processing, and preset management
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import sys
import json
import cv2
from pathlib import Path
from PIL import Image, ImageTk
import time

# Import the stitcher (assumes gear360_stitcher.py is in the same directory)
try:
    from gear360_stitcher import Gear360Stitcher, calibrate_camera
except ImportError:
    messagebox.showerror("Import Error",
                         "Could not import gear360_stitcher.py\n"
                         "Make sure it's in the same directory as this GUI script.")
    sys.exit(1)


class PresetManager:
    """Manage presets for stitching settings"""

    def __init__(self, preset_file="stitcher_presets.json"):
        self.preset_file = preset_file
        self.presets = self.load_presets()

    def load_presets(self):
        """Load presets from file"""
        try:
            with open(self.preset_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Default presets
            return {
                "4K Standard": {
                    "width": 3840,
                    "height": 1920,
                    "rotation": 0
                },
                "4K Rotated": {
                    "width": 3840,
                    "height": 1920,
                    "rotation": 90
                },
                "HD Standard": {
                    "width": 1920,
                    "height": 960,
                    "rotation": 0
                },
                "8K Ultra": {
                    "width": 7680,
                    "height": 3840,
                    "rotation": 0
                }
            }

    def save_presets(self):
        """Save presets to file"""
        with open(self.preset_file, 'w') as f:
            json.dump(self.presets, f, indent=2)

    def add_preset(self, name, width, height, rotation):
        """Add a new preset"""
        self.presets[name] = {
            "width": width,
            "height": height,
            "rotation": rotation
        }
        self.save_presets()

    def delete_preset(self, name):
        """Delete a preset"""
        if name in self.presets:
            del self.presets[name]
            self.save_presets()

    def get_preset(self, name):
        """Get a preset by name"""
        return self.presets.get(name)


class StitcherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gear 360 Video Stitcher - Advanced")
        self.root.geometry("1000x800")
        self.root.resizable(True, True)

        # Apply dark theme
        self.setup_dark_theme()

        # Queue for thread communication
        self.log_queue = queue.Queue()

        # Processing state
        self.is_processing = False
        self.cancel_requested = False

        # Preset manager
        self.preset_manager = PresetManager()

        # Batch processing list
        self.batch_files = []

        # Preview state
        self.preview_image = None

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Create tabs
        self.create_single_tab()
        self.create_batch_tab()
        self.create_preview_tab()
        self.create_calibration_tab()

        # Start queue checker
        self.check_queue()

    def setup_dark_theme(self):
        """Setup dark theme for the application"""
        # Color scheme
        self.colors = {
            'bg': '#2b2b2b',
            'fg': '#e0e0e0',
            'select_bg': '#404040',
            'select_fg': '#ffffff',
            'button_bg': '#3c3c3c',
            'button_fg': '#e0e0e0',
            'entry_bg': '#1e1e1e',
            'entry_fg': '#e0e0e0',
            'frame_bg': '#2b2b2b',
            'accent': '#0d7377',
            'accent_hover': '#14a085',
            'border': '#404040',
            'text_bg': '#1e1e1e',
            'log_bg': '#1a1a1a',
            'log_fg': '#b0b0b0'
        }

        # Configure root window
        self.root.configure(bg=self.colors['bg'])

        # Create custom style
        style = ttk.Style()

        # Try to use a base theme that works well with dark colors
        try:
            style.theme_use('clam')
        except:
            pass

        # Configure general ttk styles
        style.configure('.',
                        background=self.colors['bg'],
                        foreground=self.colors['fg'],
                        fieldbackground=self.colors['entry_bg'],
                        bordercolor=self.colors['border'],
                        darkcolor=self.colors['bg'],
                        lightcolor=self.colors['bg'])

        # Frame styles
        style.configure('TFrame',
                        background=self.colors['bg'])

        # Label styles
        style.configure('TLabel',
                        background=self.colors['bg'],
                        foreground=self.colors['fg'])

        # Button styles
        style.configure('TButton',
                        background=self.colors['button_bg'],
                        foreground=self.colors['button_fg'],
                        bordercolor=self.colors['border'],
                        focuscolor=self.colors['accent'],
                        relief='flat',
                        padding=6)

        style.map('TButton',
                  background=[('active', self.colors['select_bg']),
                              ('pressed', self.colors['accent'])],
                  foreground=[('active', self.colors['select_fg'])])

        # Accent button style
        style.configure('Accent.TButton',
                        background=self.colors['accent'],
                        foreground='white',
                        relief='flat',
                        padding=6)

        style.map('Accent.TButton',
                  background=[('active', self.colors['accent_hover']),
                              ('pressed', self.colors['accent'])],
                  foreground=[('active', 'white')])

        # Entry styles
        style.configure('TEntry',
                        fieldbackground=self.colors['entry_bg'],
                        foreground=self.colors['entry_fg'],
                        bordercolor=self.colors['border'],
                        insertcolor=self.colors['fg'])

        # Combobox styles
        style.configure('TCombobox',
                        fieldbackground=self.colors['entry_bg'],
                        background=self.colors['button_bg'],
                        foreground=self.colors['entry_fg'],
                        bordercolor=self.colors['border'],
                        arrowcolor=self.colors['fg'],
                        selectbackground=self.colors['select_bg'],
                        selectforeground=self.colors['select_fg'])

        style.map('TCombobox',
                  fieldbackground=[('readonly', self.colors['entry_bg'])],
                  selectbackground=[('readonly', self.colors['select_bg'])],
                  foreground=[('readonly', self.colors['entry_fg'])])

        # Spinbox styles
        style.configure('TSpinbox',
                        fieldbackground=self.colors['entry_bg'],
                        foreground=self.colors['entry_fg'],
                        bordercolor=self.colors['border'],
                        arrowcolor=self.colors['fg'])

        # Notebook styles
        style.configure('TNotebook',
                        background=self.colors['bg'],
                        bordercolor=self.colors['border'])

        style.configure('TNotebook.Tab',
                        background=self.colors['button_bg'],
                        foreground=self.colors['fg'],
                        padding=[20, 8],
                        bordercolor=self.colors['border'])

        style.map('TNotebook.Tab',
                  background=[('selected', self.colors['accent']),
                              ('active', self.colors['select_bg'])],
                  foreground=[('selected', 'white'),
                              ('active', self.colors['select_fg'])],
                  expand=[('selected', [1, 1, 1, 0])])

        # LabelFrame styles
        style.configure('TLabelframe',
                        background=self.colors['bg'],
                        foreground=self.colors['fg'],
                        bordercolor=self.colors['border'],
                        relief='flat')

        style.configure('TLabelframe.Label',
                        background=self.colors['bg'],
                        foreground=self.colors['fg'])

        # Progressbar styles
        style.configure('TProgressbar',
                        background=self.colors['accent'],
                        troughcolor=self.colors['entry_bg'],
                        bordercolor=self.colors['border'],
                        lightcolor=self.colors['accent'],
                        darkcolor=self.colors['accent'])

    def create_single_tab(self):
        """Create single video processing tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="📹 Single Video")

        # Configure grid
        tab.columnconfigure(1, weight=1)

        row = 0

        # === Input File Section ===
        ttk.Label(tab, text="Input Video:", font=('Helvetica', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)

        self.input_path = tk.StringVar()
        ttk.Entry(tab, textvariable=self.input_path, width=50).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(tab, text="Browse...", command=self.browse_input).grid(
            row=row, column=2, padx=5)

        # === Output File Section ===
        row += 1
        ttk.Label(tab, text="Output Video:", font=('Helvetica', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)

        self.output_path = tk.StringVar()
        ttk.Entry(tab, textvariable=self.output_path, width=50).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(tab, text="Browse...", command=self.browse_output).grid(
            row=row, column=2, padx=5)

        # === Calibration File Section ===
        row += 1
        ttk.Label(tab, text="Calibration:", font=('Helvetica', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)

        self.calib_path = tk.StringVar()
        ttk.Entry(tab, textvariable=self.calib_path, width=50).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(tab, text="Browse...", command=self.browse_calibration).grid(
            row=row, column=2, padx=5)

        # === Presets Section ===
        row += 1
        preset_frame = ttk.LabelFrame(tab, text="Presets", padding="10")
        preset_frame.grid(row=row, column=0, columnspan=3,
                          sticky=(tk.W, tk.E), pady=10)

        ttk.Label(preset_frame, text="Load Preset:").grid(
            row=0, column=0, sticky=tk.W, padx=5)
        self.preset_var = tk.StringVar()
        self.preset_combo = ttk.Combobox(preset_frame, textvariable=self.preset_var,
                                         values=list(
                                             self.preset_manager.presets.keys()),
                                         state="readonly", width=20)
        self.preset_combo.grid(row=0, column=1, sticky=tk.W, padx=5)
        self.preset_combo.bind('<<ComboboxSelected>>', self.load_preset)

        ttk.Button(preset_frame, text="Save Current as Preset",
                   command=self.save_preset).grid(row=0, column=2, padx=5)
        ttk.Button(preset_frame, text="Delete Preset",
                   command=self.delete_preset).grid(row=0, column=3, padx=5)

        # === Settings Frame ===
        row += 1
        settings_frame = ttk.LabelFrame(tab, text="Settings", padding="10")
        settings_frame.grid(row=row, column=0, columnspan=3,
                            sticky=(tk.W, tk.E), pady=10)

        # Width
        ttk.Label(settings_frame, text="Output Width:").grid(
            row=0, column=0, sticky=tk.W, pady=5, padx=(0, 5))
        self.width_var = tk.StringVar(value="3840")
        width_spinbox = ttk.Spinbox(settings_frame, from_=1920, to=7680,
                                    increment=320, textvariable=self.width_var, width=10)
        width_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(settings_frame, text="px").grid(row=0, column=2, sticky=tk.W)

        # Height
        ttk.Label(settings_frame, text="Output Height:").grid(
            row=0, column=3, sticky=tk.W, pady=5, padx=(20, 5))
        self.height_var = tk.StringVar(value="1920")
        height_spinbox = ttk.Spinbox(settings_frame, from_=960, to=3840,
                                     increment=160, textvariable=self.height_var, width=10)
        height_spinbox.grid(row=0, column=4, sticky=tk.W, padx=5)
        ttk.Label(settings_frame, text="px").grid(row=0, column=5, sticky=tk.W)

        # Rotation
        ttk.Label(settings_frame, text="Rotation:").grid(
            row=1, column=0, sticky=tk.W, pady=5, padx=(0, 5))
        self.rotation_var = tk.StringVar(value="0")
        rotation_combo = ttk.Combobox(settings_frame, textvariable=self.rotation_var,
                                      values=["0", "90", "180", "270"],
                                      state="readonly", width=8)
        rotation_combo.grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Label(settings_frame, text="degrees").grid(
            row=1, column=2, sticky=tk.W)

        # === Action Buttons ===
        row += 1
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=row, column=0, columnspan=3, pady=15)

        self.stitch_button = ttk.Button(button_frame, text="🎬 Stitch Video",
                                        command=self.start_stitching)
        self.stitch_button.pack(side=tk.LEFT, padx=5)

        ttk.Button(button_frame, text="👁 Generate Preview",
                   command=self.generate_preview).pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="❌ Cancel",
                                        command=self.cancel_processing,
                                        state=tk.DISABLED)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # === Progress Section ===
        row += 1
        progress_frame = ttk.LabelFrame(tab, text="Progress", padding="10")
        progress_frame.grid(row=row, column=0, columnspan=3,
                            sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)

        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        self.status_label = ttk.Label(progress_frame, text="Ready",
                                      font=('Helvetica', 9))
        self.status_label.grid(row=1, column=0, sticky=tk.W)

        # === Log Section ===
        row += 1
        log_frame = ttk.LabelFrame(tab, text="Log", padding="5")
        log_frame.grid(row=row, column=0, columnspan=3,
                       sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        tab.rowconfigure(row, weight=1)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=10, width=70,
                                                  wrap=tk.WORD, state=tk.DISABLED,
                                                  font=('Courier', 9),
                                                  bg=self.colors['log_bg'],
                                                  fg=self.colors['log_fg'],
                                                  insertbackground=self.colors['fg'],
                                                  selectbackground=self.colors['select_bg'],
                                                  selectforeground=self.colors['select_fg'])
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    def create_batch_tab(self):
        """Create batch processing tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="📁 Batch Processing")

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # Instructions
        instructions = ttk.Label(tab,
                                 text="Add multiple videos to process them all with the same settings",
                                 font=('Helvetica', 10))
        instructions.grid(row=0, column=0, columnspan=3, pady=(0, 10))

        # File list frame
        list_frame = ttk.LabelFrame(tab, text="Video Queue", padding="10")
        list_frame.grid(row=1, column=0, columnspan=3,
                        sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.batch_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set,
                                        height=15, font=('Courier', 9),
                                        bg=self.colors['log_bg'],
                                        fg=self.colors['log_fg'],
                                        selectbackground=self.colors['select_bg'],
                                        selectforeground=self.colors['select_fg'],
                                        borderwidth=0,
                                        highlightthickness=1,
                                        highlightbackground=self.colors['border'],
                                        highlightcolor=self.colors['accent'])
        self.batch_listbox.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.config(command=self.batch_listbox.yview)

        # Buttons
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)

        ttk.Button(button_frame, text="➕ Add Videos",
                   command=self.add_batch_videos).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="➖ Remove Selected",
                   command=self.remove_batch_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑 Clear All",
                   command=self.clear_batch_videos).pack(side=tk.LEFT, padx=5)

        # Output directory
        output_frame = ttk.LabelFrame(
            tab, text="Output Settings", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3,
                          sticky=(tk.W, tk.E), pady=10)

        ttk.Label(output_frame, text="Output Directory:").grid(
            row=0, column=0, sticky=tk.W, pady=5)
        self.batch_output_dir = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.batch_output_dir, width=50).grid(
            row=0, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(output_frame, text="Browse...",
                   command=self.browse_batch_output).grid(row=0, column=2, padx=5)

        output_frame.columnconfigure(1, weight=1)

        # Process button
        process_frame = ttk.Frame(tab)
        process_frame.grid(row=4, column=0, columnspan=3, pady=15)

        self.batch_process_button = ttk.Button(process_frame, text="🚀 Process All Videos",
                                               command=self.start_batch_processing)
        self.batch_process_button.pack(side=tk.LEFT, padx=5)

        self.batch_cancel_button = ttk.Button(process_frame, text="❌ Cancel",
                                              command=self.cancel_processing,
                                              state=tk.DISABLED)
        self.batch_cancel_button.pack(side=tk.LEFT, padx=5)

        # Progress
        progress_frame = ttk.LabelFrame(
            tab, text="Batch Progress", padding="10")
        progress_frame.grid(row=5, column=0, columnspan=3,
                            sticky=(tk.W, tk.E), pady=10)
        progress_frame.columnconfigure(0, weight=1)

        self.batch_progress_bar = ttk.Progressbar(
            progress_frame, mode='determinate')
        self.batch_progress_bar.grid(
            row=0, column=0, sticky=(tk.W, tk.E), pady=5)

        self.batch_status_label = ttk.Label(progress_frame, text="Ready",
                                            font=('Helvetica', 9))
        self.batch_status_label.grid(row=1, column=0, sticky=tk.W)

    def create_preview_tab(self):
        """Create preview tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="👁 Preview")

        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

        # Instructions
        instructions = ttk.Label(tab,
                                 text="Preview a single frame before processing the entire video",
                                 font=('Helvetica', 10))
        instructions.grid(row=0, column=0, pady=(0, 10))

        # Preview canvas frame
        canvas_frame = ttk.LabelFrame(tab, text="Preview", padding="10")
        canvas_frame.grid(row=1, column=0, sticky=(
            tk.W, tk.E, tk.N, tk.S), pady=10)
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

        # Canvas with scrollbars
        self.preview_canvas = tk.Canvas(canvas_frame, bg='#1a1a1a', width=800, height=400,
                                        borderwidth=0,
                                        highlightthickness=1,
                                        highlightbackground=self.colors['border'])
        self.preview_canvas.grid(
            row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        h_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL,
                                    command=self.preview_canvas.xview)
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        v_scrollbar = ttk.Scrollbar(canvas_frame, orient=tk.VERTICAL,
                                    command=self.preview_canvas.yview)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        self.preview_canvas.config(xscrollcommand=h_scrollbar.set,
                                   yscrollcommand=v_scrollbar.set)

        # Preview info
        info_frame = ttk.Frame(tab)
        info_frame.grid(row=2, column=0, pady=10)

        self.preview_info_label = ttk.Label(info_frame,
                                            text="Generate a preview from the Single Video tab",
                                            font=('Helvetica', 9))
        self.preview_info_label.pack()

        # Save preview button
        self.save_preview_button = ttk.Button(info_frame, text="💾 Save Preview",
                                              command=self.save_preview,
                                              state=tk.DISABLED)
        self.save_preview_button.pack(pady=10)

    def create_calibration_tab(self):
        """Create advanced calibration tab"""
        tab = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(tab, text="🎯 Calibration")

        # Instructions
        instructions = ttk.Label(tab,
                                 text="Advanced calibration settings for fine-tuning the stitching process",
                                 font=('Helvetica', 10), wraplength=600)
        instructions.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Calibration file section
        row = 1
        ttk.Label(tab, text="Input Video:", font=('Helvetica', 10, 'bold')).grid(
            row=row, column=0, sticky=tk.W, pady=5)

        self.calib_input = tk.StringVar()
        ttk.Entry(tab, textvariable=self.calib_input, width=50).grid(
            row=row, column=1, sticky=(tk.W, tk.E), padx=5)

        ttk.Button(tab, text="Browse...", command=self.browse_calib_input).grid(
            row=row, column=2, padx=5)

        # Distortion coefficients frame
        row += 1
        distortion_frame = ttk.LabelFrame(
            tab, text="Distortion Coefficients", padding="10")
        distortion_frame.grid(row=row, column=0, columnspan=3,
                              sticky=(tk.W, tk.E), pady=20)

        ttk.Label(distortion_frame, text="K1 (radial):").grid(
            row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.k1_var = tk.StringVar(value="-0.28")
        ttk.Entry(distortion_frame, textvariable=self.k1_var, width=15).grid(
            row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(distortion_frame, text="K2 (radial):").grid(
            row=1, column=0, sticky=tk.W, pady=5, padx=5)
        self.k2_var = tk.StringVar(value="0.05")
        ttk.Entry(distortion_frame, textvariable=self.k2_var, width=15).grid(
            row=1, column=1, sticky=tk.W, padx=5)

        ttk.Label(distortion_frame,
                  text="💡 Adjust K1 and K2 if edges appear stretched or compressed",
                  font=('Helvetica', 8)).grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Buttons
        row += 1
        button_frame = ttk.Frame(tab)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)

        ttk.Button(button_frame, text="🎯 Quick Calibrate",
                   command=self.quick_calibrate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="💾 Save Calibration File",
                   command=self.save_calibration_manual).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📂 Load Calibration File",
                   command=self.load_calibration_manual).pack(side=tk.LEFT, padx=5)

        # Info text
        row += 1
        info_frame = ttk.LabelFrame(tab, text="Calibration Tips", padding="10")
        info_frame.grid(row=row, column=0, columnspan=3,
                        sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        tab.rowconfigure(row, weight=1)

        info_text = scrolledtext.ScrolledText(info_frame, height=10, width=70,
                                              wrap=tk.WORD, font=(
                                                  'Helvetica', 9),
                                              bg=self.colors['log_bg'],
                                              fg=self.colors['log_fg'],
                                              insertbackground=self.colors['fg'],
                                              selectbackground=self.colors['select_bg'],
                                              selectforeground=self.colors['select_fg'])
        info_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        info_frame.columnconfigure(0, weight=1)
        info_frame.rowconfigure(0, weight=1)

        tips = """Calibration Tips:

• K1 (Radial Distortion): Controls barrel/pincushion distortion
  - More negative (e.g., -0.35): Reduces edge stretching
  - Less negative (e.g., -0.20): Increases edge coverage
  
• K2 (Secondary Radial): Fine-tunes distortion correction
  - Positive values: Adds slight outward correction
  - Negative values: Adds slight inward correction

• Default values (-0.28, 0.05) work well for most Gear 360 videos

• Test with preview before processing full video

• Save calibration profiles for different camera setups
"""
        info_text.insert(1.0, tips)
        info_text.config(state=tk.DISABLED)

    # === Helper Methods ===

    def browse_input(self):
        """Browse for input video file"""
        filename = filedialog.askopenfilename(
            title="Select Input Video",
            filetypes=[("Video files", "*.mp4 *.mov *.avi"),
                       ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
            if not self.output_path.get():
                input_path = Path(filename)
                output_name = input_path.stem + "_stitched" + input_path.suffix
                output_path = input_path.parent / output_name
                self.output_path.set(str(output_path))

    def browse_output(self):
        """Browse for output video file"""
        filename = filedialog.asksaveasfilename(
            title="Save Output Video As",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)

    def browse_calibration(self):
        """Browse for calibration file"""
        filename = filedialog.askopenfilename(
            title="Select Calibration File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.calib_path.set(filename)

    def browse_calib_input(self):
        """Browse for calibration input video"""
        filename = filedialog.askopenfilename(
            title="Select Input Video for Calibration",
            filetypes=[("Video files", "*.mp4 *.mov *.avi"),
                       ("All files", "*.*")]
        )
        if filename:
            self.calib_input.set(filename)

    def browse_batch_output(self):
        """Browse for batch output directory"""
        dirname = filedialog.askdirectory(title="Select Output Directory")
        if dirname:
            self.batch_output_dir.set(dirname)

    def add_batch_videos(self):
        """Add videos to batch list"""
        filenames = filedialog.askopenfilenames(
            title="Select Videos to Add",
            filetypes=[("Video files", "*.mp4 *.mov *.avi"),
                       ("All files", "*.*")]
        )
        for filename in filenames:
            if filename not in self.batch_files:
                self.batch_files.append(filename)
                self.batch_listbox.insert(tk.END, Path(filename).name)

    def remove_batch_video(self):
        """Remove selected video from batch list"""
        selection = self.batch_listbox.curselection()
        if selection:
            index = selection[0]
            self.batch_listbox.delete(index)
            self.batch_files.pop(index)

    def clear_batch_videos(self):
        """Clear all videos from batch list"""
        self.batch_listbox.delete(0, tk.END)
        self.batch_files.clear()

    def load_preset(self, event=None):
        """Load preset settings"""
        preset_name = self.preset_var.get()
        preset = self.preset_manager.get_preset(preset_name)
        if preset:
            self.width_var.set(str(preset['width']))
            self.height_var.set(str(preset['height']))
            self.rotation_var.set(str(preset['rotation']))
            self.log(f"Loaded preset: {preset_name}")

    def save_preset(self):
        """Save current settings as preset"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Save Preset")
        dialog.geometry("300x120")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Preset Name:").pack(pady=10)
        name_var = tk.StringVar()
        entry = ttk.Entry(dialog, textvariable=name_var, width=30)
        entry.pack(pady=5)
        entry.focus()

        def save():
            name = name_var.get().strip()
            if name:
                try:
                    width = int(self.width_var.get())
                    height = int(self.height_var.get())
                    rotation = int(self.rotation_var.get())
                    self.preset_manager.add_preset(
                        name, width, height, rotation)
                    self.preset_combo['values'] = list(
                        self.preset_manager.presets.keys())
                    self.log(f"Saved preset: {name}")
                    dialog.destroy()
                except ValueError:
                    messagebox.showerror("Error", "Invalid settings")
            else:
                messagebox.showwarning("Warning", "Please enter a preset name")

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Save", command=save).pack(
            side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel",
                   command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def delete_preset(self):
        """Delete selected preset"""
        preset_name = self.preset_var.get()
        if preset_name:
            if messagebox.askyesno("Confirm Delete",
                                   f"Delete preset '{preset_name}'?"):
                self.preset_manager.delete_preset(preset_name)
                self.preset_combo['values'] = list(
                    self.preset_manager.presets.keys())
                self.preset_var.set('')
                self.log(f"Deleted preset: {preset_name}")

    def generate_preview(self):
        """Generate preview of stitched output"""
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input video first")
            return

        if not Path(self.input_path.get()).exists():
            messagebox.showerror("Error", "Input video file does not exist")
            return

        self.log("Generating preview...")
        self.notebook.select(2)  # Switch to preview tab

        thread = threading.Thread(target=self.preview_worker, daemon=True)
        thread.start()

    def preview_worker(self):
        """Worker thread for generating preview"""
        try:
            input_file = self.input_path.get()
            calib_file = self.calib_path.get() if self.calib_path.get() else None
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            rotation = int(self.rotation_var.get())

            # Create stitcher
            stitcher = Gear360Stitcher(calib_file)

            # Open video and get middle frame
            cap = cv2.VideoCapture(input_file)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            mid_frame = total_frames // 2

            cap.set(cv2.CAP_PROP_POS_FRAMES, mid_frame)
            ret, frame = cap.read()
            cap.release()

            if not ret:
                self.log_queue.put(
                    ('error', "Could not read frame from video"))
                return

            # Stitch frame
            panorama = stitcher.stitch_frame(frame, width, height)

            # Rotate if needed
            if rotation == 90:
                panorama = cv2.rotate(panorama, cv2.ROTATE_90_CLOCKWISE)
            elif rotation == 180:
                panorama = cv2.rotate(panorama, cv2.ROTATE_180)
            elif rotation == 270:
                panorama = cv2.rotate(panorama, cv2.ROTATE_90_COUNTERCLOCKWISE)

            # Convert BGR to RGB
            panorama_rgb = cv2.cvtColor(panorama, cv2.COLOR_BGR2RGB)

            # Store for saving later
            self.preview_image = panorama_rgb

            # Convert to PIL Image
            pil_image = Image.fromarray(panorama_rgb)

            # Resize for display if too large
            display_width = 800
            aspect = pil_image.height / pil_image.width
            display_height = int(display_width * aspect)
            pil_image_display = pil_image.resize((display_width, display_height),
                                                 Image.Resampling.LANCZOS)

            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(pil_image_display)

            # Update canvas in main thread
            self.log_queue.put(('preview', (photo, panorama.shape)))

        except Exception as e:
            self.log_queue.put(
                ('error', f"Error generating preview: {str(e)}"))

    def save_preview(self):
        """Save preview image"""
        if self.preview_image is None:
            messagebox.showwarning("Warning", "No preview to save")
            return

        filename = filedialog.asksaveasfilename(
            title="Save Preview Image",
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"),
                       ("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            pil_image = Image.fromarray(self.preview_image)
            pil_image.save(filename)
            self.log(f"Preview saved to: {filename}")
            messagebox.showinfo("Success", "Preview saved successfully!")

    def quick_calibrate(self):
        """Quick calibration process"""
        if not self.calib_input.get():
            messagebox.showerror("Error", "Please select an input video first")
            return

        calib_file = filedialog.asksaveasfilename(
            title="Save Calibration File As",
            defaultextension=".json",
            initialfile="calibration.json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )

        if not calib_file:
            return

        self.is_processing = True
        self.log("Starting calibration...")

        thread = threading.Thread(
            target=self.calibrate_worker,
            args=(self.calib_input.get(), calib_file),
            daemon=True
        )
        thread.start()

    def save_calibration_manual(self):
        """Save manual calibration settings"""
        filename = filedialog.asksaveasfilename(
            title="Save Calibration File",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                k1 = float(self.k1_var.get())
                k2 = float(self.k2_var.get())

                calibration = {
                    "camera_model": "Samsung Gear 360",
                    "distortion_k1": k1,
                    "distortion_k2": k2,
                    "notes": "Manually configured calibration"
                }

                with open(filename, 'w') as f:
                    json.dump(calibration, f, indent=2)

                self.log(f"Calibration saved to: {filename}")
                messagebox.showinfo("Success", "Calibration file saved!")

            except ValueError:
                messagebox.showerror(
                    "Error", "Invalid distortion coefficient values")

    def load_calibration_manual(self):
        """Load calibration file and populate fields"""
        filename = filedialog.askopenfilename(
            title="Load Calibration File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r') as f:
                    calibration = json.load(f)

                self.k1_var.set(str(calibration.get('distortion_k1', -0.28)))
                self.k2_var.set(str(calibration.get('distortion_k2', 0.05)))

                self.log(f"Loaded calibration from: {filename}")
                messagebox.showinfo("Success", "Calibration file loaded!")

            except Exception as e:
                messagebox.showerror(
                    "Error", f"Could not load calibration: {str(e)}")

    def log(self, message):
        """Add message to log"""
        self.log_queue.put(('log', message))

    def update_status(self, message):
        """Update status label"""
        self.log_queue.put(('status', message))

    def check_queue(self):
        """Check for messages from worker thread"""
        try:
            while True:
                item = self.log_queue.get_nowait()

                if isinstance(item, tuple):
                    msg_type = item[0]

                    if msg_type == 'log':
                        message = item[1]
                        self.log_text.config(state=tk.NORMAL)
                        self.log_text.insert(tk.END, message + '\n')
                        self.log_text.see(tk.END)
                        self.log_text.config(state=tk.DISABLED)

                    elif msg_type == 'status':
                        message = item[1]
                        self.status_label.config(text=message)
                        self.batch_status_label.config(text=message)

                    elif msg_type == 'progress':
                        value = item[1]
                        self.progress_bar['value'] = value
                        self.batch_progress_bar['value'] = value

                    elif msg_type == 'preview':
                        photo, shape = item[1]
                        self.preview_canvas.delete("all")
                        self.preview_canvas.create_image(
                            0, 0, anchor=tk.NW, image=photo)
                        self.preview_canvas.image = photo  # Keep reference
                        self.preview_canvas.config(
                            scrollregion=self.preview_canvas.bbox("all"))
                        self.preview_info_label.config(
                            text=f"Preview generated | Resolution: {shape[1]}x{shape[0]}")
                        self.save_preview_button.config(state=tk.NORMAL)
                        self.log("Preview generated successfully!")

                    elif msg_type == 'done':
                        message = item[1]
                        self.processing_complete(message)

                    elif msg_type == 'error':
                        message = item[1]
                        self.processing_error(message)

        except queue.Empty:
            pass

        self.root.after(100, self.check_queue)

    def validate_inputs(self):
        """Validate user inputs"""
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input video file")
            return False

        if not self.output_path.get():
            messagebox.showerror(
                "Error", "Please specify an output video file")
            return False

        if not Path(self.input_path.get()).exists():
            messagebox.showerror("Error", "Input video file does not exist")
            return False

        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            if width <= 0 or height <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror(
                "Error", "Width and height must be positive integers")
            return False

        return True

    def start_stitching(self):
        """Start video stitching in background thread"""
        if not self.validate_inputs():
            return

        self.cancel_requested = False
        self.is_processing = True
        self.stitch_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)

        self.progress_bar.config(mode='determinate', value=0)

        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

        self.log("Starting video stitching...")
        self.update_status("Processing...")

        thread = threading.Thread(target=self.stitch_worker, daemon=True)
        thread.start()

    def stitch_worker(self):
        """Worker thread for stitching"""
        try:
            input_file = self.input_path.get()
            output_file = self.output_path.get()
            calib_file = self.calib_path.get() if self.calib_path.get() else None
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            rotation = int(self.rotation_var.get())

            # Create custom stitcher with progress callback
            stitcher = Gear360Stitcher(calib_file)

            # Monkey-patch the process_video method to report progress
            original_process_video = stitcher.process_video

            def process_video_with_progress(input_path, output_path, pano_width=3840,
                                            pano_height=1920, rotate_angle=0):
                import cv2
                import numpy as np
                import subprocess
                import tempfile
                import os
                from pathlib import Path
                import time

                # Check if ffmpeg is available
                has_ffmpeg = stitcher.check_ffmpeg()
                if not has_ffmpeg:
                    self.log_queue.put(
                        ('log', "⚠ Warning: ffmpeg not found. Audio will not be preserved."))

                # Open input video
                cap = cv2.VideoCapture(input_path)
                if not cap.isOpened():
                    self.log_queue.put(
                        ('log', f"✗ Error: Could not open video file: {input_path}"))
                    raise Exception(f"Could not open video file: {input_path}")

                # Get video properties
                fps = cap.get(cv2.CAP_PROP_FPS)
                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                # Determine final output dimensions based on rotation
                output_w, output_h = pano_width, pano_height
                if rotate_angle in [90, 270]:
                    output_w, output_h = pano_height, pano_width

                self.log_queue.put(('log', f"\n📹 Input Video Info:"))
                self.log_queue.put(('log', f"   FPS: {fps:.2f}"))
                self.log_queue.put(('log', f"   Total Frames: {total_frames}"))
                self.log_queue.put(
                    ('log', f"   Duration: {total_frames/fps:.2f}s"))
                self.log_queue.put(
                    ('log', f"\n🎬 Output: {output_w}x{output_h} @ {fps:.2f} FPS ({rotate_angle}° rotation)"))

                # If ffmpeg is available, use a temporary file for video without audio
                if has_ffmpeg:
                    temp_output = tempfile.NamedTemporaryFile(
                        suffix='.mp4', delete=False).name
                    video_output = temp_output
                else:
                    video_output = output_path

                # Setup video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                out = cv2.VideoWriter(
                    video_output, fourcc, fps, (output_w, output_h))

                if not out.isOpened():
                    self.log_queue.put(
                        ('log', f"✗ Error: Could not create output video: {video_output}"))
                    cap.release()
                    raise Exception(
                        f"Could not create output video: {video_output}")

                # Process frames
                frame_count = 0
                start_time = time.time()
                last_update = start_time

                self.log_queue.put(('log', "\n⚙️ Processing video..."))

                while True:
                    if self.cancel_requested:
                        self.log_queue.put(
                            ('log', "\n⚠ Processing cancelled by user"))
                        break

                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Stitch frame
                    panorama = stitcher.stitch_frame(
                        frame, pano_width, pano_height)

                    # Rotate panorama if requested
                    if rotate_angle == 90:
                        panorama = cv2.rotate(
                            panorama, cv2.ROTATE_90_CLOCKWISE)
                    elif rotate_angle == 180:
                        panorama = cv2.rotate(panorama, cv2.ROTATE_180)
                    elif rotate_angle == 270:
                        panorama = cv2.rotate(
                            panorama, cv2.ROTATE_90_COUNTERCLOCKWISE)

                    out.write(panorama)

                    frame_count += 1

                    # Update progress every 0.5 seconds
                    current_time = time.time()
                    if current_time - last_update >= 0.5 or frame_count == total_frames:
                        progress_percent = (frame_count / total_frames) * 100
                        elapsed = current_time - start_time
                        fps_actual = frame_count / elapsed if elapsed > 0 else 0
                        eta = (total_frames - frame_count) / \
                            fps_actual if fps_actual > 0 else 0

                        # Send progress update to GUI
                        self.log_queue.put(('progress', progress_percent))
                        self.log_queue.put(
                            ('status', f"Processing: {progress_percent:.1f}% | Frame {frame_count}/{total_frames} | {fps_actual:.1f} fps | ETA: {eta:.0f}s"))

                        last_update = current_time

                # Cleanup
                cap.release()
                out.release()

                if self.cancel_requested:
                    # Clean up partial output
                    try:
                        os.unlink(video_output)
                    except:
                        pass
                    return

                total_time = time.time() - start_time
                self.log_queue.put(('log', f"\n✓ Video processing complete!"))
                self.log_queue.put(('log', f"  Total time: {total_time:.1f}s"))
                self.log_queue.put(
                    ('log', f"  Average FPS: {frame_count/total_time:.1f}"))

                # Merge audio if ffmpeg is available
                if has_ffmpeg:
                    self.log_queue.put(
                        ('log', "\n🔊 Merging audio from original video..."))

                    try:
                        # Use ffmpeg to copy video from stitched file and audio from original
                        cmd = [
                            'ffmpeg',
                            '-i', video_output,  # Video source (no audio)
                            '-i', input_path,    # Audio source
                            '-c:v', 'copy',      # Copy video stream without re-encoding
                            '-c:a', 'aac',       # Encode audio as AAC
                            '-map', '0:v:0',     # Map video from first input
                            # Map audio from second input (? means optional)
                            '-map', '1:a:0?',
                            '-shortest',         # Finish encoding when shortest stream ends
                            '-y',                # Overwrite output file
                            output_path
                        ]

                        result = subprocess.run(cmd,
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                text=True)

                        if result.returncode == 0:
                            self.log_queue.put(
                                ('log', "✓ Audio merged successfully"))
                            audio_merged = True
                        else:
                            self.log_queue.put(
                                ('log', "⚠ Warning: Could not merge audio (ffmpeg error)"))
                            self.log_queue.put(
                                ('log', f"  Video saved without audio: {video_output}"))
                            audio_merged = False

                    except Exception as e:
                        self.log_queue.put(
                            ('log', f"⚠ Warning: Error merging audio: {e}"))
                        self.log_queue.put(
                            ('log', f"  Video saved without audio: {video_output}"))
                        audio_merged = False

                    # Clean up temporary file
                    try:
                        os.unlink(video_output)
                    except:
                        pass

                    if audio_merged:
                        self.log_queue.put(
                            ('log', f"  Output saved to: {output_path}"))
                    else:
                        # If audio merge failed, rename temp file to output
                        try:
                            os.rename(video_output, output_path)
                            self.log_queue.put(
                                ('log', f"  Output saved to: {output_path} (without audio)"))
                        except:
                            self.log_queue.put(
                                ('log', f"  Output saved to: {video_output} (without audio)"))
                else:
                    self.log_queue.put(
                        ('log', f"  Output saved to: {output_path} (without audio)"))

            # Use our custom version
            process_video_with_progress(
                input_file, output_file, width, height, rotation)

            if not self.cancel_requested:
                self.log_queue.put(
                    ('done', 'Video stitching completed successfully!'))
            else:
                self.log_queue.put(('done', 'Processing cancelled'))

        except Exception as e:
            self.log_queue.put(('error', f"Error during stitching: {str(e)}"))

    def start_batch_processing(self):
        """Start batch processing"""
        if not self.batch_files:
            messagebox.showerror("Error", "No videos in batch queue")
            return

        if not self.batch_output_dir.get():
            messagebox.showerror("Error", "Please select an output directory")
            return

        if not Path(self.batch_output_dir.get()).exists():
            messagebox.showerror("Error", "Output directory does not exist")
            return

        self.cancel_requested = False
        self.is_processing = True
        self.batch_process_button.config(state=tk.DISABLED)
        self.batch_cancel_button.config(state=tk.NORMAL)

        self.batch_progress_bar.config(mode='determinate', value=0)

        self.log("Starting batch processing...")
        self.update_status(f"Processing 0/{len(self.batch_files)} videos...")

        thread = threading.Thread(target=self.batch_worker, daemon=True)
        thread.start()

    def batch_worker(self):
        """Worker thread for batch processing"""
        import cv2
        import time
        import tempfile
        import os
        import subprocess  # MISSING IMPORT - THIS WAS THE MAIN ISSUE

        try:
            output_dir = Path(self.batch_output_dir.get())
            calib_file = self.calib_path.get() if self.calib_path.get() else None
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            rotation = int(self.rotation_var.get())

            total_videos = len(self.batch_files)
            successful = 0
            failed = 0

            for i, input_file in enumerate(self.batch_files):
                if self.cancel_requested:
                    self.log_queue.put(
                        ('log', "\n⚠ Batch processing cancelled by user"))
                    break

                input_path = Path(input_file)
                output_name = input_path.stem + "_stitched" + input_path.suffix
                output_file = output_dir / output_name

                self.log_queue.put(
                    ('status', f"Processing {i+1}/{total_videos}: {input_path.name}"))
                self.log_queue.put(('log', f"\n{'='*60}"))
                self.log_queue.put(
                    ('log', f"Processing video {i+1}/{total_videos}: {input_path.name}"))
                self.log_queue.put(('log', f"{'='*60}"))

                # Create stitcher
                stitcher = Gear360Stitcher(calib_file)

                # Process video with progress tracking
                try:
                    cap = cv2.VideoCapture(str(input_file))
                    if not cap.isOpened():
                        self.log_queue.put(
                            ('log', f"✗ Error: Could not open {input_path.name}"))
                        failed += 1
                        continue

                    fps = cap.get(cv2.CAP_PROP_FPS)
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                    self.log_queue.put(
                        ('log', f"📹 Video info: {total_frames} frames @ {fps:.2f} fps"))

                    output_w, output_h = width, height
                    if rotation in [90, 270]:
                        output_w, output_h = height, width

                    has_ffmpeg = stitcher.check_ffmpeg()

                    # Use temp file if we'll merge audio later
                    if has_ffmpeg:
                        video_output = tempfile.NamedTemporaryFile(
                            suffix='.mp4', delete=False).name
                    else:
                        video_output = str(output_file)

                    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                    out = cv2.VideoWriter(
                        video_output, fourcc, fps, (output_w, output_h))

                    if not out.isOpened():
                        self.log_queue.put(
                            ('log', f"✗ Error: Could not create output file"))
                        cap.release()
                        failed += 1
                        continue

                    frame_count = 0
                    start_time = time.time()
                    last_log_time = start_time

                    self.log_queue.put(('log', "⚙️ Stitching frames..."))

                    while True:
                        if self.cancel_requested:
                            self.log_queue.put(
                                ('log', "⚠ Processing cancelled"))
                            break

                        ret, frame = cap.read()
                        if not ret:
                            break

                        # Stitch frame
                        panorama = stitcher.stitch_frame(frame, width, height)

                        # Apply rotation
                        if rotation == 90:
                            panorama = cv2.rotate(
                                panorama, cv2.ROTATE_90_CLOCKWISE)
                        elif rotation == 180:
                            panorama = cv2.rotate(panorama, cv2.ROTATE_180)
                        elif rotation == 270:
                            panorama = cv2.rotate(
                                panorama, cv2.ROTATE_90_COUNTERCLOCKWISE)

                        out.write(panorama)
                        frame_count += 1

                        # Update progress
                        current_time = time.time()
                        if current_time - last_log_time >= 0.5 or frame_count == total_frames:
                            video_progress = (frame_count / total_frames) * 100
                            overall_progress = (
                                (i + (frame_count / total_frames)) / total_videos) * 100
                            elapsed = current_time - start_time
                            fps_actual = frame_count / elapsed if elapsed > 0 else 0

                            self.log_queue.put(('progress', overall_progress))
                            self.log_queue.put(('status',
                                                f"Video {i+1}/{total_videos} | {video_progress:.1f}% | "
                                                f"Frame {frame_count}/{total_frames} | {fps_actual:.1f} fps"))

                            last_log_time = current_time

                    cap.release()
                    out.release()

                    if self.cancel_requested:
                        try:
                            os.unlink(video_output)
                        except:
                            pass
                        break

                    total_time = time.time() - start_time
                    self.log_queue.put(
                        ('log', f"✓ Stitching complete ({total_time:.1f}s)"))

                    # Merge audio if ffmpeg is available
                    if has_ffmpeg:
                        self.log_queue.put(('log', "🔊 Merging audio..."))

                        try:
                            cmd = [
                                'ffmpeg',
                                '-i', video_output,
                                '-i', str(input_file),
                                '-c:v', 'copy',
                                '-c:a', 'aac',
                                '-map', '0:v:0',
                                '-map', '1:a:0?',
                                '-shortest',
                                '-y',
                                str(output_file)
                            ]

                            result = subprocess.run(cmd,
                                                    stdout=subprocess.PIPE,
                                                    stderr=subprocess.PIPE,
                                                    text=True)

                            if result.returncode == 0:
                                self.log_queue.put(
                                    ('log', "✓ Audio merged successfully"))
                            else:
                                self.log_queue.put(
                                    ('log', "⚠ Could not merge audio"))
                                # Copy video-only file to output
                                try:
                                    import shutil
                                    shutil.copy2(
                                        video_output, str(output_file))
                                except:
                                    pass

                        except Exception as e:
                            self.log_queue.put(
                                ('log', f"⚠ Audio merge error: {str(e)}"))
                            # Copy video-only file to output
                            try:
                                import shutil
                                shutil.copy2(video_output, str(output_file))
                            except:
                                pass

                        # Clean up temp file
                        try:
                            os.unlink(video_output)
                        except:
                            pass

                    self.log_queue.put(('log', f"✓ Completed: {output_name}"))
                    successful += 1

                except Exception as e:
                    self.log_queue.put(
                        ('log', f"✗ Error processing {input_path.name}: {str(e)}"))
                    failed += 1
                    continue

            # Final summary
            if not self.cancel_requested:
                summary = f'Batch processing complete! Success: {successful}/{total_videos}'
                if failed > 0:
                    summary += f' | Failed: {failed}'
                self.log_queue.put(('done', summary))
            else:
                self.log_queue.put(
                    ('done', f'Batch processing cancelled. Completed: {successful}/{total_videos}'))

        except Exception as e:
            self.log_queue.put(
                ('error', f"Error during batch processing: {str(e)}"))

    def calibrate_worker(self, input_file, calib_file):
        """Worker thread for calibration"""
        try:
            import cv2
            import json

            self.log_queue.put(('log', "\n🎯 Camera Calibration Tool"))
            self.log_queue.put(('log', "=" * 60))

            cap = cv2.VideoCapture(input_file)
            if not cap.isOpened():
                self.log_queue.put(
                    ('error', f"Could not open video: {input_file}"))
                return

            # Read first frame
            ret, frame = cap.read()
            cap.release()

            if not ret:
                self.log_queue.put(
                    ('error', "Could not read frame from video"))
                return

            h, w = frame.shape[:2]
            self.log_queue.put(('log', f"\n📏 Video resolution: {w}x{h}"))

            # Save sample frame for reference
            sample_path = "calibration_sample.jpg"
            cv2.imwrite(sample_path, frame)
            self.log_queue.put(
                ('log', f"✓ Sample frame saved to: {sample_path}"))

            # Basic calibration parameters
            self.log_queue.put(
                ('log', "\n⚙️ Setting default calibration parameters for Gear 360..."))

            calibration = {
                "camera_model": "Samsung Gear 360",
                "video_resolution": [w, h],
                "distortion_k1": -0.28,
                "distortion_k2": 0.05,
                "notes": "Default distortion coefficients for Gear 360. Adjust if needed."
            }

            # Save calibration
            with open(calib_file, 'w') as f:
                json.dump(calibration, f, indent=2)

            self.log_queue.put(
                ('log', f"\n✓ Calibration saved to: {calib_file}"))
            self.log_queue.put(('log', "\n💡 Tips:"))
            self.log_queue.put(
                ('log', "   - The default distortion coefficients work for most Gear 360 videos"))
            self.log_queue.put(
                ('log', "   - If the output appears distorted, try adjusting 'distortion_k1' and 'distortion_k2'"))
            self.log_queue.put(
                ('log', "   - Increase k1 (make less negative) if edges are too compressed"))
            self.log_queue.put(
                ('log', "   - Decrease k1 (make more negative) if edges are too stretched"))

            self.log_queue.put(('done', f'Calibration saved to: {calib_file}'))

        except Exception as e:
            self.log_queue.put(
                ('error', f"Error during calibration: {str(e)}"))

    def cancel_processing(self):
        """Cancel current processing"""
        self.cancel_requested = True
        self.log("Cancel requested...")

    def processing_complete(self, message):
        """Called when processing completes"""
        self.is_processing = False
        self.cancel_requested = False

        self.progress_bar['value'] = 100
        self.batch_progress_bar['value'] = 100

        self.stitch_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.batch_process_button.config(state=tk.NORMAL)
        self.batch_cancel_button.config(state=tk.DISABLED)

        self.update_status(message)
        self.log(f"\n✓ {message}")

        messagebox.showinfo("Complete", message)

    def processing_error(self, message):
        """Called when processing errors"""
        self.is_processing = False
        self.cancel_requested = False

        self.progress_bar['value'] = 0
        self.batch_progress_bar['value'] = 0

        self.stitch_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.batch_process_button.config(state=tk.NORMAL)
        self.batch_cancel_button.config(state=tk.DISABLED)

        self.update_status("Error occurred")
        self.log(f"\n✗ {message}")

        messagebox.showerror("Error", message)


def main():
    root = tk.Tk()
    app = StitcherGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
