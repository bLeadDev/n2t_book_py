import sys
import more_itertools

from enum import Enum

class Code:
    @staticmethod
    def dest(str):
        switcher = {
            "null": "000",
            "M": "001",
            "D": "010",
            "MD": "011",
            "A": "100",
            "AM": "101",
            "AD": "110",
            "AMD": "111",
        }
        return switcher.get(str, "000")
    
    @staticmethod
    def comp(str):
        switcher = {
            # a = 0
            "0":      "0101010",
            "1":      "0111111",
            "-1":     "0111010",
            "D":      "0001100",
            "A":      "0110000",
            "!D":     "0001101",
            "!A":     "0110001",
            "-D":     "0001111",
            "-A":     "0110011",
            "D+1":    "0011111",
            "A+1":    "0110111",
            "D-1":    "0001110",
            "A-1":    "0110010",
            "D+A":    "0000010",
            "D-A":    "0010011",
            "A-D":    "0000111",
            "D&A":    "0000000",
            "D|A":    "0010101",
            # a = 1
            "M":      "1110000",
            "!M":     "1110001",
            "-M":     "1110011",
            "M+1":    "1110111",
            "M-1":    "1110010",
            "D+M":    "1000010",
            "D-M":    "1010011",
            "M-D":    "1000111",
            "D&M":    "1000000",
            "D|M":    "1010101",                
        }
        return switcher.get(str, "0000000")
    
    @staticmethod
    def jump(str):
        switcher = {
            "null": "000",
            "JGT": "001",
            "JEQ": "010",
            "JGE": "011",
            "JLT": "100",
            "JNE": "101",
            "JLE": "110",
            "JMP": "111",
        }
        return switcher.get(str, "000")

class CommandType(Enum):
    A_COMMAND = 0
    C_COMMAND = 1
    L_COMMAND = 2

class Parser:
    def __init__(self, path): 
        self.file_lines = [line.rstrip("\n\r ") for line in open(path, "r").readlines()]
        self.line_iter = more_itertools.peekable(iter(self.file_lines))          
        self.actual_line = None
        self.advance() # Advance to first command. If file is empty, this will set actual_line to None
    
    def has_more_commands(self) -> bool:
        try:
            return self.line_iter.peek() is not None
        except StopIteration:
            return False
    
    def advance(self) -> None:
        try:
            self.actual_line = next(self.line_iter)
            # Process the next line here
        except StopIteration:
            # Handle the end of the file
            self.actual_line = None           
            
    
    def command_type(self) -> CommandType:
        switcher = {
            "@": CommandType.A_COMMAND,
            "(": CommandType.L_COMMAND,
        }
        return switcher.get(self.actual_line[0], CommandType.C_COMMAND)
        
    
    def symbol(self) -> str:
        if self.command_type() == CommandType.A_COMMAND:
            return self.actual_line[1:]
        elif self.command_type() == CommandType.L_COMMAND:
            return self.actual_line[1:-1]
        else:
            raise Exception("Command type is not A_COMMAND or L_COMMAND")
    
    def dest(self) -> str:
        return self.actual_line.split("=")[0]
        
    def comp(self) -> str:
        return self.actual_line.split("=")[1]
    
    def jump(self) -> str:
        return self.actual_line.split(";")[1]        
    
    
        
def main():
    if len(sys.argv) < 2:
        print("Please provide a filename/path as a parameter.")
        return

    filepath = sys.argv[1]
    
    p = Parser(filepath)
    
    while p.has_more_commands():
        print(p.actual_line)
        p.advance()
    
    

if __name__ == "__main__":
    main()
