from colorama import init, Fore, Style
import re
from datetime import datetime


class CleanGABC:

    def __init__(slef):
        init(autoreset=True)

    def color_text(self, filegabc):

        with open(filegabc, "r", encoding="utf-8") as file:
            content = file.read()

        content = content.replace("%%", Fore.GREEN + "%%")
        word_list = [
            "name:",
            "gabc-copyright:",
            "score-copyright:",
            "office-part:",
            "occasion:",
            "meter:",
            "commentary:",
            "arranger:",
            "author:",
            "date:",
            "manuscript:",
            "manuscript-reference:",
            "manuscript-storage-place:",
            "book:",
            "language:",
            "transcriber:",
            "transcription-date:",
            "mode:",
            "user-notes:",
            "annotation:",
            ";",
        ]
        for word in word_list:
            if word in content:
                content = content.replace(
                    word, Style.BRIGHT + Fore.YELLOW + word + Fore.RESET
                )

        pos = content.find("%%")

        if pos != -1:

            before = content[: pos + 2]
            after = content[pos + 2 :]

            result = []
            in_parentheses = False
            in_cran = False
            in_para_spe = False

            for i in range(len(after)):
                char = after[i]
                if char in r".*+?'^${}/!§|_[]":
                    result.append(Fore.RED + char + Fore.RESET)
                elif char == "(":
                    if i + 1 < len(after) and after[i + 1] in r",;:":
                        result.append(Fore.YELLOW + char + Fore.RESET)
                        in_para_spe = True
                    else:
                        in_parentheses = True
                        result.append(Fore.CYAN + char + Fore.RESET)
                elif char == ")":
                    if i - 1 >= 0 and after[i - 1] in r",;:":
                        result.append(Fore.YELLOW + char + Fore.RESET)
                        in_para_spe = False
                    else:
                        in_parentheses = False
                        result.append(Fore.CYAN + char + Fore.RESET)
                elif in_para_spe:
                    result.append(Fore.YELLOW + char + Fore.RESET)
                elif in_parentheses:
                    if char in r"0123456789":
                        result.append(Fore.GREEN + char + Fore.RESET)
                    else:
                        result.append(Fore.CYAN + char + Fore.RESET)
                elif char == "<":
                    in_cran = True
                    result.append(Fore.YELLOW + char + Fore.RESET)
                elif char == ">":
                    in_cran = False
                    result.append(Fore.YELLOW + char + Fore.RESET)
                elif in_cran:
                    result.append(Fore.YELLOW + char + Fore.RESET)
                elif char == "\n":
                    result.append(char)
                else:
                    result.append(Fore.MAGENTA + char + Fore.RESET)

            content = before + "".join(result)
        print(content)

    def insert_line_breaks(self, input_file, output_file):
        
        date = datetime.now()
        date = date.strftime("%d/%m/%Y")
        
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        filtred_lines = []
        date_y = False
        ano_t = False
        ano_i = 0
        
        for line in lines:
            if "date:" in line:
                print("yes")
                date_y = True
            if "annotation:"in line:
                ano_i += 1
                print(ano_i)
        
        for line in lines:
            if not line.startswith(("transcriber")):
                if "date:" in line:
                    filtred_lines.append(f"date:{date};\n")
                elif "%%"in line and ano_i == 1:
                    filtred_lines.append("annotation:;\n%%\n")
                elif "%%"in line and ano_i == 0:
                    filtred_lines.append("annotation:;\nannotation:;\n%%\n")
                else:
                    filtred_lines.append(line)
            
                    
            if line.startswith("name:"):
                match = re.search(r"name:\s*(.*?);", line)
                
                if match:
                    name = match.group(1).strip()
                    print(name)
                    
                if not date_y:
                    filtred_lines.append(f"date:{date};\n")
 
        content = ''.join(filtred_lines)
            
        
        for char in ["(;)", "(:)", "(::)", "(,)"]:
           content = content.replace(char, char + "\n" if content[content.index(char) + len(char):].startswith("\n") is False else char)
           
        for char in ["<eu>","<nlba>"]:
            index = content.find(char)
            while index != -1:
            
                if index == 0 or content[index - 1] != "\n":
                    content = content.replace(char, "\n" + char, 1)
                index = content.find(char, index + 1)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(content)
            
        return output_file
        


