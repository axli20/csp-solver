# author: Angela Li
# date: 10/17/17

import random

# Each 3-line block of code below runs the heuristics specified in the comment
# Toggle comments to enable/disable heuristics and inference
# (to uncomment/re-comment, highlight block of code and hit Command(Ctrl for PC) '/')
def backtracking_search(csp):

    # Basic backtrack, no heuristics or inferences
    print("\n**** Basic Backtrack ****\n")
    result = backtrack_basic(csp.assignment, csp)

    # # Forward-checking
    # print("\n**** Forward-checking Backtrack ****\n")
    # result = backtrack_fc(csp.assignment, csp)

    # # FC and MRV heuristic
    # print("\n**** Forward-checking Backtrack with MRV Heuristic ****\n")
    # result = backtrack_mrv(csp.assignment, csp)

    # # FC and LCV heuristic
    # print("\n**** Forward-checking Backtrack with LCV Heuristic ****\n")
    # result = backtrack_lcv(csp.assignment, csp)

    # # FC, MRV, and LCV heuristic
    # print("\n**** Forward-checking Backtrack with MRC and LCV Heuristic ****\n")
    # result = backtrack_mrv_lcv(csp.assignment, csp)

    # # MAC Inference (Toggle heuristics in the function backtrack_mac below)
    # print("\n**** MAC Inference ****\n")
    # result = backtrack_mac(csp.assignment, csp)

    # DO NOT TOUCH
    return result

# The most basic backtracker, with no forward-checking or heuristics
def backtrack_basic(assignment, csp):
    # If the assignment is complete (i. e. there are no unassigned variables left), return the assignment
    if csp.assignment_complete():
        return assignment

    # Otherwise, select an unassigned variable chronologically
    var = csp.chronological_select()

    # Get the domain of the unassigned variable
    values = list(csp.variable_values[var])

    # Randomly get the values in the domain of the variable
    random.shuffle(values)

    # Loop through the values
    for value in values:
        # print("Variable: " + str(var) + ", " + "value: " + str(value))
        # If the value is consistent with the partial assignment, recursively call backtrack
        if csp.is_consistent(assignment, value, var):
            # print("Value " + str(value) + " is consistent!\n")
            result = backtrack_basic(assignment, csp)

            # If the result is not a failure, return the result
            if result is not None:
                return result

    # print("No values consistent for var: " + str(var) + "\n")

    # If no consistent value found for a variable, add it back to the unassigned variables set
    csp.replace_unassigned(var)

    # Case where no solution is found
    return None

# Backtracker with forward-checking but no heuristics
def backtrack_fc(assignment, csp):

    # If the assignment is complete (i. e. there are no unassigned variables left), return the assignment
    if csp.assignment_complete():
        return assignment

    # Otherwise, select an unassigned variable chronologically
    var = csp.chronological_select()

    # Get the domain of the unassigned variable
    values = list(csp.variable_values[var])

    # Randomly get the values in the domain of the variable
    random.shuffle(values)

    # Loop through the values
    for value in values:
        # print("Variable: " + str(var) + ", " + "value: " + str(value))

        # Save the initial state of all the variable domains
        original_domains = list(csp.variable_values)

        if csp.is_consistent(assignment, value, var):
            # Forward check
            forward_check = csp.forward_check(var, value)

            # print("     Domains: " + str(csp.variable_values) + "\n")

            # Backtrack if forward checking is successful
            if forward_check:
                result = backtrack_fc(assignment, csp)
                if result is not None:
                    return result

        # Restores the initial domains of the variables
        csp.variable_values = list(original_domains)

    # If no consistent value found for a variable, add it back to the unassigned variables set
    csp.replace_unassigned(var)

    return None

# Backtracker with forward-checking and the MRV heuristic
def backtrack_mrv(assignment, csp):

    # If the assignment is complete (i. e. there are no unassigned variables left), return the assignment
    if csp.assignment_complete():
        return assignment

    # Otherwise, select an unassigned variable using MRV heuristic
    var = csp.mrv_select()

    # Get the domain of the unassigned variable
    values = list(csp.variable_values[var])

    # Randomly get the values in the domain of the variable
    random.shuffle(values)

    # Loop through the values
    for value in values:
        # print("Variable: " + str(var) + ", " + "value: " + str(value))

        # Save the initial state of all the variable domains
        original_domains = list(csp.variable_values)

        if csp.is_consistent(assignment, value, var):
            # Forward check
            forward_check = csp.forward_check(var, value)

            # print("     Domains: " + str(csp.variable_values) + "\n")

            # Backtrack if forward checking is successful
            if forward_check:
                result = backtrack_mrv(assignment, csp)
                if result is not None:
                    return result

        # Restores the initial domains of the variables: ***COMMENT OUT IF NOT USING MRV***
        csp.variable_values = list(original_domains)

    # If no consistent value found for a variable, add it back to the unassigned variables set
    csp.replace_unassigned(var)

    return None


