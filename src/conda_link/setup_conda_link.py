# setup_conda_link.py
import os
import sys
import shutil
import subprocess


def check_conda_environment():
    """Check if the script is running inside a conda environment."""
    return os.environ.get("CONDA_PREFIX") is not None


def get_conda_environment_path():
    """Get the path of the currently active conda environment."""
    return os.environ.get("CONDA_PREFIX")


def copy_files(conda_env_path):
    """Copy the conda_link.py and create a batch file in the Scripts folder of the conda environment."""
    scripts_path = os.path.join(conda_env_path, "Scripts")

    # Copy the main Python script
    source_script = "conda_link.py"  # Ensure this script is in the same directory as setup script
    target_script = os.path.join(scripts_path, "conda_link.py")
    shutil.copyfile(source_script, target_script)
    print(f"Copied {source_script} to {target_script}")

    # Create a batch wrapper (conda_link.bat)
    batch_file_content = "@echo off\n" f'python "%~dp0\\conda_link.py" %*\n'
    batch_file_path = os.path.join(scripts_path, "conda_link.bat")
    with open(batch_file_path, "w") as batch_file:
        batch_file.write(batch_file_content)

    print(
        f"Created batch file at {batch_file_path} to wrap conda link command."
    )


def main():
    if not check_conda_environment():
        print(
            "Error: This script must be run inside an activated conda environment."
        )
        sys.exit(1)

    conda_env_path = get_conda_environment_path()
    print(f"Detected conda environment: {conda_env_path}")

    # Copy files and create the batch wrapper
    copy_files(conda_env_path)

    print("Installation completed successfully!")
    print("You can now use the command: conda link <path-to-directory>")


if __name__ == "__main__":
    main()
