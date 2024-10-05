import os
import sys
import argparse
import subprocess


def get_site_packages(conda_env_path):
    """Get the site-packages path for a given conda environment on Windows."""
    lib_folder = os.path.join(conda_env_path, "Lib")
    if not os.path.isdir(lib_folder):
        raise ValueError(f"Invalid conda environment path: {conda_env_path}")

    site_packages = os.path.join(lib_folder, "site-packages")
    if not os.path.exists(site_packages):
        raise ValueError(
            "Unable to locate site-packages in the given conda environment."
        )
    return site_packages


def replace_with_junction(site_packages_path, target_dir):
    """Replace the package in site-packages with a junction to the target directory."""
    package_name = os.path.basename(target_dir.rstrip("\\"))
    package_path = os.path.join(site_packages_path, package_name)

    if not os.path.exists(target_dir):
        raise ValueError(f"Target directory does not exist: {target_dir}")

    # Remove existing package if present
    if os.path.exists(package_path):
        print(f"Removing existing package: {package_path}")
        if os.path.islink(package_path) or os.path.isdir(package_path):
            subprocess.run(
                ["rmdir", "/S", "/Q", package_path], shell=True, check=True
            )
        else:
            raise ValueError(
                f"Cannot remove {package_path}. It is not a directory or symlink."
            )

    # Create a junction instead
    print(f"Creating a junction from {package_path} to {target_dir}")
    junction_cmd = f'mklink /J "{package_path}" "{target_dir}"'
    result = subprocess.run(junction_cmd, shell=True, capture_output=True)

    if result.returncode != 0:
        print(f"Error creating junction: {result.stderr.decode().strip()}")
        sys.exit(1)
    else:
        print(f"Junction created successfully: {package_path} -> {target_dir}")


def main():
    parser = argparse.ArgumentParser(
        description="Replace a package in the current conda environment with a junction to the given directory."
    )
    parser.add_argument(
        "target_dir",
        type=str,
        help="Directory to link the package to (e.g., C:\\Users\\user\\repos\\myutil).",
    )

    args = parser.parse_args()

    # Automatically detect the conda environment path
    conda_env_path = sys.prefix

    # Get the site-packages directory in the conda environment
    try:
        site_packages_path = get_site_packages(conda_env_path)
        print(f"Site-packages found at: {site_packages_path}")

        # Replace the package with a junction
        replace_with_junction(site_packages_path, args.target_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
