# 1_prompt.py
from rich.prompt import Prompt
from rich.prompt import Confirm

print("Simple prompt:")
name = Prompt.ask("Enter your name")
print(f"{name=}")

print("Simple prompt with default:")
name = Prompt.ask("Enter your name", default="Paul Atreides")
print(f"{name=}")

print("Simple prompt with choices:")
name = Prompt.ask("Enter your name", choices=["Paul", "Jessica", "Duncan"], default="Paul")
print(f"{name=}")

print("Prompt with confirm:")
is_rich_great = Confirm.ask("Do you like rich?")
# assert is_rich_great
print(f"{is_rich_great=}")
