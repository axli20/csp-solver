# author: Angela Li
# date: 10/17/17

from Constraint import Constraint
from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem
from backtracking_search import backtracking_search

class MapColoringCSP:

    # Constructor
    def __init__(self, map_filename):
        self.variables = []
        self.domain = None
        self.int_domains = []
        self.constraint_pairs = []
        self.constraints = []
        self.connections = []

        f = open(map_filename)
        line_num = 0
        for line in f:
            line = line.strip()
            components = line.split(", ")

            if line_num == 0:
                self.variables = components

            if line_num == 1:
                self.generate_domains(tuple(components))

            if line_num == 2:
                self.init_connections()
                self.generate_pairs_connections(components)

            line_num += 1

        f.close()

        self.legal_constraint_values = self.legal_values(self.int_domains[0])
        self.generate_constraints()

        self.int_csp = ConstraintSatisfactionProblem(len(self.variables), self.connections, self.int_domains, self.constraints)

    # Generates the legal values based on the domain
    def legal_values(self, domain):
        lv = []
        for val1 in range(0, len(domain)):
            for val2 in range(0, len(domain)):
                if val1 != val2:
                    lv.append((val1, val2))

        return lv

    # Generates the binary constraint pairs and connections hashtable given from the constraints in the text file
    def generate_pairs_connections(self, components):
        for component in components:
            variables = component.split("-")
            var1_index = self.variables.index(variables[0])
            var2_index = self.variables.index(variables[1])

            # Creating and adding the binary pair
            var_pair = (var1_index, var2_index)
            self.constraint_pairs.append(var_pair)

            # Adding variables to the connections hash table
            self.connections[var1_index].append(var2_index)
            self.connections[var2_index].append(var1_index)


    # Generates the constraint objects from the constraint pairs and legal values
    def generate_constraints(self):
        for pair in self.constraint_pairs:
            self.constraints.append(Constraint(pair, self.legal_constraint_values))

    # Initializes the connections hashtable
    def init_connections(self):
        for i in range(len(self.variables)):
            self.connections.append([])

    # Generates the domains array
    def generate_domains(self, domain):
        int_domain = []

        for i in range(0, len(domain)):
            int_domain.append(i)

        for i in range(0, len(self.variables)):
            self.int_domains.append(tuple(int_domain))

        self.domain = domain

    # Prints the solution to the backtracking search in word form. (e.g. Country name: color)
    def solution(self):
        result = backtracking_search(self.int_csp)
        sol = ""

        for i in range(0, len(result)):
            sol += self.variables[i] + ": " + self.domain[result[i]] + "\n"

        print(sol)



if __name__ == "__main__":
    test = MapColoringCSP("australia_map.txt")
    test.solution()

