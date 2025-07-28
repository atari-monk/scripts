#!/usr/bin/env python3
from __future__ import annotations

import random
import sys
from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, Tuple

import typer

app = typer.Typer(add_completion=False, rich_markup_mode="markdown")


class Direction(Enum):
    NORTH = auto()
    EAST = auto()
    SOUTH = auto()
    WEST = auto()


class ItemType(Enum):
    KEY = "rusty key"
    SWORD = "shiny sword"
    POTION = "health potion"
    TORCH = "flickering torch"


class EnemyType(Enum):
    GOBLIN = "goblin"
    ORC = "orc"
    SPIDER = "giant spider"
    DRAGON = "ancient dragon"


class RoomType(Enum):
    CAVE = "damp cave"
    HALL = "grand hall"
    KITCHEN = "abandoned kitchen"
    GARDEN = "overgrown garden"
    DUNGEON = "dark dungeon"
    TREASURE = "treasure room"


@dataclass
class Item:
    item_type: ItemType
    description: str


@dataclass
class Enemy:
    enemy_type: EnemyType
    health: int
    damage: int


@dataclass
class Room:
    room_type: RoomType
    description: str
    items: List[Item]
    enemy: Optional[Enemy]
    exits: List[Direction]


@dataclass
class Player:
    health: int
    inventory: List[Item]
    current_room: Room
    all_rooms: List[Room]


class GameState(Enum):
    PLAYING = auto()
    WON = auto()
    LOST = auto()
    QUIT = auto()


def generate_dungeon() -> Tuple[List[Room], Room]:
    rooms: List[Room] = []

    for room_type in RoomType:
        items: List[Item] = []
        enemy = None
        
        if random.random() > 0.6:
            item_type = random.choice(list(ItemType))
            items.append(Item(item_type, f"A {item_type.value} lies here."))
            
        if random.random() > 0.7:
            enemy_type = random.choice(list(EnemyType))
            health = random.randint(10, 50)
            damage = random.randint(5, 15)
            enemy = Enemy(enemy_type, health, damage)
            
        exits = random.sample(list(Direction), k=random.randint(1, 3))
        room = Room(
            room_type=room_type,
            description=f"You are in a {room_type.value}. It looks mysterious.",
            items=items,
            enemy=enemy,
            exits=exits
        )
        rooms.append(room)

    for room in rooms:
        room.exits = random.sample(list(Direction), k=random.randint(1, 3))

    return rooms, rooms[0]


def describe_room(room: Room) -> None:  # Changed return type to None (prints directly)
    typer.secho(room.description, bold=True)
    
    if room.items:
        typer.secho("\nItems here:", fg="green")
        for item in room.items:
            typer.echo(f"- {item.description}")
            
    if room.enemy:
        typer.secho(
            f"\nDanger! A {room.enemy.enemy_type.value} "
            f"({room.enemy.health} HP) lurks here!",
            fg="red"
        )
        
    typer.secho("\nExits:", fg="blue", nl=False)
    typer.echo(" " + ", ".join(exit.name.lower() for exit in room.exits))


def handle_command(player: Player, command: str) -> GameState:
    command = command.strip().lower()
    
    if command in ("q", "quit"):
        return GameState.QUIT
        
    if command in ("n", "north"):
        return move_player(player, Direction.NORTH)
    if command in ("e", "east"):
        return move_player(player, Direction.EAST)
    if command in ("s", "south"):
        return move_player(player, Direction.SOUTH)
    if command in ("w", "west"):
        return move_player(player, Direction.WEST)
        
    if command.startswith("take "):
        return take_item(player, command[5:])
        
    if command.startswith("use "):
        return use_item(player, command[4:])
        
    if command == "attack":
        return attack_enemy(player)
        
    if command in ("i", "inventory"):
        show_inventory(player)
        return GameState.PLAYING
        
    typer.echo("Unknown command. Try 'north', 'take item', 'attack', or 'inventory'.")
    return GameState.PLAYING


