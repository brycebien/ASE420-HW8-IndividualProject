from src.commands import Console

while(True):        
    console = Console()
    user_input = input("Enter a command (record DATE FROM TO TASK :TAG)(query :TAG or DATE or TASK) ")
    console.processCommand(user_input)
    console.runCommands()