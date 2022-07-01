import disnake
from disnake import Colour, Embed

def default_message(title: str = None, description: str = None, color: Colour = 0x8c73e6) -> Embed:
    return Embed(
        title=title, 
        description=description, 
        color=color
    )
    
def error_message(title: str = 'Error!', description: str = 'Unknown error', color: Colour = 0xE02B2B) -> Embed:
    return Embed(
        title=title,
        description=description,
        color=color
    )