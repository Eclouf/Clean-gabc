import argparse, time
import sys
from cor import CleanGABC

RED = '\033[31m'      # Rouge
GREEN = '\033[32m'    # Vert
YELLOW = '\033[33m'   # Jaune
RESET = '\033[0m'     # Réinitialiser la couleur

class Command:
    
    @staticmethod
    def print_help():
        print("""
Usage: Clean-gabc [OPTION] FILE 

Options:
    -h, --help                      Print this help text and exit
    -c, --color                     Color text for read
    -o, --output                    Path for the result
        """)
    
    def run(self):
        parser = argparse.ArgumentParser(description="Clean GABC tool")
        parser.add_argument("-c", "--color",action='store_true', required=False)
        parser.add_argument("-o", "--output", type=str, required=False, help="Path for the result")
        parser.add_argument("file", type=str, help="Input file")

        score = CleanGABC()
        
        try:
            time_0 = time.time()
            args = parser.parse_args()

            
            if args.output:
                result = score.clean(args.file, args.output)
            else:
                result = score.clean(args.file, args.file)
            if args.color:
                score.color_text(result)
            time_1 = time.time()

            print(f"Execution de la tâche en : {time_1 - time_0 : .6f} seconde")
        except SystemExit as e:
            print(RED+"[erro]"+RESET+" Arguments non valides.")
            print("Utilisez -h ou --help pour voir l'aide.")
            sys.exit(1)

def main():
    if len(sys.argv) == 1 or '-h' in sys.argv or '--help' in sys.argv:
        Command.print_help()
        sys.exit(0)
    
    command_instance = Command()
    command_instance.run()

if __name__ == "__main__":
    main()