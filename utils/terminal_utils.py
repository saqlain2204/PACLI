from rich.console import Console
from rich.theme import Theme

# Custom theme for PACLI
custom_theme = Theme({
    "info": "bold cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "error": "bold red",
    "prompt": "bold magenta",
    "title": "bold blue underline",
    "event": "bold white",
    "user_input": "bold green",
})

console = Console(theme=custom_theme)

def print_info(message):
    console.print(message, style="info")

def print_success(message):
    console.print(message, style="success")

def print_warning(message):
    console.print(message, style="warning")

def print_error(message):
    console.print(message, style="error")

def print_prompt(message, end=""):
    console.print(message, style="prompt", end=end)

def print_title(message):
    console.print(message, style="title")

def print_event(message):
    console.print(message, style="event")
