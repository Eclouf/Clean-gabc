import argparse
import sys
from cor import CleanGABC

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
            args = parser.parse_args()

            
            if args.output:
                result = score.insert_line_breaks(args.file, args.output)
            else:
                result = score.insert_line_breaks(args.file, args.file)
            if args.color:
                score.color_text(result)

        except SystemExit as e:
            print("Erreur : Arguments non valides.")
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