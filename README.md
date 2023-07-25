
# Horn cleaner

Small tools to clean file and folder name

## Run Locally

```bash
# Clone the project
git clone https://link-to-project
# Go to the project directory
cd my-project

python3 -m venv .venv

# Enable .venv
## Windows
.venv\scripts\activate

##Linux
. .venv/bin/activate

# In order to run the application, use pip to generate it
pip install --editable .

# Run the application
cleaner
```

## Build

```bash
python setup.py sdist bdist_wheel
```

## Manually deploy
```bash
pip install horn-cleaner.whl
```

## Authors

- [@Herwans](https://www.github.com/Herwans)
