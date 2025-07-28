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


def describe_room(room: Room) -> str:
    description = [f"\n[bold]{room.description}[/bold]"]
    
    if room.items:
        description.append("\n[green]Items here:[/green]")
        description.extend(f"- {item.description}" for item in room.items)
        
    if room.enemy:
        description.append(
            f"\n[red]Danger! A {room.enemy.enemy_type.value} "
            f"({room.enemy.health} HP) lurks here![/red]"
        )
        
    description.append("\n[blue]Exits:[/blue] " + ", ".join(
        exit.name.lower() for exit in room.exits
    ))
    
    return "\n".join(description)


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
        typer.echo("You can't go that way!")
        return GameState.PLAYING
        
    all_rooms = player.all_rooms
    possible_rooms = [room for room in all_rooms if room != player.current_room]
    if not possible_rooms:
        typer.echo("There are no other rooms to move to!")
        return GameState.PLAYING
    new_room = random.choice(possible_rooms)
    player.current_room = new_room
    typer.echo(describe_room(player.current_room))
    
    if player.current_room.room_type == RoomType.TREASURE:
        typer.echo("\n[bold yellow]You found the treasure! You win![/bold yellow]")
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
        typer.echo("There's nothing to attack here!")
        return GameState.PLAYING
        
    enemy = player.current_room.enemy
    has_sword = any(item.item_type == ItemType.SWORD for item in player.inventory)
    
    damage = random.randint(10, 20) if has_sword else random.randint(5, 10)
    enemy.health -= damage
    
    typer.echo(
        f"You attack the {enemy.enemy_type.value} "
        f"for {damage} damage! ({enemy.health} HP remaining)"
    )
    
    if enemy.health <= 0:
        typer.echo(f"You defeated the {enemy.enemy_type.value}!")
        player.current_room.enemy = None
        return GameState.PLAYING
        
    player.health -= enemy.damage
    typer.echo(
        f"The {enemy.enemy_type.value} attacks you "
        f"for {enemy.damage} damage! ({player.health} HP remaining)"
    )
    
    if player.health <= 0:
        typer.echo("\n[bold red]You have been defeated! Game over.[/bold red]")
        return GameState.LOST
        
    return GameState.PLAYING


def show_inventory(player: Player) -> None:
    if not player.inventory:
        typer.echo("Your inventory is empty.")
        return
        
    typer.echo("[bold]Inventory:[/bold]")
    for item in player.inventory:
        typer.echo(f"- {item.item_type.value}: {item.description}")
    typer.echo(f"\nHealth: {player.health}")


def show_help() -> None:
    typer.echo("\n[bold]Commands:[/bold]")
    typer.echo("- [green]Movement[/green]: north/n, east/e, south/s, west/w")
    typer.echo("- [green]Items[/green]: take <item>, use <item>, inventory/i")
    typer.echo("- [green]Combat[/green]: attack")
    typer.echo("- [green]Other[/green]: quit/q, help")
    typer.echo("\nExplore the dungeon and find the treasure room to win!")


def run_game() -> None:
    """Run the game in interactive mode."""
    typer.echo("[bold]Welcome to Dungeon Adventure![/bold]")
    typer.echo("Type 'help' for commands or 'quit' to exit.\n")
    
    rooms, starting_room = generate_dungeon()
    player = Player(
        health=100,
        inventory=[],
        current_room=starting_room,
        all_rooms=rooms
    )
    
    typer.echo(describe_room(player.current_room))
    
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
        typer.echo("\nThanks for playing!")
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