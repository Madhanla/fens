"""
fen.py
Transform a FEN code into a Wikipedia diagram
"""
license = """
LICENSE (MIT)
Copyright (c) 2023 Madhanla

Permission is hereby granted, free  of charge, to any person obtaining
a  copy  of this  software  and  associated documentation  files  (the
"Software"), to  deal in  the Software without  restriction, including
without limitation  the rights to  use, copy, modify,  merge, publish,
distribute, sublicense,  and/or sell  copies of  the Software,  and to
permit persons to whom the Software  is furnished to do so, subject to
the following conditions:

The  above  copyright  notice  and this  permission  notice  shall  be
included in all copies or substantial portions of the Software.

THE  SOFTWARE IS  PROVIDED  "AS  IS", WITHOUT  WARRANTY  OF ANY  KIND,
EXPRESS OR  IMPLIED, INCLUDING  BUT NOT LIMITED  TO THE  WARRANTIES OF
MERCHANTABILITY,    FITNESS    FOR    A   PARTICULAR    PURPOSE    AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING  FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
class FenException(Exception):
    """Syntax Error in FEN"""

class Square:
    """Class that wraps  strings as only some letters  are valid piece
    names"""
    def __init__(self, piece):
        if piece in "PBNRQKpbnrqk AaCcFfGgMmEeSsHhZzWw":
            self.piece = piece
        elif type(piece) is str:
            raise FenException("Invalid piece " + piece)
        else:
            raise FenException("Invalid piece")

    def isempty(self):
        return self.piece == ' '

    def iswhite(self):
        return self.piece.isupper()

    def uncolor(self):
        return self.piece.lower()

    def wikiformat(self):
        """In FEN, an  uppercase piece name means  it's white, whereas
        lowercase piece  name means it's  black.  In wiki  format, all
        piece names  are lowercase.  To distinguish  between black and
        white, a `d' (dark) or `l' (light) is appended at the end
        """
        if self.isempty():
            return '  '
        c = 'd'
        if self.iswhite():
            c = 'l'
        return self.uncolor() + c

    def __str__(self):
        return str(self.piece)
    def __repr__(self):
        """ TODO: Remove """
        return str(self.piece)

class Position:
    """A class that stores all the information about a chess position
    that one can unravel from its FEN code.

    """
    def __init__(self, fen):
        """ Parse a FEN code into a Position """
        if type(fen) is not str:
            raise FenException("Invalid fen type")

        # Empty board
        self.squares = [[Square(' ') for _ in range(8)] for _ in
                        range(8)]
        self.side = None
        self.castling = None
        self.enpeassant = None
        self.draw_moves = 0
        self.move_number = 0

        # Fill up the  board from the top left (`i'  is column, `j' is
        # row)
        i = j = 0

        # `state'  is   one  of  "board",  "bar",   "space1",  "side",
        # "space2",  "castling", "enpeassant",  "space3" "draw_moves",
        # "move_number", in order of appearance in FEN
        state = 'board'
        for char in fen:
            if state in ["space1", "space2", "space3"] and char != ' ':
                raise FenException("Expected space but got " + char)
            if state == 'space1':
                state = 'side'
                continue
            if state == 'space2':
                state = 'castling'
                continue
            if state == 'space3':
                state = 'draw_moves'
                continue
            if state == 'side':
                state = 'space2'
                if char in 'wb':
                    self.side = char
                    continue
                raise FenException("Unknown side to move " + char)
            if state == 'castling':
                if char.isspace():
                    state = 'enpeassant'
                    continue
                if char == '-':
                    self.castling = ''
                    continue
                if char in 'KQkq':
                    if self.castling is None:
                        self.castling = ''
                    self.castling += char
                    continue
                raise FenException("Unkown castling side " + char)
            if state == 'enpeassant':
                if char.isalpha():
                    if(self.enpeassant is None):
                        self.enpeassant = char
                        continue
                    raise FenException('Wrong en peassant ' +
                                    self.enpeassant + char)
                if char.isnumeric():
                    self.enpeassant += char
                    state = 'space3'
                    continue
                if char == '-':
                    state = 'space3'
                    continue
                raise FenException('Unknown en peassant: ' + char)
            if state == 'draw_moves':
                if char.isspace():
                    state = 'move_number'
                    continue
                if char.isnumeric():
                    self.draw_moves = 10*self.draw_moves + int(char)
                    continue
                raise FenException("Not a number for draw_moves: " + char)
            if state == 'move_number':
                if char.isnumeric():
                    self.move_number = 10*self.move_number + int(char)
                    continue
                raise FenException("Not a number for move_number: " + char)
            if state == 'bar':
                if char == '/':
                    state = 'board'
                    continue
                raise FenException("Expected bar")

            if state != 'board':
                raise Exception("Unknown state " + state)
            if char.isnumeric():
                char = int(char)
                if char == 0:
                    raise FenException("0 in fen")
                while char != 0:
                    char -= 1
                    i += 1
                    if i == 8:
                        i = 0
                        j += 1
                        state = 'bar'
                        if char != 0:
                            raise FenException("Number too big in fen")
                        if j == 8:
                            state = 'space1'
                        continue
                continue
            self.squares[j][i] = Square(char)
            i += 1
            if i == 8:
                i = 0
                j += 1
                state = 'bar'
                if j == 8:
                    state = 'space1'
                continue

    def longside(self):
        """ Whole name of the side to move """
        if self.side == 'w':
            return 'blancas'
        if self.side == 'b':
            return 'negras'
        return ''

    def __str__(self):
        """ Pretty print board """
        s = ''
        for j in range(8):
            s += '\t|'
            for i in range(8):
                s += str(self.squares[j][i]) + '|'
            s += '\n'
        s += '  '
        if self.side:
            s += 'Side: ' + self.side + '   '
        if self.castling is not None:
            s += 'Castling: ' + self.castling + '   '
        if self.enpeassant is not None:
            s += 'En peassant: ' + self.enpeassant + '   '
        if self.draw_moves is not None:
            s += 'Fifty move rule: ' + str(self.draw_moves) + '   '
        if self.move_number is not None:
            s += 'Move number: ' + str(self.move_number)
        return s

    def __repr__(self):
        """ TODO: Remove """
        return self.__str__()

def pos2diagram(pos, alignment = '', header = '', footer = ''):
    """ Chess diagram in Wikipedia format """
    if type(pos) is not Position:
        raise TypeError("`pos2diagram' must be called with a \
        Position but received " + str(pos))

    if not alignment in ['tright', 'tleft', '']:
        raise TypeError("`alignment' must be `tright' or\
        `tleft'. Invalid" + str(alignment))

    s = '{{Diagrama de ajedrez'
    s += '\n| ' + alignment
    s += '\n| ' + header
    s += '\n|=\n'
    for j in range(8):
        s += ' ' + str(8-j) + ' '
        for i in range(8):
            s += '|' + pos.squares[j][i].wikiformat()
        s += '|=\n'
    s += '    a  b  c  d  e  f  g  h\n'
    s += '| ' + footer + '\n}}'
    return s

def substitute_vars(string, position):
    """Substitute the  variable value in `position'  for each variable
    name in `string'
    """
    result = ""        #  Final string
    state = "normal"   #  What is expected next (one of "normal",
                       #  "var", "number")
    column = None      #  Current column for state "number"
    for char in string:
        if state == "normal":
            if char == "%":
                state = "var"
                continue
            result += char
            continue
        if state == "var":
            column = {
                'A': 0,
                'B': 1,
                'C': 2,
                'D': 3,
                'E': 4,
                'F': 5,
                'G': 6,
                'H': 7}.get(char)
            if column is not None:
                state = "number"
                continue
            state = "normal"
            if char == "m":
                result += str(position.move_number)
                continue
            if char == "s":
                result += position.longside()
                continue
            if char == "e":
                result += str(position.enpeassant)
                continue
            if char == "d":
                result += str(position.draw_moves)
                continue
            if char == "c":
                result += str(position.castling)
                continue
            if char == "%":
                result += "%"
                continue
            raise FenException("Unrecognized variable name " + char)
        if state == "number":
            if char in "12345678":
                row = 8-int(char)
                result += str(position.squares[row][column])
                column = None
                state = "normal"
                continue
            raise FenException("Nonexistent row " + char)
        raise Exception("Unknwon state " + state)
    return result

if __name__ == "__main__":
    import argparse
    header_help = "add a header. See section Variables"
    footer_help = "add a footer. If FOOTER is not provided, the move \
number and side to move are used. See section Variables"

    alignment_help = "align according to ALIGNMENT which is one of \
`tleft' or `tright'"

    vars_help = """Variables:
  The percent sign `%' can be used in options -h and -f to add one
  of  the variables  in section  Variables. Unrecoginzed  variable
  names  will  lead to  an  error.   Variable  names need  not  be
  followed by a space as there is no ambiguity

    %m                     full move number
    %s                     side to move
    %e                     possible en peassant capture
    %d                     number of full moves since last capture
                           or pawn advance (see 50 moves rule)
    %c                     castling rights as in FEN
    %A1, ..., %H8          piece on a particular square as in FEN
    %%                     Literal `%' sign
"""
    parser = argparse.ArgumentParser(
        prog = 'python3 fen.py',
        description = 'Transforms a FEN code into a Wikipedia diagram',
        epilog = vars_help + license,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('fen')
    parser.add_argument('-H', '--header',
                        default='',
                        help=header_help)
    parser.add_argument('-F', '--footer',
                        default='',
                        const='Las %s mueven',
                        nargs='?',
                        help=footer_help)
    parser.add_argument('-A', '--alignment',
                        default='',
                        choices=['', 'tright', 'tleft'],
                        help=alignment_help)
    args = parser.parse_args()

    position = Position(args.fen)
    header = substitute_vars(args.header, position)
    footer = substitute_vars(args.footer, position)
    diagram = pos2diagram(position,
                      alignment=args.alignment,
                      header=header,
                      footer=footer)
    print(str(diagram))
