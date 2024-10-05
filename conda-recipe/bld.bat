:: Ensure that we are in the correct directory (where meta.yaml is located)
:: Navigate to the source directory if necessary.

:: Use pip to install the package into the conda environment
"%PYTHON%" -m pip install . --no-deps --ignore-installed -vv