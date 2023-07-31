
# Horn cleaner

Small tools to clean file and folder name

## Run Locally

```bash
# Clone the project
git clone https://github.com/Herwans/horn_cleaner

# Go to the project directory
cd horn_cleaner

# Create a virtual environment for the application
# Avoid version conflict with others applications
## Windows
python -m venv .venv
## Linux
python3 -m venv .venv

# Enable .venv
## Windows
.venv\scripts\activate
##Linux
. .venv/bin/activate

# In order to run the application, use pip to generate it
pip install --editable .
```

## Build

```bash
# Generate the version
python setup.py sdist bdist_wheel
# Install it
pip install <file>.whl
```

## Usage example
```bash
# Apply the name cleaning and delete the empty folders
hcleaner rename <folder> --apply --delete
```

## Authors

- [@Herwans](https://www.github.com/Herwans)
