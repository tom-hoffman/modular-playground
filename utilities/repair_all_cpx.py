import os
import subprocess
import sys


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
            if len(parts) >= 2 and "CIRCUITPY" in parts[1].upper():
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
        subprocess.check_call(["fsck.vfat", "-a", "-v", "-w", device])
        print(f"Success: {device} repaired successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Warning: fsck returned error code ({e.returncode}) on {device}.")
        return False


def remount_device(device, mount_point):
    """Remount the device back to its original mount point."""
    print(f"Remounting {device} back to {mount_point}...")
    try:
        # Re-mount with normal read/write privileges
        subprocess.check_call(["mount", device, mount_point])
        print(f"Success: {device} is remounted.")
    except subprocess.CalledProcessError:
        print(f"Error: Failed to remount {device} to {mount_point}.")


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

        # Track the original mount location
        original_mount = get_mount_point(device)

        if original_mount:
            print(f"Device is mounted at {original_mount}. Unmounting safely...")
            if not unmount_device(device):
                print(f"Failed to unmount {device}. Skipping repair.")
                continue
        else:
            print("Device is not currently mounted.")

        # Perform the filesystem fix
        repair_device(device)

        # Automatically restore the mount state if it was originally mounted
        if original_mount:
            remount_device(device, original_mount)

    print("-" * 50)
    print("Process complete.")


if __name__ == "__main__":
    main()
