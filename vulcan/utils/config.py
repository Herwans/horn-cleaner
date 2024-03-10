import json
import pathlib


class Configuration:
    cliConfig = None

    def __init__(self):
        path = None
        default_path = pathlib.Path(f"{pathlib.Path.home()}/.vulcan/config.json")
        root_path = pathlib.Path("config.json")
        if default_path.exists() and default_path.is_file():
            path = default_path
        elif root_path.exists() and root_path.is_file():
            path = "config.json"

        if path is not None:
            with open(path, 'r') as f:
                data = json.load(f)
                self.cliConfig = data["cli"]
        else:
            Exception("No rules found")

    def get_folder_rules(self):
        return self.cliConfig['folder-rules']

    def get_file_rules(self):
        return self.cliConfig['file-rules']

    def get_extension_sets(self):
        return self.cliConfig['extension-set']

    def get_image_extensions(self):
        return self.cliConfig["extensions"]["images"]

    def get_videos_extensions(self):
        return self.cliConfig["extensions"]["videos"]

    def get_delete_pattern(self):
        return self.cliConfig["to_delete"]

