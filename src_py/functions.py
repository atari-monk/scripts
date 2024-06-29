import os

def print_project_structure(folder_path, output_file, exclude_folders=None, printContent=False, description=None, printStructure=True):
    if exclude_folders is None:
        exclude_folders = []

    with open(output_file, 'w') as f:
        if description:
            f.write(f'{description}\n\n')
        if printStructure:
            for root, dirs, files in os.walk(folder_path):
                dirs[:] = [d for d in dirs if d not in exclude_folders]
                f.write(f'{root}\n')
                for file in files:
                    if printContent:
                        f.write(f'{file}:\n')
                        with open(os.path.join(root, file), 'r') as infile:
                            contents = infile.read()
                            f.write(f'{contents}\n')
                    else:
                        f.write(f'\t{file}\n')
                for directory in dirs:
                    f.write(f'\t{directory}/\n')
        elif printContent:
            for root, _, files in os.walk(folder_path):
                for file in files:
                    with open(os.path.join(root, file), 'r') as infile:
                        contents = infile.read()
                        f.write(f'{file}:\n{contents}\n')

def generate_project_structure(configurations):
    exclude_folders = configurations.get("exclude_folders", [])
    for file_config in configurations.get("files", []):
        description = file_config["description"]
        isOn = file_config["isOn"]
        printStructure = file_config["printStructure"]
        printContent = file_config["printContent"]
        input_folder = file_config["input_folder"]
        output_file = file_config["output_file"]

        if not isOn: continue
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        print_project_structure(input_folder, output_file, exclude_folders, printContent, description, printStructure)
