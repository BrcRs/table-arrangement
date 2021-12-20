from random import shuffle
from utility import is_number, copy_dict
import sys
from interpreter import load_problem

def encode_solution(solution):
    value = [(g, solution[g]["seat"], solution[g]["value"]) for g in solution.keys()]
    value.sort(key= lambda x: x[0])
    value = str(value)
    value = hash(value)
    return value

assert encode_solution({"1" : {"seat":0, "value":100}, "2" : {"seat":5, "value":16}}) \
     == encode_solution({"2" : {"value":16, "seat":5}, "1" : {"seat":0, "value":100}})

def eval_guest(problem, solution, seat_to_guest, g):
    solution[g]["value"] = 0
    # print("for", g)
    # print(problem.constraints[g])

    # review each constraint of guest g
    for c in problem.constraints[g].keys():
        # print("c:", c)
        # seat constraint
        seat_cond = is_number(c) and solution[g]["seat"] == c

        # guest constraint
        # if the guest is in neighbors
        nearby_guests = [seat_to_guest[s] for s in problem.topology[solution[g]["seat"]]]
        guest_cond = c in nearby_guests
        # print("seat_cond", seat_cond)
        # print("guest_cond", guest_cond)
        # print(g, "is at", solution[g]["seat"])
        if seat_cond or guest_cond:
            solution[g]["value"] += problem.constraints[g][c]
        # print(g, "value is", solution[g]["value"])
        assert (type(solution[g]["value"]) != type(None))

def eval(problem, solution):
    sol_val = 0
    if problem.function == "maxmin":
        # print([solution[g]["value"] for g in problem.guests.keys()])
        sol_val = min([solution[g]["value"] for g in problem.guests.keys()])
    elif problem.function == "maxsum":
        sol_val = sum([solution[g]["value"] for g in problem.guests.keys()])
    return sol_val

def swap(problem, g1, g2, sol, seat_to_guest):
    assert g1 != g2
    # print("swap", g1, "and", g2)
    # print("previous seat_to_guest", seat_to_guest)
    old_g1_seat = sol[g1]['seat']
    # print("old_g1_seat", old_g1_seat)
    assert seat_to_guest[old_g1_seat] == g1

    sol[g1]['seat'] = sol[g2]['seat']
    eval_guest(problem, sol, seat_to_guest, g1)
    # print("map", sol[g2]['seat'], "to", g1)
    seat_to_guest[sol[g2]['seat']] = g1

    sol[g2]['seat'] = old_g1_seat
    eval_guest(problem, sol, seat_to_guest, g2)

    # print("map", old_g1_seat, "to", g2)
    seat_to_guest[old_g1_seat] = g2
    # print("now seat_to_guest", seat_to_guest)

def neighbors(problem, solution, seat_to_guest):
    neighs = dict()
    swapped_people = []
    # for each guest, add each solution where it is swaped with a neighbor
    # for each neighbor it has
    for g in problem.guests.keys():
        for n in problem.topology[solution[g]['seat']]:
            # print("solution[g]['seat']", solution[g]['seat'])
            # print("problem.topology[solution[g]['seat']]", problem.topology[solution[g]['seat']])
            sol_copy = copy_dict(solution)
            s_to_g_copy = copy_dict(seat_to_guest)
            g2 = seat_to_guest[n]
            # print("seat_to_guest", seat_to_guest)
            # print("n", n)
            # print("g", g)
            # print("g2", g2)
            if (g, g2) in swapped_people or (g2, g) in swapped_people:
               continue
            swapped_people.append((g, g2)) 
            # swap g and the guest at n in a copy of solution
            # swap g and the guest at n in a copy of seat_to_guest
            # print("swap", g, g2)
            swap(problem, g, g2, sol_copy, s_to_g_copy)
            # add the couple to neighs and the value (if not in already!)
            sol_id = encode_solution(sol_copy)
            # print("L71", sol_copy)
            neighs[sol_id] = (sol_copy, s_to_g_copy, eval(problem, sol_copy))
    return neighs

def solve(problem):
    solution = dict()
    seat_to_guest = dict()
    sol_val = 0
    # initialize everyone to random seats
    seats = [k for k in problem.topology.keys()]
    shuffle(seats)
    i = 0
    for a in problem.guests.keys():
        solution[a] = {"seat" : seats[i]}
        seat_to_guest[seats[i]] = a
        i += 1

    # compute values of guests
    for g in problem.guests.keys():
        eval_guest(problem, solution, seat_to_guest, g)

    # compute value of solution
    sol_val = eval(problem, solution)

    # then add to the front every neighboring instance
    # compute the score of every neighboring instance
    front = neighbors(problem, solution, seat_to_guest)
    # init done, start loop

    # get best value in neighbors
    best = max(front.keys(), key=lambda k: front[k][2])
    best_value = front[best][2]
    print("best value", best_value)
    print("front")
    print([front[k][2] for k in front.keys()])
    # if there is no best one, return current solution
    while best_value > sol_val:
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
    return solution, sol_val
def main():
    print(sys.argv)
    problem = load_problem(sys.argv[1])
    solution, sol_val = solve(problem)
    print(solution)
    print(sol_val)

if __name__ == "__main__":
    main()