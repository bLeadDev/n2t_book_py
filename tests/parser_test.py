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

def test_parser_symbol_a_command():
    # GIVEN a parser with an A_COMMAND
    parser = Parser("tests\\test_files\\test_a_com_1.n2t")
    # WHEN symbol is called
    symbol = parser.symbol()
    # THEN symbol returns the expected value
    assert symbol == "32"
    
def test_parser_symbol_multiple_a_commands():
    # GIVEN a parser with an A_COMMAND
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

@pytest.mark.skip(reason="Skipping test_parser_symbol_multiple_a_commands_check_end")
def test_parser_symbol_multiple_a_commands_check_end():
    # GIVEN a parser with an A_COMMAND
    parser = Parser("tests\\test_files\\test_a_com_3.n2t")
    # WHEN advance is called 4 times
    parser.advance()
    parser.advance()
 #   parser.advance()
 #   parser.advance()    
    # THEN has_more_commands returns False
    assert parser.has_more_commands() == False
        
    
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
    assert has_more_commands == False
    
def test_has_more_commands_with_more_commands_than_the_current():
    # GIVEN a parser with more commands
    parser = Parser("tests\\test_files\\test_a_com_3.n2t")
    # WHEN has_more_commands is called
    has_more_commands = parser.has_more_commands()
    # THEN has_more_commands returns True
    assert has_more_commands == True    

