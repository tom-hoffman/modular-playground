import os
import subprocess
from pathlib import Path
import sys
import re

FILENAMES = ("CIRCU", "CLOCK", "EUCLI", "PLAYE")

def check_root():
    """Ensure the script runs with administrative privileges."""
    if os.geteuid() != 0:
        print("Error: Please run this script with 'sudo'.")
        sys.exit(1)


def find_circuit_playgrounds():
    """Find block device names matching the CIRCUITPY label."""
    try:
        output = subprocess.check_output(
            ["lsblk", "-o", "NAME,LABEL", "-n", "-l"], text=True
        )
        devices = []
        for line in output.strip().split("\n"):
            parts = line.split()
            if len(parts) >= 2 and any(parts[1].upper().startswith(f) for f in FILENAMES):
                devices.append(f"/dev/{parts[0]}")
        return devices
    except subprocess.CalledProcessError:
        print("Error: Failed to query system block devices.")
        return []


def get_mount_point(device):
    """Check if the device is mounted and return the path."""
    try:
        output = subprocess.check_output(
            ["findmnt", "-n", "-o", "TARGET", device], text=True
        )
        return output.strip()
    except subprocess.CalledProcessError:
        return None  # Device is not currently mounted


def unmount_device(device):
    """Safely unmount the device before running fsck."""
    try:
        subprocess.check_call(["umount", device])
        return True
    except subprocess.CalledProcessError:
        return False


def repair_device(device):
    """Run fsck.vfat with automatic repair flags."""
    print(f"Running filesystem check and repair on {device}...")
    try:
        # -a: auto repair, -v: verbose, -w: write to disk immediately
        subprocess.check_call(["fsck.vfat", "-a", "-w", device])
        print(f"Success: {device} repaired successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Warning: fsck returned error code ({e.returncode}) on {device}.")
        return False


def remount_device_as_user(device):
    """Remount the device dynamically as the user who invoked sudo."""
    # Get the username of the person who ran 'sudo'
    username = os.environ.get("SUDO_USER")
    
    if not username:
        print(f"Warning: Could not detect the non-root user. Falling back to root mount.")
        cmd = ['udisksctl', 'mount', '-b', device]
    else:
        print(f"Remounting {device} dynamically as user '{username}'...")
        # 'sudo -u username' drops root privileges to run udisksctl as the standard user
        cmd = ['sudo', '-u', username, 'udisksctl', 'mount', '-b', device]

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        stdout = result.stdout.strip()
        
        # Extract the new user-accessible dynamic path from stdout
        match = re.search(r'at\s+(.+)\b', stdout)
        if match:
            new_path = match.group(1).rstrip('.')
            print(f"Success: {device} is remounted at {new_path}")
            return new_path
            
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to remount {device}: {e.stderr.strip()}")
        return None


def main():
    check_root()
    print("Searching for connected Circuit Playground boards...")

    devices = find_circuit_playgrounds()
    if not devices:
        print("No Circuit Playground boards found.")
        return

    for device in devices:
        print("-" * 50)
        print(f"Found device: {device}")

        # Track if the device was originally mounted
        was_mounted = get_mount_point(device) is not None

        if was_mounted:
            print(f"Device is currently mounted. Unmounting safely for repair...")
            if not unmount_device(device):
                print(f"Failed to unmount {device}. Skipping repair.")
                continue
        else:
            print("Device is not currently mounted.")

        # Perform the filesystem fix
        repair_device(device)

        # Automatically restore mount state dynamically for the user account
        if was_mounted:
            remount_device_as_user(device)

    print("-" * 50)
    print("Process complete.")


if __name__ == "__main__":
    main()

