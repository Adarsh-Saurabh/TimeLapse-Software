# Timelapse Capture Tool

## Description
This project is a timelapse capture tool that allows you to take images from a webcam at fixed intervals and convert those images into a video. The application features a graphical user interface built using `Tkinter` and is packaged into an executable using `cx_Freeze`.

## Dependencies
This project requires the following Python packages:

- `cx_Freeze`: To create standalone executables from Python scripts.
- `Pillow`: For image processing tasks.
- `Tkinter`: For creating the graphical user interface (comes pre-installed with Python).
- `OpenCV`: For handling video capture and image processing.

You can install the necessary dependencies using `pip`:

```bash
pip install cx_Freeze Pillow opencv-python
```

## Setup Instructions

1. **Set Up Your Environment**:
   - Create a virtual environment (optional but recommended):

     ```bash
     python -m venv venv
     ```

   - Activate the virtual environment:
     - **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - **macOS/Linux**:
       ```bash
       source venv/bin/activate
       ```

2. **Install Dependencies**:
   - Install the required packages using `pip`:

     ```bash
     pip install cx_Freeze Pillow opencv-python
     ```

3. **Prepare Your Project**:
   - Make sure you have your main script (`timelapse.py`) and any other required files (e.g., icons) in the project directory.

4. **Create `execute.py`**:
   - Use the provided `execute.py` script to configure the build process. Ensure that the script includes the necessary options and paths.

5. **Build the Executable**:
   - Run the `execute.py` script to build the executable:

     ```bash
     python execute.py build
     ```

   - This will generate the executable in the `build` directory.

## Additional Information

- **Icon File**: Ensure that the icon file (e.g., `your_icon.ico`) is available in the same directory as `setup.py` or specify the correct path in the `setup.py` script.
- **UPX Compression**: For reducing the size of the executable, you can use UPX compression. Ensure UPX is installed and configured properly.

## Troubleshooting

- **UPX Not Found**: Ensure UPX is installed and its path is included in your system’s PATH environment variable.
- **Execution Errors**: Check for any missing dependencies or configuration issues if you encounter errors while running the executable.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
