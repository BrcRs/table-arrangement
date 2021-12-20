from random import shuffle
from utility import is_number

def eval(problem, solution):
    sol_val = 0
    for g in problem.guests.keys():
        solution[g]["value"] = 0     

        # review each constraint of guest g
        for c in problem.constraints[g].keys():
            # seat constraint
            seat_cond = is_number(c) and solution[g]["seat"] == c

            # guest constraint
            # if the guest is in neighbors
            guest_cond = c in problem.topology[solution[g]["seat"]]
            if seat_cond or guest_cond:
                solution[g]["value"] += problem.constraints[g][c]
    if problem.function == "maxmin":
        sol_val = min([solution[g]["value"] for g in problem.guests.keys()])
    elif problem.function == "maxsum":
        sol_val = sum([solution[g]["value"] for g in problem.guests.keys()])
    return sol_val

def solve(problem):
    solution = dict()
    sol_val = 0
    # initialize everyone to random seats
    seats = problem.topology.keys().copy()
    seats.shuffle()
    i = 0
    for a in problem.guests.keys():
        solution[a] = {"seat" : seats[i]}
        i += 1
    # compute value of solution
    sol_val = eval(problem, solution)
    
    front = problem.neighbors()
    # then add to the front every neighboring instance
    # compute the score of every neighboring instance
    # go to the best one found
    # repeat
    # if there is no best one, return current solution