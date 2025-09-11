#!/usr/bin/env python3
"""
PSTimer Build Script
Create standalone executables for distribution.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def check_requirements():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller

        print("✓ PyInstaller found")
        return True
    except ImportError:
        print("❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False


def create_icon():
    """Create platform-specific icon files."""
    logo_png = Path("logo.png")
    if not logo_png.exists():
        print("❌ logo.png not found")
        return False

    system = platform.system().lower()

    try:
        if system == "windows":
            # Try to create ICO file
            try:
                from PIL import Image

                img = Image.open(logo_png)
                ico_path = Path("logo.ico")
                img.save(
                    ico_path,
                    format="ICO",
                    sizes=[
                        (16, 16),
                        (32, 32),
                        (48, 48),
                        (64, 64),
                        (128, 128),
                        (256, 256),
                    ],
                )
                print(f"✓ Created {ico_path}")
                return str(ico_path)
            except ImportError:
                print("ℹ️ Pillow not available, using PNG as icon")
                return str(logo_png)
        else:
            print(f"ℹ️ Using PNG icon for {system}")
            return str(logo_png)
    except Exception as e:
        print(f"⚠️ Icon creation warning: {e}")
        return str(logo_png)


def build_executable():
    """Build the executable using PyInstaller."""
    system = platform.system().lower()
    icon_file = create_icon()

    # Base command
    cmd = ["pyinstaller", "--onefile", "--name", "PSTimer", "main.py"]

    # Add windowed flag for GUI apps (no console)
    if system in ["windows", "darwin"]:
        cmd.insert(2, "--windowed")

    # Add icon if available
    if icon_file and Path(icon_file).exists():
        cmd.extend(["--icon", icon_file])

    # Add additional data files
    cmd.extend(
        [
            "--add-data",
            f"src{os.pathsep}src",
            "--add-data",
            f"logo.png{os.pathsep}.",
        ]
    )

    print(f"🔨 Building executable for {system}...")
    print(f"Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✓ Build successful!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def create_distribution():
    """Create distribution package."""
    system = platform.system().lower()
    dist_dir = Path("dist")

    if not dist_dir.exists():
        print("❌ dist directory not found. Build may have failed.")
        return False

    # Create distribution folder
    version = "1.0"  # You can make this dynamic
    package_name = f"PSTimer-v{version}-{system.title()}"
    package_dir = Path(package_name)

    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()

    # Copy executable
    exe_name = "PSTimer.exe" if system == "windows" else "PSTimer"
    exe_path = dist_dir / exe_name

    if exe_path.exists():
        shutil.copy2(exe_path, package_dir)
        print(f"✓ Copied {exe_name}")
    else:
        print(f"❌ Executable {exe_name} not found")
        return False

    # Copy additional files
    files_to_copy = [
        "logo.png",
        "USER_README.md",
        "LICENSE" if Path("LICENSE").exists() else None,
    ]

    for file_name in files_to_copy:
        if file_name and Path(file_name).exists():
            shutil.copy2(file_name, package_dir)
            print(f"✓ Copied {file_name}")

    # Create README for package
    package_readme = package_dir / "README.txt"
    with open(package_readme, "w") as f:
        f.write(
            f"""PSTimer v{version}
Professional Speedcubing Timer

To run PSTimer:
- Windows: Double-click PSTimer.exe
- macOS: Double-click PSTimer.app (if available)
- Linux: Run ./PSTimer in terminal

For detailed instructions, see USER_README.md

Visit: https://github.com/plinsy/pstimer
"""
        )

    # Create ZIP package
    try:
        shutil.make_archive(package_name, "zip", ".", package_name)
        print(f"✓ Created {package_name}.zip")
    except Exception as e:
        print(f"⚠️ ZIP creation warning: {e}")

    print(f"\n🎉 Distribution package created: {package_name}/")
    return True


def main():
    """Main build process."""
    print("PSTimer Build Script")
    print("===================")

    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Run this script from the PSTimer root directory.")
        sys.exit(1)

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Clean previous builds
    for dir_name in ["build", "dist", "__pycache__"]:
        if Path(dir_name).exists():
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}")

    # Build executable
    if not build_executable():
        sys.exit(1)

    # Create distribution package
    if not create_distribution():
        sys.exit(1)

    print("\n✅ Build complete!")
    print("📁 Check the generated folder and ZIP file for distribution.")


if __name__ == "__main__":
    main()
