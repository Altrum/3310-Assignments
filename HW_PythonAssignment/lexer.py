# By Robert Chung
# HW for CSC 3310 - Concepts in Programming Languages
# Dr. Arias
# Lexer.py
# This program should take a program written in Mini-Power and output the
#   Tokens and Lexemes into a new file.

# QUESTIONS:
# 1) Do we exit from program if we find a syntax error? Or do we keep going?
# 3) How do you want us to format the output (spaces and stuff)
# 4) String token?? the ':' after a string in one of your example programs
# 5) You indicate that the quote should be a token, but it's never printed in any example programs.
#       Do you want us to print "QUOTE" when we encounter a quote, or just take it as a string?

# TODO
# 1) The last semicolon  -- done
# 2) Put it into an actual file instead of just printing -- done
# 3) Check program with tests (Faults)
# 4) Extra credit?
# 5) Think about more cases where things would be wrong (relates to #3 todo) -- done
# 6) Add comments -- done
# 7) Count number of tokens and stuff to print out to file
        # WHAT CONSTITUTES WHEN TO INCREASE COUNT WTF
# 8) Put the stuff you already encountered into a lookup table ?
# 9) Quote token -> Do you want QUOTE\n blah\n QUOTE\n

import sys

miniPowerLetters = ('a', 'b', 'c', 'd', 'e', 'f', 'e', 'g', 'h', 'i', 'j', 'k',
                    'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
                    'x', 'y', 'z')
miniPowerDigits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
miniPowerOtherTokens = {';': "SEMICOLON", '+': "PLUS", '-': "MINUS",
                        '*': "TIMES", '/': "DIV", '^': "POWER", '=': "ASSIGN",
                        '\"': "STRING", '(': "LPAREN", ')': "RPAREN"}
miniPowerType = {'#': "INTEGER", '%': "REAL", '$': "STRING"}

# Global file
f = ""
f_out = ""

# Global characters, tokens, and lexemes
ch = " "
token = ""
lexeme = ""
tokenCount = 0


def main():
    global f
    global f_out

    # ----------------------------------------------------------------- #
    #                   ======= FILE OPENING =======                    #
    #                      Opening Input File
    inputFile = sys.argv[1]
    try:
        f = open(inputFile, 'r')
    except IOError:
        print "Unable to open the file you specificed! Please try again."
        return
    # ----------------------------------------------------------------- #
    #                Opening Output File for writing
    outputFile = inputFile.split('.')[0] + ".out"
    try:
        f_out = open(outputFile, 'w')
    except IOError:
        print "Error creating new file for writing"
        return
    # ================================================================= #

    # Actual lex time now
    print "Processing input file ", inputFile
    while ch != "":
        lex()

    if token == "SEMICOLON":
        f_out.write("SYNTAX ERROR: shouldn't have semicolon at end of program\n")

    print tokenCount, " tokens produced"
    print "Result in file " + outputFile

    f.close()
    f_out.close()


def getNextChar():
    global ch
    global f

    # process the next character if its not EOF
    if ch != "":
        ch = f.read(1)


def getNextNonWhiteSpace():
    global ch
    global f

    while ch == " " or ch == '\n' or ch == '\t':
        getNextChar()


def lex():
    global ch
    global f_out

    getNextNonWhiteSpace()
    if ch in miniPowerLetters:
        handleIDToken()
    elif ch == '\"':
        handleSTRINGToken()
    elif ch in miniPowerOtherTokens:
        handleOtherTokens()
    elif ch in miniPowerDigits:
        handleNumbers()
    elif ch == 'P':
        checkAndHandlePrintToken()
    elif ch == "":
        return
    else:
        f_out.write("SYNTAX ERROR: Character not recognized!\n")
        getNextChar()


def handleIDToken():
    global ch
    global token
    global lexeme
    global tokenCount
    global f_out

    token = "ID"
    lexeme += ch
    getNextChar()

    # Loop until character isn't recognized by letter/digit
    #   add to current lexeme if it is recognized
    while ch in miniPowerLetters or ch in miniPowerDigits:
        lexeme += ch
        getNextChar()

    # ID must end with a type symbol.
    #   If not, then it should be error.
    if ch in miniPowerType:
        f_out.write(token + '\t' + lexeme + '\t' + miniPowerType[ch] + '\n')
        tokenCount += 1
    else:
        f_out.write("SYNTAX ERROR: Incorrect ID Grammer\n")

    getNextChar()
    # reset lexeme for next token/lexeme pair
    lexeme = ""


def handleSTRINGToken():
    global ch
    global lexeme
    global token
    global tokenCount
    global f_out

    token = "STRING"
    getNextChar()

    # Loop until character isn't recognized as a string format
    #   add to current lexeme if it is recognized
    while ch in miniPowerLetters or ch in miniPowerDigits or ch == ' ':
        lexeme += ch
        getNextChar()

    # String must end with a ".
    #   If not, then it should be an error.
    if ch == '\"':
        f_out.write(token + '\t' + lexeme + '\n')
        tokenCount += 1
    else:
        f_out.write("SYNTAX ERROR: Incorrect String Format\n")

    getNextChar()
    lexeme = ""


def handleNumbers():
    global ch
    global token
    global lexeme
    global tokenCount
    global f_out

    # Before encountering a '.' all we know is that it's a INT_CONST.
    #   We will later check and update if we encounter a '.'
    token = "INT_CONST"
    lexeme += ch
    getNextChar()

    # Loop until ch isn't recognized as a number.
    #   Add to current lexeme if it is recognized.
    while ch in miniPowerDigits:
        lexeme += ch
        getNextChar()

    # Check to see if the number was a decimal number
    #   Update the token to a real const if it is.
    if ch == '.':
        token = "REAL_CONST"
        lexeme += ch
        getNextChar()

        # Same loop as above, just getting rest of the numbers.
        while ch in miniPowerDigits:
            lexeme += ch
            getNextChar()

    f_out.write(token + '\t' + lexeme + '\n')
    tokenCount += 1
    lexeme = ""


def checkAndHandlePrintToken():
    global ch
    global token
    global lexeme
    global f_out

    # Not really that efficient imo, TODO make it better
    printStr = "PRINT"
    stringComp = ""
    while ch in printStr:
        stringComp += ch
        getNextChar()

    if stringComp == printStr:
        token = "PRINT"
        f_out.write(token + '\n')
    else:
        f_out.write("SYNTAX ERROR: Did you mean Print?\n")

    getNextChar()


def handleOtherTokens():
    global ch
    global token
    global f_out
    global tokenCount

    token = miniPowerOtherTokens[ch]
    f_out.write(token + '\n')
    #tokenCount += 1 TODO
    getNextChar()


if __name__ == "__main__":
    main()


# When encountered with error, could output error that you know of
#   And then ignore everything until the semicolon. (Possible another way)
