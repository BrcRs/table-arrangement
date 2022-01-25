from table_arrangement import TAProblem
import string
import sys
from utility import is_number
def load_problem(filename):
    if filename[-3:] != ".ta":
        raise NameError("The file is not a .ta file")
    f = open(filename, "r")
    problem = TAProblem()
    aliases = dict()
    nline = 1
    # for each line:
    line = f.readline()
    while line:
        # if it begins with guests:
        if line[:len("guests:")] == "guests:":
            line = f.readline()
            nline += 1
            # while the line begins with \t or \n:
            while line:
                if len(line) == 0 or line[0] == "\n":
                    line = f.readline()
                    nline += 1
                    continue
                if line[:4] != " "*4:
                    break
                # parse the line with \t then blank
                parsed_line = line.split(" "*4)
                parsed_line = parsed_line[1].split(" ")
                # get alias (first value) as identifier for names 
                # (second value)
                k = parsed_line[0].replace("\n", "")
                # make sure it doesn't begin with a number
                if k[0] in string.digits:
                    raise SyntaxError("Guests names can't begin with a number")
                if len(parsed_line) <= 1:
                    aliases[k] = k
                else:
                    aliases[k] = parsed_line[1].replace("\n", "")
                
                # check for syntax errors
                
                line = f.readline()
                nline += 1
            # Add guests to problem
            problem.add_guests(aliases)

        # if it begins with /*:
        elif line[:2] == "/*":
            # print("Found /* on line " + str(nline))
            line = f.readline()
            nline += 1
            # pass lines until */ is found
            while line and not "*/" in line:
                # print("Line " + str(nline))
                line = f.readline() # Caution: lines with */ will be ignored?
                nline += 1
            line = f.readline()
            nline += 1
        # if it begins with //:
        elif line[:2] == "//" or line[0] == "\n":
            # pass
            line = f.readline()
            nline += 1
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

                if len(line) == 0 or line[0] == "\n":
                    line = f.readline()
                    nline += 1
                    continue

                if line[:4] != " "*4:
                    break

                # parse with \t then blank
                parsed_line = line.split(" "*4)
                parsed_line = parsed_line[1].split(" ")
                for i in [0, 1]:
                    if not is_number(parsed_line[i]):
                        raise ValueError("Seats should be numbers, got " + parsed_line[i] + " instead")
                # add edge(first value, second value) to the graph
                problem.add_edge(parsed_line[0].replace("\n", ""), parsed_line[1].replace("\n", ""))
                line = f.readline()
                nline += 1
        # if it begins with constraints:
        elif line[:len("constraints:")] == "constraints:":
            # print("Found constraints section on line " + str(nline))
            line = f.readline()
            nline += 1

            # while the line begins by \t or \n:
            while line:
                # print("Line " + str(nline))
                if line[:2] == "//":
                    line = f.readline()
                    nline += 1
                    continue
                if len(line) == 0 or line[0] == "\n":
                    line = f.readline()
                    nline += 1
                    continue

                if line[:4] != " "*4:
                    # print("[115] Exit of constraints on line", nline)
                    # print(len(line))
                    # print("\"" + line + "\"")
                    break

                # parse with \t then blank
                parsed_line = line.split(" "*4)
                parsed_line = parsed_line[1].split(" ")
                # add third value to the key: second value for first value
                # constraints
                # print("line", nline)
                guest = parsed_line[0].replace("\n", "")
                other = parsed_line[1].replace("\n", "")


                value = parsed_line[2].replace("\n", "")
                if value in ['N', 'Y']:
                    problem.add_absolute_constraint(guest, other, value)
                else:
                    value = float(parsed_line[2].replace("\n", ""))
                    problem.add_constraint(guest, other, value)


                line = f.readline()
                nline += 1
            # print("[129] Exit of constraints on line", nline)

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

                if line[:4] != " "*4:
                    break

                # parse with \t then blank
                parsed_line = line.split(" "*4)
                parsed_line = parsed_line[1].split(" ")
                if not parsed_line[0] in TAProblem.types:
                    raise ValueError("Unknown problem type: " + parsed_line[0])
                problem.set_opt_function(parsed_line[0])
                line = f.readline()
                nline += 1
                break
        # else
        else:
            # throw syntax error
            raise SyntaxError("Unable to read line " + str(nline) + " of length "+ str(len(line)) +" :\n\"" + line + "\"")
        # line = f.readline()
    f.close()
    return problem

def main():
    print(sys.argv)
    problem = load_problem(sys.argv[1])
    print("guests", problem.guests)
    print("topology", problem.topology)
    print("constraints", problem.constraints)
    print("function", problem.function)
if __name__ == "__main__":
    main()
