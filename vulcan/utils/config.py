import json
import pathlib


class Configuration:
    cliConfig = None

    def __init__(self):
        path = self.get_config_file()
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                self.cliConfig = data["cli"]
        except Exception:
            raise Exception("Unable to read the configuration file. Please check it.")

        if self.cliConfig is None:
            raise Exception("Error while parsing the configuration. Please check the configuration file.")

    @staticmethod
    def get_config_file():
        path = None
        default_path = pathlib.Path(f"{pathlib.Path.home()}/.vulcan/config.json")
        root_path = pathlib.Path("config.json")
        if default_path.exists() and default_path.is_file():
            path = default_path
        elif root_path.exists() and root_path.is_file():
            path = "config.json"

        if path is None:
            raise Exception("No configuration file found.")
        return path

    def get_folder_rules(self):
        rules = self.cliConfig['folder-rules']
        if len(rules) > 0:
            for rule in rules:
                if len(rule) != 2:
                    raise Exception("Folder's rules invalid. Check that you define the pattern and the replacement.")
        return rules

    def get_file_rules(self):
        rules = self.cliConfig['file-rules']
        if len(rules) > 0:
            for rule in rules:
                if len(rule) < 3:
                    raise Exception("File's rules invalid. Check that you define at least the pattern, "
                                    "the replacement and the extension set.")
        return rules

    def get_extension_sets(self):
        return self.cliConfig['extension-set']

    def get_image_extensions(self):
        return self.cliConfig["extensions"]["images"]

    def get_videos_extensions(self):
        return self.cliConfig["extensions"]["videos"]

    def get_delete_pattern(self):
        return self.cliConfig["to_delete"]
