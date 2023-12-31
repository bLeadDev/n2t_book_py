import pytest
import sys
from assembler.assembler import Parser, CommandType

### COMMAND TYPE TESTS ###
def test_parser_command_type_a_command():
    # GIVEN a parser with an A_COMMAND
    parser = Parser("tests\\test_files\\test_a_com_1.n2t")
    # WHEN command_type is called
    command_type = parser.command_type()
    # THEN command_type returns A_COMMAND
    assert command_type == CommandType.A_COMMAND

def test_parser_command_type_c_command():
    # GIVEN a parser with a C_COMMAND
    parser = Parser("tests\\test_files\\test_c_com_1.n2t")
    # WHEN command_type is called
    command_type = parser.command_type()
    # THEN command_type returns C_COMMAND
    assert command_type == CommandType.C_COMMAND

### SYMBOL TESTS ###

def test_parser_symbol_a_command():
    # GIVEN a parser with an A_COMMAND
    parser = Parser("tests\\test_files\\test_a_com_1.n2t")
    # WHEN symbol is called
    symbol = parser.symbol()
    # THEN symbol returns the expected value
    assert symbol == "32"
    
def test_parser_symbol_multiple_a_commands():
    # GIVEN a parser with three A_COMMANDs
    parser = Parser("tests\\test_files\\test_a_com_3.n2t")
    # WHEN symbol is called
    symbol = parser.symbol()
    # THEN symbol returns the expected values when advacing
    assert symbol == "32"
    parser.advance()
    symbol = parser.symbol()
    assert symbol == "33"   
    parser.advance()
    symbol = parser.symbol()
    assert symbol == "34"

def test_parser_symbol_multiple_a_commands_check_end():
    # GIVEN a parser with 3 A_COMMANDs
    parser = Parser("tests\\test_files\\test_a_com_3.n2t")
    # WHEN advance is called 3 times
    parser.advance()
    parser.advance()   
    parser.advance()   
    # THEN has_more_commands returns False
    assert parser.has_more_commands() == False
    
def test_parser_symbol_multiple_a_commands_check_end():
    # GIVEN a parser with 3 A_COMMANDs
    parser = Parser("tests\\test_files\\test_a_com_3.n2t")
    # WHEN advance is called 2 times
    parser.advance()
    parser.advance()   
    # THEN has_more_commands returns True   
    assert parser.has_more_commands() == True
    
def test_c_command_mnemonic_dest():
    # GIVEN a parser with a dest C_COMMAND
    parser = Parser("tests\\test_files\\test_c_com_1.n2t")
    # WHEN dest is called
    dest = parser.dest()
    # THEN dest returns the expected value
    assert dest == "M"
        
def test_c_command_mnemonic_comp():
    # GIVEN a parser with a comp C_COMMAND
    parser = Parser("tests\\test_files\\test_c_com_1.n2t")
    # WHEN dest is called
    dest = parser.comp()
    # THEN dest returns the expected value
    assert dest == "D+1"
    
def test_c_command_mnemonic_jump_without_command():
    # GIVEN a parser without a jump C_COMMAND
    parser = Parser("tests\\test_files\\test_c_com_1.n2t")
    # WHEN jump is called
    jump = parser.jump()
    # THEN jump returns the expected value
    assert jump == "null"
    
def test_c_command_mnemonic_comp_without_command():
    # GIVEN a parser with a comp C_COMMAND in line 5
    parser = Parser("tests\\test_files\\assembler_test.n2t")
    parser.advance()
    parser.advance()
    parser.advance()
    parser.advance()
    # WHEN comp is called
    comp = parser.comp()
    # THEN comp returns the expected value
    assert comp == "null"
    
def test_c_command_mnemonic_jump_in_line_4():
    # GIVEN a parser with a C_COMMAND, JMP in line 4
    parser = Parser("tests\\test_files\\test_c_com_all.n2t")
    # WHEN setting to line 4 and dest is called
    parser.advance()
    parser.advance()
    parser.advance()
    jmp = parser.jump()
    # THEN dest returns the expected value
    assert jmp == "JGT"
    

### COMMENT TESTS ###

def test_comments_with_one_command():
    # GIVEN a parser with a one command and a few comments
    parser = Parser("tests\\test_files\\comments.n2t")
    # WHEN checking for the symbol
    symbol = parser.symbol()
    # THEN symbol returns the expected value
    assert symbol == "32"
    
def test_only_comments():
    # GIVEN a parser with only comments
    parser = Parser("tests\\test_files\\comments_only.n2t")
    # WHEN checking if there are more commands
    has_more_commands = parser.has_more_commands()
    # THEN has_more_commands returns False
    assert has_more_commands == False
    
def test_reading_full_code_piece():
    # GIVEN a parser with a full code piece
    parser = Parser("tests\\test_files\\full_code_piece.n2t")
    # WHEN checking if there are more commands and advancing
    while parser.has_more_commands():
        parser.advance()
    #THEN no exception is raised
    
def test_reading_full_code_pieces_commands():
    # GIVEN a parser with a full code piece
    parser = Parser("tests\\test_files\\full_code_piece.n2t")
    # WHEN checking if there are more commands and advancing with calling the expected methods
    while parser.has_more_commands():
        if parser.command_type() == CommandType.C_COMMAND:
            parser.comp()
            parser.dest()
            parser.jump()
        elif parser.command_type() == CommandType.A_COMMAND:
            parser.symbol()
        parser.advance()
    #THEN no exception is raised


@pytest.mark.skip(reason="Skipping test_parser_symbol_l_command")
def test_parser_symbol_invalid_command():
    # GIVEN a parser with an invalid command type
    parser = Parser("tests\\test_files\\test_c_com_1.n2t")
    # WHEN symbol is called
    # THEN symbol raises an Exception
    with pytest.raises(Exception):
        symbol = parser.symbol()    

    

### INIT AND FILE HANDLING TESTS ###
def test_init_parser_with_valid_file():
    # GIVEN a valid file path
    # WHEN a parser is initialized with the file path
    parser = Parser("tests\\test_files\\test_a_com_1.n2t")
    # THEN the parser has a file attribute which is not None
    assert parser.line_iter is not None
    
def test_init_parser_with_valid_empty_file():
    # GIVEN a valid file path with an empty file
    # WHEN a parser is initialized with the file path
    parser = Parser("tests\\test_files\\empty.n2t")
    # THEN the parser has no more commands
    assert parser.has_more_commands() == False
 

@pytest.mark.skip(reason="Skipping test_init_parser_with_invalid_file")
def test_init_parser_with_invalid_file():
    # GIVEN an invalid file path
    # WHEN a parser is initialized with the file path
    # THEN the parser raises a FileNotFoundError
    with pytest.raises(FileNotFoundError):
        parser = Parser("tests\\test_files\\INVALId.n2t")
        
def test_has_more_commands_with_no_more_commands_than_the_current():
    # GIVEN a parser with more commands
    parser = Parser("tests\\test_files\\test_a_com_1.n2t")
    # WHEN has_more_commands is called
    has_more_commands = parser.has_more_commands()
    # THEN has_more_commands returns True
    assert has_more_commands == True
    
def test_has_more_commands_with_more_commands_than_the_current():
    # GIVEN a parser with more commands
    parser = Parser("tests\\test_files\\test_a_com_3.n2t")
    # WHEN has_more_commands is called
    has_more_commands = parser.has_more_commands()
    # THEN has_more_commands returns True
    assert has_more_commands == True    

