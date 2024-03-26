import json

def load_positions(file_path):
    with open(file_path, 'r') as file:
        positions = json.load(file)
    return {pos['id']: (pos['x'], pos['y']) for pos in positions}

def load_mouse_commands(file_path):
    with open(file_path, 'r') as file:
        mouse_commands = json.load(file)
    return mouse_commands

def join_positions_to_commands(mouse_commands, positions):
    for command in mouse_commands:
        if 'positionId' in command:
            position_id = command['positionId']
            if position_id in positions:
                position = positions[position_id]
                command['x'], command['y'] = position
    return mouse_commands