def move_player(player: Player, direction: Direction) -> GameState:
    if direction not in player.current_room.exits:
        typer.secho("You can't go that way!", fg="red")
        return GameState.PLAYING
        
    all_rooms = player.all_rooms
    possible_rooms = [room for room in all_rooms if room != player.current_room]
    if not possible_rooms:
        typer.secho("There are no other rooms to move to!", fg="red")
        return GameState.PLAYING
        
    new_room = random.choice(possible_rooms)
    player.current_room = new_room
    describe_room(player.current_room)  # Direct print
    
    if player.current_room.room_type == RoomType.TREASURE:
        typer.secho("\nYou found the treasure! You win!", fg="yellow", bold=True)
        return GameState.WON
        
    return GameState.PLAYING


def take_item(player: Player, item_name: str) -> GameState:
    for item in list(player.current_room.items):
        if item_name in item.item_type.value:
            player.inventory.append(item)
            player.current_room.items.remove(item)
            typer.echo(f"You took the {item.item_type.value}.")
            return GameState.PLAYING
            
    typer.echo(f"There is no {item_name} here.")
    return GameState.PLAYING


def use_item(player: Player, item_name: str) -> GameState:
    for item in player.inventory:
        if item_name in item.item_type.value:
            if item.item_type == ItemType.POTION:
                player.health += 20
                player.inventory.remove(item)
                typer.echo("You drank the potion and gained 20 health!")
                return GameState.PLAYING
            typer.echo(f"You can't use the {item.item_type.value} right now.")
            return GameState.PLAYING
            
    typer.echo(f"You don't have a {item_name}.")
    return GameState.PLAYING


def attack_enemy(player: Player) -> GameState:
    if not player.current_room.enemy:
        typer.secho("There's nothing to attack here!", fg="red")
        return GameState.PLAYING
        
    enemy = player.current_room.enemy
    has_sword = any(item.item_type == ItemType.SWORD for item in player.inventory)
    
    damage = random.randint(10, 20) if has_sword else random.randint(5, 10)
    enemy.health -= damage
    
    typer.secho(
        f"You attack the {enemy.enemy_type.value} "
        f"for {damage} damage! ({enemy.health} HP remaining)",
        fg="cyan"
    )
    
    if enemy.health <= 0:
        typer.secho(f"You defeated the {enemy.enemy_type.value}!", fg="green", bold=True)
        player.current_room.enemy = None
        return GameState.PLAYING
        
    player.health -= enemy.damage
    typer.secho(
        f"The {enemy.enemy_type.value} attacks you "
        f"for {enemy.damage} damage! ({player.health} HP remaining)",
        fg="red"
    )
    
    if player.health <= 0:
        typer.secho("\nYou have been defeated! Game over.", fg="red", bold=True)
        return GameState.LOST
        
    return GameState.PLAYING


def show_inventory(player: Player) -> None:
    if not player.inventory:
        typer.secho("Your inventory is empty.", fg="yellow")
        return
        
    typer.secho("Inventory:", bold=True)
    for item in player.inventory:
        typer.secho(f"- {item.item_type.value}: {item.description}", fg="cyan")
    typer.secho(f"\nHealth: {player.health}", fg="green")


def show_help() -> None:
    typer.secho("\nCommands:", bold=True)
    typer.secho("- Movement: north/n, east/e, south/s, west/w", fg="green")
    typer.secho("- Items: take <item>, use <item>, inventory/i", fg="green")
    typer.secho("- Combat: attack", fg="green")
    typer.secho("- Other: quit/q, help", fg="green")
    typer.secho("\nExplore the dungeon and find the treasure room to win!", bold=True)


def run_game() -> None:
    typer.secho("Welcome to Dungeon Adventure!", bold=True)
    typer.secho("Type 'help' for commands or 'quit' to exit.\n")
    
    rooms, starting_room = generate_dungeon()
    player = Player(
        health=100,
        inventory=[],
        current_room=starting_room,
        all_rooms=rooms
    )
    
    describe_room(player.current_room)  # Now prints directly
    
    game_state = GameState.PLAYING
    while game_state == GameState.PLAYING:
        try:
            command = typer.prompt("What will you do?").strip().lower()
            
            if command in ("h", "help"):
                show_help()
                continue
            game_state = handle_command(player, command)
        except (EOFError, KeyboardInterrupt):
            game_state = GameState.QUIT
            
    if game_state == GameState.QUIT:
        typer.secho("\nThanks for playing!", bold=True)
    sys.exit(0)


@app.command()
def play() -> None:
    """Start the text adventure game."""
    run_game()


def main() -> None:
    """Entry point for the CLI application."""
    app()


if __name__ == "__main__":
    main()