# Backtracker with forward-checking and the LCV heuristic
def backtrack_lcv(assignment, csp):

    # If the assignment is complete (i. e. there are no unassigned variables left), return the assignment
    if csp.assignment_complete():
        return assignment

    # Otherwise, select an unassigned variable chronologically
    var = csp.chronological_select()

    # Get the domain of the unassigned variable
    values = list(csp.variable_values[var])
    random.shuffle(values)
    # print("Shuffled: " + str(values))

    # Sort the values into ascending order based on least-constraining properties
    values = csp.lcv(var, values)
    # print("Ordered using LCV: " + str(values))

    # Loop through the values
    for value in values:
        # print("Variable: " + str(var) + ", " + "value: " + str(value))

        # Save the initial state of all the variable domains
        original_domains = list(csp.variable_values)

        if csp.is_consistent(assignment, value, var):
            # Forward check
            forward_check = csp.forward_check(var, value)

            # print("     Domains: " + str(csp.variable_values) + "\n")

            # Backtrack if forward checking is successful
            if forward_check:
                result = backtrack_lcv(assignment, csp)
                if result is not None:
                    return result

        # Restores the initial domains of the variables: ***COMMENT OUT IF NOT USING MRV***
        csp.variable_values = list(original_domains)

    # If no consistent value found for a variable, add it back to the unassigned variables set
    csp.replace_unassigned(var)

    return None

# Backtracker with forward-checking, MRV, and LCV
def backtrack_mrv_lcv(assignment, csp):

    # If the assignment is complete (i. e. there are no unassigned variables left), return the assignment
    if csp.assignment_complete():
        return assignment

    # Otherwise, select an unassigned variable using MRV heuristic
    var = csp.mrv_select()

    # Get the domain of the unassigned variable
    values = list(csp.variable_values[var])
    random.shuffle(values)
    # print("Shuffled: " + str(values))

    # Sort the values into ascending order based on least-constraining properties
    values = csp.lcv(var, values)
    # print("Ordered using LCV: " + str(values))

    # Loop through the values
    for value in values:
        # print("Variable: " + str(var) + ", " + "value: " + str(value))

        # Save the initial state of all the variable domains
        original_domains = list(csp.variable_values)

        if csp.is_consistent(assignment, value, var):
            # Forward check
            forward_check = csp.forward_check(var, value)
            # print("     Domains: " + str(csp.variable_values) + "\n")
            if forward_check:

                result = backtrack_mrv_lcv(assignment, csp)
                if result is not None:
                    return result

        # Restores the initial domains of the variables: ***COMMENT OUT IF NOT USING MRV***
        csp.variable_values = list(original_domains)

    # If no consistent value found for a variable, add it back to the unassigned variables set
    csp.replace_unassigned(var)

    return None

# Backtracker with MAC inference (to add MRV and/or LCV, toggle with comment blocks below)
def backtrack_mac(assignment, csp):

    # If the assignment is complete (i. e. there are no unassigned variables left), return the assignment
    if csp.assignment_complete():
        return assignment

    # # MRV Heuristic
    # var = csp.mrv_select()

    # Chronological Select
    var = csp.chronological_select()

    # Get the domain of the unassigned variable
    values = list(csp.variable_values[var])

    # Randomize values
    random.shuffle(values)

    # # LCV Heuristic
    # values = csp.lcv(var, values)

    # Loop through the values
    for value in values:
        # print("Variable: " + str(var) + ", " + "value: " + str(value))

        # Save the initial state of all the variable domains
        original_domains = list(csp.variable_values)

        if csp.is_consistent(assignment, value, var):
            # Run MAC
            mac = csp.mac(var, value)
            # print("     Domains: " + str(csp.variable_values) + "\n")
            if mac:
                result = backtrack_mac(assignment, csp)
                if result is not None:
                    return result

        # Restores the initial domains of the variables: ***COMMENT OUT IF NOT USING MRV***
        csp.variable_values = list(original_domains)

    # If no consistent value found for a variable, add it back to the unassigned variables set
    csp.replace_unassigned(var)

    return None