from src.commands import Console
  
console = Console()
args = console.parseArgs()
console.processCommand(args)