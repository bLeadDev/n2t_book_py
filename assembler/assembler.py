import sys
import more_itertools

from enum import Enum

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
        pass
    
    def comp(self) -> str:
        pass
    
    def jump(self) -> str:
        pass
    
        
def main():
    if len(sys.argv) < 2:
        print("Please provide a filename/path as a parameter.")
        return

    filepath = sys.argv[1]
    
    

if __name__ == "__main__":
    main()
