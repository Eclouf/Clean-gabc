from colorama import init, Fore, Style, just_fix_windows_console

import re
from datetime import datetime

RED = '\033[31m'      # Rouge
GREEN = '\033[32m'    # Vert
YELLOW = '\033[33m'   # Jaune
RESET = '\033[0m'     # Réinitialiser la couleur

class CleanGABC:
    def __init__(self):
        init(autoreset=True)
        just_fix_windows_console()
        self.office = {1:"Alleluia",2:"Antiphona",3:"Canticum", 4:"Communio", 5:"Graduale", 6:"Hymnus", 7:"Improperia", 8:"Introitus", 9:"Kyriale", 10:"Offertorium", 11:"Toni Communes", 12:"Prosa", 13:"Praefationes", 14:"Psalmus", 15:"Responsorium breve", 16:"Responsorium", 17:"Rhythmus", 18:"Sequentia", 19:"Supplicatio", 20:"Tropa", 21:"Tractus", 22:"Varia"}
        

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
                    if i - 1 >= 0 and after[i - 1] in ',;:0123456789':
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
        print() 
        print(content)

    def office_part(self):
        print(YELLOW+"[warn]"+RESET+" Enter the type of office partition:  ")
        for i, (key, valeur) in enumerate(self.office.items()):
            print(f"        {key} - {valeur}", end="\t")
            if (i + 1) % 2 == 0:
                print()
        if len(self.office) % 2 !=0:
            print()
        office = input("Enter value(0-22): ")
        print()
        return self.office[int(office)]
        
    
    def clean(self, input_file, output_file):
        
        date = datetime.now()
        date = date.strftime("%d/%m/%Y")
        
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
        
        filtred_lines = []
        date_y = False
        ano_i = 0
        
        for line in lines:
            if "date:" in line:
                date_y = True
            if "annotation:"in line:
                ano_i += 1
        
        for line in lines:
            if not line.startswith(("transcriber")):
                if "date:" in line:
                    filtred_lines.append(f"date:{date};\n")
                    print(GREEN+"[info]"+ RESET+f" Date update: {date}")
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
                    print(GREEN+"[info]"+ RESET + " Name:",name)
                    
                if not date_y:
                    print(GREEN+"[info]"+ RESET + f" Add date: {date}")
                    filtred_lines.append(f"date:{date};\n")
            
        content = ''.join(filtred_lines)
            
        
        for char in ["(;)", "(:)", "(::)", "(,)", "(;3)", "(;4)", "(;6)"]:
            if char in content:
                content = content.replace(char, char + "\n" if content[content.index(char) + len(char):].startswith("\n") is False else char)
           
        for char in ["(c1)","(c2)","(c3)","(c4)", "(f3)","(f4)","(cb3)","(c2@c4)"]:
            if char in content:
                content = content.replace(char, char + "\n\n" if content[content.index(char) + len(char):].startswith("\n") is False else char)
                
        match = re.search(r'office-part:\s*(.*?)\s*;', content)     
        if match:
            content_between = match.group(1).strip()
            if content_between:
                print(GREEN+"[info]"+ RESET + " Office-part:", content_between)
            else:
                print(GREEN+"[info]"+ RESET + " Add office-part")
                office = self.office_part()
                #office_part = input("[warn]"+" Enter the type of office partition: ")
                content = re.sub(r'date:\s*(.*?)\s*;', r'date: \1;\noffice-part: ' + office + ';', content)
        else:
            print(GREEN+"[info]"+ RESET + " Add office-part")
            office = self.office_part()
            #office_part = input("[warn]"+" Enter the type of office partition: ")
            content = re.sub(r'date:\s*(.*?)\s*;', r'date: \1;\noffice-part: ' + office + ';', content)
            
        
        
            
        for char in ["<eu>","<nlba>"]:
            index = content.find(char)
            while index != -1:
            
                if index == 0 or content[index - 1] != "\n":
                    content = content.replace(char, "\n" + char, 1)
                index = content.find(char, index + 1)

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(content)
            
        return output_file
        


