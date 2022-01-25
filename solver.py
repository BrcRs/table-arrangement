from random import shuffle
from utility import is_number, copy_dict
import sys
from interpreter import load_problem
import itertools

def encode_solution(solution):
    value = [(g, solution[g]["seat"], solution[g]["value"]) for g in solution.keys()]
    value.sort(key= lambda x: x[0])
    value = str(value)
    value = hash(value)
    return value

assert encode_solution({"1" : {"seat":0, "value":100}, "2" : {"seat":5, "value":16}}) \
     == encode_solution({"2" : {"value":16, "seat":5}, "1" : {"seat":0, "value":100}})

def eval_guest(problem, solution, seat_to_guest, g):
    # print("Evalutating", g, file=open(problem.name + ".log", "a"))
    prev_value = solution[g]["value"] if "value" in solution[g].keys() else 0
    solution[g]["value"] = 0

    # review each constraint of guest g
    for c in problem.constraints[g].keys():
        # seat constraint
        seat_cond = is_number(c) and solution[g]["seat"] == c

        # guest constraint
        # if the guest is in neighbors
        nearby_guests = [seat_to_guest[s] for s in problem.topology[solution[g]["seat"]]]
        guest_cond = c in nearby_guests
        if seat_cond or guest_cond:
            # print("Adding", problem.constraints[g][c], "to", g, "'s value", file=open(problem.name + ".log", "a"))
            # print("Reason: constraint on", c, file=open(problem.name + ".log", "a"))
            solution[g]["value"] += problem.constraints[g][c]
        assert (type(solution[g]["value"]) != type(None))
    # print("\tvalue updated for", g, "to", solution[g]["value"], file=open(problem.name + ".log", "a"))

def is_feasible(problem, solution):
    for g in solution.keys():
        for o in problem.abs_constraints[g].keys():
            # o is a seat
            if is_number(o):
                if problem.abs_constraints[g][o] == 'N':
                    if solution[g]['seat'] == int(o):
                        # Constraint violated
                        return False
                elif problem.abs_constraints[g][o] == 'Y':
                    if solution[g]['seat'] != int(o):
                        # Constraint violated
                        return False
            # o is a guest
            else:
                # get neighbors' seats
                neigh_seats = problem.topology[solution[g]['seat']]

                # get neigbors
                neigh = [k for k in solution.keys() if solution[k]['seat'] in neigh_seats]
                if problem.abs_constraints[g][o] == 'N':
                    if o in neigh:
                        return False
                elif problem.abs_constraints[g][o] == 'Y':
                    if o not in neigh:
                        return False
    return True
def eval(problem, solution):
    # print("Evaluating the solution", solution, file=open(problem.name + ".log", "a"))
    # print("Function:", problem.function, file=open(problem.name + ".log", "a"))
    sol_val = 0
    if problem.function == "maxmin":
        sol_val = min([solution[g]["value"] for g in problem.guests.keys()])
    elif problem.function == "maxsum":
        sol_val = sum([solution[g]["value"] for g in problem.guests.keys()])
    # print("Value of solution:", sol_val, file=open(problem.name + ".log", "a"))
    return sol_val

def full_eval(problem, solution):
    # print("Full evaluation of solution", solution, file=open(problem.name + ".log", "a"))
    seat_to_guest = dict()
    for k in solution.keys():
        seat_to_guest[solution[k]["seat"]] = k
    # compute values of guests
    for g in problem.guests.keys():
        eval_guest(problem, solution, seat_to_guest, g)

    # compute value of solution
    sol_val = eval(problem, solution)
    return sol_val

def swap(problem, g1, g2, sol, seat_to_guest):
    # print("swap", g1, "and", g2, file=open(problem.name + ".log", "a"))
    assert g1 != g2
    old_g1_seat = sol[g1]['seat']
    # print(g1, "was at", old_g1_seat, file=open(problem.name + ".log", "a"))
    assert seat_to_guest[old_g1_seat] == g1
    # print(g2, "was at", sol[g2]['seat'], file=open(problem.name + ".log", "a"))
    sol[g1]['seat'] = sol[g2]['seat']
    # print(g1, "is now at", sol[g1]['seat'], file=open(problem.name + ".log", "a"))
    seat_to_guest[sol[g2]['seat']] = g1

    sol[g2]['seat'] = old_g1_seat
    # print(g2, "is now at", old_g1_seat, file=open(problem.name + ".log", "a"))

    seat_to_guest[old_g1_seat] = g2


