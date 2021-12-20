from table_arrangement import TAProblem
import string
import sys

def load_problem(filename):
    if filename[-3:] != ".ta":
        raise NameError("The file is not a .ta file")
    f = open(filename, "r")
    problem = TAProblem()
    aliases = dict()
    nline = 0
    # for each line:
    line = f.readline()
    while line:
        # if it begins with guests:
        if line[:len("guests:")] == "guests:":
            line = f.readline()
            nline += 1
            # while the line begins with \t or \n:
            while line:
                if len(line) == 0:
                    line = f.readline()
                    nline += 1
                    continue
                if line[0] != "\t":
                    break
                # parse the line with \t then blank
                parsed_line = line.split("\t")
                parsed_line = parsed_line[1].split(" ")
                # get alias (first value) as identifier for names 
                # (second value)
                k = parsed_line[0]
                # make sure it doesn't begin with a number
                if k[0] in string.digits:
                    raise SyntaxError("Guests names can't begin with a number")
                aliases[k] = parsed_line[1]
                
                # check for syntax errors
                
                line = f.readline()
                nline += 1
            # Add guests to problem
            problem.add_guests(aliases)

        # if it begins with /*:
        elif line[:2] == "/*":
            line = f.readline()
            nline += 1
            # pass lines until */ is found
            while line and not "*/" in line:
                line = f.readline() # Caution: lines with */ will be ignored?
                nline += 1
        # if it begins with //:
        elif line[:2] == "//":
            # pass
            continue

        # if it begins with blank:
        elif line[0] == " ":
            # throw syntax error
            raise SyntaxError("Lonely blank on line " + str(nline))

        # if it begins with topology:
        elif line[:len("topology:")] == "topology:":
            line = f.readline()
            nline += 1
            # while the line begins by \t or \n:
            while line:

                if len(line) == 0:
                    line = f.readline()
                    nline += 1
                    continue

                if line[0] != "\t":
                    break

                # parse with \t then blank
                parsed_line = line.split("\t")
                parsed_line = parsed_line[1].split(" ")

                # add edge(first value, second value) to the graph
                problem.add_edge(parsed_line[0], parsed_line[1])

        # if it begins with constraints:
        elif line[:len("constraints:")] == "constraints:":
            line = f.readline()
            nline += 1

            # while the line begins by \t or \n:
            while line:

                if len(line) == 0:
                    line = f.readline()
                    nline += 1
                    continue

                if line[0] != "\t":
                    break

                # parse with \t then blank
                parsed_line = line.split("\t")
                parsed_line = parsed_line[1].split(" ")
                # add third value to the key: second value for first value
                # constraints
                if parsed_line[1][0] in string.digits:
                    guest = parsed_line[0]
                    seat = parsed_line[1]
                    value = float(parsed_line[2])
                    problem.add_topo_constraint(guest, seat, value)
                else:
                    guest = parsed_line[0]
                    guest2 = parsed_line[1]
                    value = float(parsed_line[2])
                    problem.add_guest_constraint(guest, guest2, value)
        # if it begins with problem:
        elif line[:len("problem:")] == "problem:":
            line = f.readline()
            nline += 1

            # while the line begins by \t or \n:
            while line:

                if len(line) == 0:
                    line = f.readline()
                    nline += 1
                    continue

                if line[0] != "\t":
                    break

                # parse with \t then blank
                parsed_line = line.split("\t")
                parsed_line = parsed_line[1].split(" ")
                if not parsed_line[0] in TAProblem.types:
                    raise ValueError("Unknown problem type: " + parsed_line[0])
                problem.set_opt_function(parsed_line[0])
                break
        # else
        else:
            # throw syntax error
            raise SyntaxError()
        # line = f.readline()
    return problem

def main():
    print(sys.argv)
    problem = load_problem(sys.argv[1])
if __name__ == "__main__":
    main()
