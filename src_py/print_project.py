import json
from functions import generate_project_structure

def main():
    with open('C:/atari-monk/code/scripts/data/print_project.json', 'r') as file:
        configurations = json.load(file)

    generate_project_structure(configurations)

if __name__ == "__main__":
    main()
