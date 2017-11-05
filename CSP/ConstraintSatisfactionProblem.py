# author: Angela Li
# date: 10/17/17

class ConstraintSatisfactionProblem:

    # Constructor
    def __init__(self, num_variables, var_connections, variable_values, constraints):
        self.num_var = num_variables
        self.var_connections = var_connections
        self.unassigned_variables = self.create_unassigned()
        self.variable_values = variable_values
        self.constraints = constraints
        self.assignment = self.initialize_assignment()

    # Initializing the assignment array
    def initialize_assignment(self):
        asn = []
        for i in range(0, self.num_var):
            asn.append(None)
        return asn

    # The assignment is complete if there are no more unassigned variables
    def assignment_complete(self):
        return len(self.unassigned_variables) == 0

    # Adds all the variables to a set of unassigned variables
    def create_unassigned(self):
        unassigned = set()
        for i in range(0, self.num_var):
            unassigned.add(i)
        return unassigned

    # Changes a specific variable's status back to unassigned
    def replace_unassigned(self, var):
        self.unassigned_variables.add(var)

    def is_consistent(self, assignment, value, var):
        assignment[var] = value

        for constraint in self.constraints:
            if constraint.involves(var):
                if not constraint.is_satisfied(assignment):
                    assignment[var] = None
                    return False

        return True

    # Removes a specified value from the specified variable's domain in variable_values
    def remove_from_domain(self, var, value):

        # Get the domain of the variable and remove the value
        domain = self.variable_values[var]
        domain = list(domain)
        domain.remove(value)

        # Set the domain of the variable to the newly updated domain
        self.variable_values[var] = tuple(domain)

    # Forward checker that removes values from neighboring variables as they are assigned
    def forward_check(self, var, value):
        # Dealing with self domain
        self.variable_values[var] = (value,)

        # Dealing with neighbor domains
        neighbors = self.var_connections[var]
        if neighbors == None:
            return True

        for neighbor in neighbors:
            if neighbor in self.unassigned_variables and value in self.variable_values[neighbor]:
                self.remove_from_domain(neighbor, value)
                if len(self.variable_values[neighbor]) == 0:
                    return False

        return True

    # Chronological selecting of unassigned variables
    def chronological_select(self):
        if len(self.unassigned_variables) > 0:
            v = self.unassigned_variables.pop()
            return v
        return None

    # Minimum-remaining-values heuristic for selecting an unassigned variable
    def mrv_select(self):
        unassigned = list(self.unassigned_variables)
        min_var = unassigned[0]

        for i in range(1, len(unassigned)):
            if (len(self.variable_values[unassigned[i]]) < len(self.variable_values[min_var])):
                min_var = unassigned[i]

        self.unassigned_variables.remove(min_var)
        return min_var

    # Calculates the number of constrains on neighbors that would result from assigning val to var
    def calculate_constrain_factor(self, var, val):
        constrains = 0
        neighbors = self.var_connections[var]
        if neighbors is None:
            return constrains

        for neighbor in neighbors:
            if val in self.variable_values[neighbor]:
                constrains += 1

        return constrains


    # Orders a set of values, prioritizing the least-constraining value given a variable and a set of values
    def lcv(self, var, values):
        dict = {}
        sorted_values = []
        for value in values:
            dict[value] = self.calculate_constrain_factor(var, value)

        # Sorts the dictionary in ascending order based on values
        ascending = sorted(dict.items(), key=lambda v: v[1])

        for pair in ascending:
            sorted_values.append(pair[0])

        return sorted_values

    # Finds and returns the constraint involving the two variables
    def find_constraint(self, var1, var2):
        for constraint in self.constraints:
            if constraint.involves(var1) and constraint.involves(var2):
                return constraint

        return None

    # MAC inference
    def mac(self, var, value):
        # Dealing with self domain
        self.variable_values[var] = (value,)

        q = set()
        neighbors = self.var_connections[var]

        if neighbors is not None:
            for neighbor in neighbors:
                if neighbor in self.unassigned_variables:
                    q.add((neighbor, var))

        while len(q) > 0:
            pair = q.pop()
            var1 = pair[0]
            var2 = pair[1]
            if self.revise(var1, var2):
                # print("     Domains: " + str(self.variable_values) + "\n")
                if len(self.variable_values[var1]) == 0:
                    return False
                next_neighbors = self.var_connections[var1]
                if next_neighbors is not None:
                    for neighbor in next_neighbors:
                        if neighbor != var:
                            q.add((neighbor, var1))

        return True



    # Revise helper method to see if the domain of a pair has been revised
    def revise(self, var1, var2):

        revised = False
        domain1 = self.variable_values[var1]
        domain2 = self.variable_values[var2]
        constraint = self.find_constraint(var1, var2)

        # print("variables: " + "(" + str(var1) + ", " + str(var2) + ")")
        for value1 in domain1:
            satisfies_constraint = False
            for value2 in domain2:
                value_pair = (value1, value2)
                inverse = (value2, value1)
                # print("value pair: " + str(value_pair))

                # Since order matters in constraints, we must check if the variables
                # are in the same order as the constriant variables
                if (var1, var2) == constraint.variable_pair:
                    if value_pair in constraint.values:
                        satisfies_constraint = True
                        break
                else:
                    if inverse in constraint.values:
                        satisfies_constraint = True
                        break

            if not satisfies_constraint:
                # print("revised domain of index: " + str(var1))
                self.remove_from_domain(var1, value1)
                # print("     Domains: " + str(self.variable_values) + "\n")
                revised = True

        return revised