def neighbors(problem, solution, seat_to_guest):
    neighs = dict()
    swapped_people = []
    # for each guest, add each solution where it is swaped with a neighbor
    # for each neighbor it has
    # print("For each guest", file=open(problem.name + ".log", "a"))
    for g in problem.guests.keys():
        # print("Guest", g, file=open(problem.name + ".log", "a"))
        # print("For each adjacent position", file=open(problem.name + ".log", "a"))
        for n in problem.topology[solution[g]['seat']]:
            # print("Position", n, file=open(problem.name + ".log", "a"))
            sol_copy = copy_dict(solution)
            s_to_g_copy = copy_dict(seat_to_guest)
            g2 = seat_to_guest[n]
            if (g, g2) in swapped_people or (g2, g) in swapped_people:
                # print((g, g2), "already in", swapped_people, file=open(problem.name + ".log", "a"))
                continue
            swapped_people.append((g, g2)) 
            # swap g and the guest at n in a copy of solution
            # swap g and the guest at n in a copy of seat_to_guest
            swap(problem, g, g2, sol_copy, s_to_g_copy)
            # add the couple to neighs and the value (if not in already!)
            sol_id = encode_solution(sol_copy)
            if is_feasible(problem, sol_copy):
                neighs[sol_id] = (sol_copy, s_to_g_copy, full_eval(problem, sol_copy))
    return neighs

def solve(problem, logfile="swap.log"):
    # f = open(logfile, 'w')
    # print("", file=f)
    # f.close()
    solution = dict()
    seat_to_guest = dict()
    sol_val = 0
    # initialize everyone to random seats
    seats = [k for k in problem.topology.keys()]
    # print("Randomizing seats", file=open(logfile, "a"))
    shuffle(seats)
    i = 0
    for a in problem.guests.keys():
        solution[a] = {"seat" : seats[i]}
        seat_to_guest[seats[i]] = a
        i += 1
    while not is_feasible(problem, solution):
        solution = dict()
        seat_to_guest = dict()
        shuffle(seats)
        i = 0
        for a in problem.guests.keys():
            solution[a] = {"seat" : seats[i]}
            seat_to_guest[seats[i]] = a
            i += 1

    # compute values of guests
    # print("initial value computing", file=open(logfile, "a"))
    for g in problem.guests.keys():
        eval_guest(problem, solution, seat_to_guest, g)
    # print("end initial value computing", file=open(logfile, "a"))
    # compute value of solution
    sol_val = eval(problem, solution)

    # then add to the front every neighboring instance
    # compute the score of every neighboring instance
    front = neighbors(problem, solution, seat_to_guest)
    # print("Initial front of size", len(front),":", front, file=open(logfile, "a"))
    # init done, start loop

    # get best value in neighbors
    if len(front) == 0:
        return solution, sol_val
    best = max(front.keys(), key=lambda k: front[k][2])
    best_value = front[best][2]
    # print("best value found in front:", best_value, file=open(logfile, "a"))
    # if there is no best one, return current solution
    while best_value > sol_val:
        # print("best value is better, exploring new node", file=open(logfile, "a"))
        # go to the best one found
        solution, seat_to_guest, sol_val = front[best]
        
        # remove best solution from front
        del front[best]

        # then add to the front every neighboring instance
        # compute the score of every neighboring instance
        neighs = neighbors(problem, solution, seat_to_guest)
        for k in neighs.keys():
            if not k in front.keys():
                front[k] = neighs[k]

        # get best value in front
        best = max(front.keys(), key=lambda k: front[k][2])
        best_value = front[best][2]
        # print("best value found in front:", best_value, file=open(logfile, "a"))

    return solution, sol_val

def solve_bruteforce(problem, logfile="bruteforce.log"):
    best = dict()
    best_val = None
    seats = [k for k in problem.topology.keys()]
    all_seats = itertools.permutations(seats)
    for bunch_of_seats in all_seats:
        solution = dict()
        seat_to_guest = dict()
        i = 0
        for a in problem.guests.keys():
            solution[a] = {"seat" : bunch_of_seats[i]}
            seat_to_guest[bunch_of_seats[i]] = a
            i += 1
        if is_feasible(problem, solution):
            # compute values of guests
            for g in problem.guests.keys():
                eval_guest(problem, solution, seat_to_guest, g)

            # compute value of solution
            sol_val = eval(problem, solution)
            if best_val == None or sol_val > best_val:
                best_val = sol_val
                best = copy_dict(solution)

    return best, best_val


def main():
    print(sys.argv)
    problem = load_problem(sys.argv[1])

    print("Swap method")
    solution, sol_val = solve(problem, logfile="swap_" + sys.argv[1] + ".log")
    print(solution)
    print(sol_val)
    assert full_eval(problem, solution) == sol_val, str(full_eval(problem, solution)) + " != " + str(sol_val)

    print("Brute force")
    brute_sol, brute_val = solve_bruteforce(problem, logfile="bruteforce_" + sys.argv[1] + ".log")
    print(brute_sol)
    print(brute_val)
    assert full_eval(problem, brute_sol) == brute_val, str(full_eval(problem, brute_sol)) + " != " + str(brute_val)

if __name__ == "__main__":
    main()