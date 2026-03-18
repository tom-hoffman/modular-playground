#!/usr/bin/env python3
"""Clean, maintainable main loop for mpy-cross compilation utility."""

import argparse
from pathlib import Path
import subprocess
import shutil
import os
import time

EXCLUDED = {"make.py"}  # Skip these filenames (e.g., bootstrap scripts)
IGNORED = {"config.py"}  # Never process these files
PY_EXT = ".py"


def is_file_to_process(filename: str, root_path: Path) -> bool:
    """Decide if a file should be processed in the main loop."""
    # Skip excluded filenames immediately
    if filename in EXCLUDED or filename not.endswith(PY_EXT):
        return False
    # Never process ignored files (even with proper extensions)
    if filename in IGNORED:
        return False
    
    # Check timestamp logic only when remote exists AND is newer
    remote_path = root_path / f"{filename[:-len(PY_EXT)]}m{PY_EXT}"  # Output suffix "m"
    if remote_path.exists() and os.path.getmtime(root_path) < os.path.getmtime(remote_path):
        return False  # Skip: already up-to-date
    
    return True


def process_file(filename: str, mpy_cross_exe: Path, root_path: Path) -> None:
    """Process a single file with compilation + fallback copy logic."""
    local = Path(filename)
    remote = root_path / f"{filename[:-len(PY_EXT)]}m{PY_EXT}"  # Output suffix "m"
    
    print(f"[{filename}] Processing...")
    
    try:
        # Try compiling first (only if compilation is feasible)
        subprocess.run(
            [str(mpy_cross_exe), str(local)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False  # Never crash on compile errors
        )
        shutil.move(str(remote.name), str(remote))  # Move compiled output to final location
        print(f"  ✓ Compiled & moved: {remote}")
    
    except FileNotFoundError as e:
        # Compilation failed silently or file doesn't exist → fallback copy
        print(f"  ! Compilation failed ({e}), copying directly...")
        shutil.copyfile(str(remote.name), str(remote))
        print(f"  ✗ Fallback copied: {remote}")
    
    except Exception as e:
        # Catch all other errors (e.g., permission issues) → fallback copy
        print(f"  ? Unexpected error ({e}), copying directly...")
        shutil.copyfile(str(remote.name), str(remote))


def main():
    """Main entry point with clean linear flow."""
    parser = argparse.ArgumentParser(description="Compile Python files with mpy-cross.")
    parser.add_argument("mpy_cross_path", help="Path to mpy-cross compiler executable.")
    parser.add_argument("remote_root_path", help="Root directory for output files.")
    
    args = parser.parse_args()
    root_path = Path(args.remote_root_path)
    mpy_cross_exe = Path(args.mpy_cross_path).resolve()  # Resolve symlinks
    
    if not root_path.is_dir():
        raise FileNotFoundError(f"Output root does not exist: {root_path}")
    if not mpy_cross_exe.is_file():
        raise FileNotFoundError(f"Compiler missing: {mpy_cross_exe}")
    
    print("Scanning directory...")
    for filename in os.listdir("."):  # Only process files in current dir (not subdirs)
        # Skip directories and non-.py files early
        if not Path(filename).is_file():
            continue
        
        # Decide whether to process this file (skip/ignore logic here)
        should_process = is_file_to_process(filename, root_path)
        
        # Only proceed with processing if needed
        if should_process:
            process_file(filename, mpy_cross_exe, root_path)
    
    print("Processing complete!")


if __name__ == "__main__":
    main()
