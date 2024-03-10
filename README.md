
# Vulcan

A small utility to clean file and folder name, and some additional features.

## Run Locally
### On Windows
```bash
# Clone the project
git clone https://github.com/Herwans/vulcan

# Go to the project directory
cd vulcan

# Create a virtual environment for the application
python -m venv venv

# Enable .venv
.venv\Scripts\activate

# In order to run the application, use pip to generate it
pip install --editable .
```

### On Linux/MacOS
```bash
# Clone the project
git clone https://github.com/Herwans/vulcan

# Go to the project directory
cd vulcan

# Create a virtual environment for the application
# Avoid version conflict with others applications
python3 -m venv .venv

# Enable .venv
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

## How to use it
1. Copy config.json.sample to `~/.vulcan/config.json`
2. Fill the configuration fields :
   * **folder-rules** : contains the rules apply to folders. Format : `[ "regex", "replacement value" ]` 
   * **file-rules** : contains the rules apply to files. Format : `[ "regex", "replacement value", "extension-set name|*", "exclusion when *" ]`
   * **extension-sets** : group of extensions, regardless the files type, use for file's rules application. Format : `"set-name": ["ext1", "ext2", "ext3"]`
   * **extensions** : indicate the extension manage for images or videos. Format `"images": ["jpg", "jpeg","png", "gif", "webp"]`


```json
{
    "cli": {
        "folder-rules": [
            ["(((\\(([^)]+)\\))|\\s|(\\[([^]]+)\\])|(\\{([^}]+)\\}))*)$",""],
            ["^(((\\(([^)]+)\\))|\\s|(\\[([^]]+)\\])|(\\{([^}]+)\\}))*)",""]
        ],
        "file-rules": [
            ["(((\\(([^)]+)\\))|\\s|(\\[([^]]+)\\])|(\\{([^}]+)\\}))*)$","", "*", "zip,rar,7zip"],
            ["^(((\\(([^)]+)\\))|\\s|(\\[([^]]+)\\])|(\\{([^}]+)\\}))*)","", "*", "zip,rar,7zip"]
        ],
        "extension-set": {
            "set-1": ["jpeg", "mkv", "py"],
            "set-2": ["jpg", "jpeg", "png", "pptx"]
        },
        "extensions": {
            "images": ["jpg", "jpeg","png", "gif", "webp"],
            "videos": ["mp4", "avi", "mpeg", "mkv"]
        }
    }
}
```

## Usage example
```bash
# Apply the name cleaning and delete the empty folders
vulcan rename <folder> --delete

# Check the integrity of images from folder's subfolders
vulcan integrity <folder> -s
```

## Authors

- [@Herwans](https://www.github.com/Herwans)
