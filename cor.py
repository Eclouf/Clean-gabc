from colorama import init, Fore, Style, just_fix_windows_console

import re
from datetime import datetime


class CleanGABC:
    def __init__(self):
        init(autoreset=True)
        just_fix_windows_console()
        

    def color_text(self, filegabc):
        with open(filegabc, "r", encoding="utf-8") as file:
            content = file.read()

        # Remplacer "%%" par sa version colorée
        content = content.replace("%%", Fore.GREEN + "%%")
        pos = content.find("%%")
        before = content[:pos + 2]
        after = content[pos + 2:]
        
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

        # Remplacement des mots en tenant compte de la casse
        for word in word_list:
            before = before.replace(word, Fore.YELLOW + word+ Fore.RESET )


        if pos != -1:

            result = []
            in_para_spe = False
            in_parentheses = False
            in_cran = False

            for i in range(len(after)):
                char = after[i]
                if char in r".*+?'^${}/!|_[]":
                    result.append(Fore.RED + char + Fore.RESET)
                elif char == "(":
                    if i + 1 < len(after) and after[i + 1] in r'[,;:]':
                        result.append(Fore.YELLOW + char + Fore.RESET)
                        in_para_spe = True
                    else:
                        in_parentheses = True
                        result.append(Fore.CYAN + char + Fore.RESET)
                elif char == ")":
                    if i - 1 >= 0 and after[i - 1] in r'[,;:]':
                        result.append(Fore.YELLOW + char + Fore.RESET)
                        in_para_spe = False
                    else:
                        in_parentheses = False
                        result.append(Fore.CYAN + char + Fore.RESET)
                elif char == ";":
                    result.append(Fore.YELLOW + char + Fore.RESET)
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
                    filtred_lines.append("annotation:;\n\n%%\n\n")
                elif "%%"in line and ano_i == 0:
                    filtred_lines.append("annotation:;\nannotation:;\n\n%%\n\n")
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
           
        #for char in ["(c1)","(c2)","(c3)","(c4)", "(f3)","(f4)","(cb3)","(c2@c4)"]:
            #content = content.replace(char, char+'\n\n')
           
        for char in ["<eu>","<nlba>"]:
            index = content.find(char)
            while index != -1:
            
                if index == 0 or content[index - 1] != "\n":
                    content = content.replace(char, "\n" + char, 1)
                index = content.find(char, index + 1)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(content)
            
        return output_file
        


