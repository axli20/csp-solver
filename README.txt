This program can solve any map-coloring constraint satisfaction problems (CSP)
or any circuit-board CSP's.

Given a list of countries, a list of colors, and a list of neighboring country
pairs, the program will assign each country a color so that no two neighboring
countries have the same color.

For the circuit-board problems, given a circuit board, e.g.
  ..........
  ..........
  ..........

and some pieces, e.g.

eeeeeee    bbbbb
           bbbbb
aaa
aaa       cc
          cc
          cc

The program will return all the pieces placed onto the board with no overlap,
like so:

eeeeeee.cc
aaabbbbbcc
aaabbbbbcc
