HOW TO RUN CODE

    Map Coloring:
    Run 'MapColoringCSP.py'

    Circuit Board:
    Run 'CircuitBoardCSP.py'

HOW TO TOGGLE INFERENCES AND HEURISTICS

    All runnable backtracking search code is located in 'backtracking_search.py'. Read the comment at the top.
    The only code you should comment/uncomment is located in the function 'backtracking_search(csp)'.
    Please do not comment/uncomment anything in the other functions of the file (except for print statements).

    In the function 'backtracking_search', there are mutliple 3-line blocks of code. Each has a comment describing what
    kind of backtracking it uses. E.g., if you want to test my MAC inference, uncomment the block that says 'MAC Inference',
    and make sure all the other blocks are commented. There should only ever be one block of uncommented code in order
    for the function to work.

    *NOTE:
    Toggling MRV and LCV in 'backtrack_mac':
        Adding MRV: Uncomment the 2-line block that says 'MRV Heuristic' AND comment out the 2-line block that says 'Chronological Select'.
        Adding LCV: Uncomment the 2-line block that says 'LCV Heuristic' AND comment out the 2-line block that says 'Randomize Values'.

HOW TO SEE ALGORITHM IN 'LIVE' ACTION

    To see the algorithm going through the process 'live', uncomment the print statements in the respective backtrackers.

    Locations (line numbers) of print statements:
    - backtrack_basic: 55, 58, 65
    - backtrack_fc: 91, 100
    - backtrack_MRV: 134, 143
    - backtrack_LCV: 173, 177, 181, 190
    - backtrack_MRV_LCV: 219, 223, 227, 235
    - backtrack_MAC:
            -In 'backtracking_search.py': 274, 282
            -In 'ConstraintSatisfactionProblem.py': 172, 178, 192, 194

INPUT FILE FORMATS

    Map Coloring:
    - Input file name: 'australia_map.txt'
    - line 1: list of countries, separated by ', '
    - line 2: colors, separated by ', '
    - line 3: neighboring country pairs of format 'country1-country2', separated by ', '

    Circuit Board:
    - Input file name: 'board.txt'
    - line 1: dimensions of the board in format 'nxm'
    - following lines: the various "pieces", with no blank lines between pieces

HOW TO COMMENT/UNCOMMENT LINES

    Highlight all the lines you want to comment/uncomment.

    Mac: Command + '/'
    PC: Ctrl + '/'


