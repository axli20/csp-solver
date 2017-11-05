# author: Angela Li
# date: 10/17/17

class Constraint:

    # Constructor
    # @var_pair the pair of integers corresponding to the variables involved in the constraint
    # @values the list of allowable combinations of values for that pair of variables
    def __init__(self, var_pair, values):
        self.variable_pair = var_pair
        self.values = values
        self.inverse = (self.variable_pair[1], self.variable_pair[0])

    # Checks to see if the assignment satisfies the constraint '
    def is_satisfied(self, assignment):
        var1 = self.variable_pair[0]
        var2 = self.variable_pair[1]

        if assignment[var1] is None or assignment[var2] is None:
            return True

        value_pair = (assignment[var1], assignment[var2])

        return value_pair in self.values

    # Checks to see if a specific variable is involved in the constraint
    def involves(self, var):
        return var in self.variable_pair

    def __str__(self):
        s = "{" + str(self.variable_pair) + ": " + str(self.values) + "}"
        return s