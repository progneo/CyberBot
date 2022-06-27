import disnake


def in_progress():
    return disnake.Embed(title="⏲ This feature is work in progress!",
                         description="Please stay tuned to our latest updates [here]("
                                     "https://github.com/ProgNeo/CyberBot)!", color=0x89CFF0)


def permission_denied():
    return disnake.Embed(title="🛑 Permission Denied!", description="You do not have permission to do this!",
                         color=0xFF0000)


def notfound(s):
    return disnake.Embed(title=f"😮 Oops! {s.capitalize()} not found!",
                         description=f"Unable to find the specified {s.lower()}!",
                         color=0xFF0000)


def downloading():
    return disnake.Embed(title="⏱ Downloading File...", description="Please wait for up to 3 seconds!",
                         color=0xFF0000)


def error(e="executing command"):
    return disnake.Embed(title=f"⚠ Unknown error occurred while {e}!",
                         description="Please report to [CyberBot](https://github.com/ProgNeo/CyberBot) developers [here](https://github.com/ProgNeo/CyberBot/issues)!",
                         color=0xFF0000)


def invalidargument(arg):
    return disnake.Embed(title="🟥 Invalid argument!", description=f"Valid argument(s): ``{arg}``",
                         color=0xFF0000)


def toomanyarguments():
    return disnake.Embed(title="🛑 Too many arguments!", description=f"You have entered too many arguments!",
                         color=0xFF0000)