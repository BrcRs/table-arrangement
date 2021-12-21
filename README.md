# Table Arrangement Solver

## Introduction

At the last birthday party I attended, I was given the task to place guests to their seats around the table. This is quite a difficult task as you need to make sure everyone will have a good time during the party, which mainly depends on who they are seated next to. I thought "Why not make a solver for that problem so I won't have this issue ever again?". And here we are.

## What it is

This project allows you to define your own table arrangement problem thanks to an easy model format. The solver can then give you the optimal placement of your guests given the constraints you wrote in your problem definition file (extension .ta).

## How to install

You can do some

    clone https://github.com/BrcRs/table-arrangement.git

in the folder of your choice or do

    clone git@github.com:BrcRs/table-arrangement.git

or even download the zip file and decompress it wherever you want.

## How to use it

### Define a problem file

You first need to define your problem in a .ta file. An example of such a file is example.ta. To define your model, you need to give 4 things:
- Your guests
- The topology of the table
- The constraints
- The function to optimize

#### Defining guests

To define guests, you need to write

    guests:

somewhere so that the interpreter knows where to look for guests.
Then, you need to give your guests nicknames and names as follows:

    <four spaces or one tab><Nickname> <Name>

Example:

    guests:
        Bru Bruce
        Ma Marc
        Em Emilie

You can also ommit the name:

Example:

    guests:
        Bru
        Ma
        Em

#### Defining the topology

By topology, I mean who can talk to who at a given seat. For instance, take the following table:

        1   2   3   4   5   6   7
    0
                                    8
    10
        11  12  13  14  15  16  9

Each seat is given a number. From the seat 7, we can imagine that we can talk to 6, to 8, to 9 and to 16. However, it will be hard to talk to someone at seat 10, because they're so far away! This is what we want to define in the topology.

First, write

    topology:

somewhere, then you need to list adjacent seats, in the following fashion:

        <seat 1> <seat 2>

Example for 7:

        7 6
        7 8
        7 9
        7 16

> Note: you do not need to specify both 7 6 and 6 7. You can consider the topology as an undirected graph.

To represent the topology of the previous big table, we would have to write:

    topology: // Unoriented graph
        0 1
        0 2
        0 10
        0 11
        1 2
        1 10
        1 11
        1 12
        2 3
        2 11
        2 12
        2 13
        3 4
        3 12
        3 13
        3 14
        4 5
        4 13
        4 14
        4 15
        5 6
        5 14
        5 15
        5 16
        6 7
        6 8
        6 9
        6 15
        6 16
        7 8
        7 9
        7 16
        8 9
        8 16
        9 16
        10 11
        11 12
        12 13
        13 14
        14 15
        15 16

It's a bit tedious. Maybe in next versions we'll add more comprehensive ways to define the topology.

> Note: you can write comments with // comment and with /* comment */.
> Don't go too crazy with those though, as it is still a beta version.

#### Defining constraints

To each pair guest1 guest2, we want to set a value which is the satisfaction of guest1 if it is next to guest2.

> Note: contrary to the topology, constraints can be seen as a directed valued graph.

Write

    constraints:

somewhere, and then define the value of each pair. For instance, let's say Marc (Ma) loves to talk to Emilie (Em) but absolutely hates Bruce (Bru). We will model his preferences with the following constraints:

        Ma Em 10
        Ma Bru -50

However, Bruce (Bru) likes to talk to Marc (Ma):

        Bru Ma 5

You can also define constraints on seats. Let's say we have the following table again:

                     ######
        1   2   3   4   5   6   7
    0
                                    8
    10
        11  12  13  14  15  16  9

It appears that there is not much room between seat 5 and the wall behind it (represented by ### here). Bruce (Bru) is a pretty big guy, so it will be very uncomfortable for him to seat at 5. We can represent his preference with a constraint:

        Bru 5 -15

The constraints section thus looks like this:

    constraints:
        Ma Em 10 // constraint on guest
        Ma Bru -50
        Bru Ma 5
        Bru 5 -15 // constraint on seat

#### Defining the function to optimize

For now, you can evaluate a solution with two functions: the maxmin function and the maxsum function.

The maxmin function gives to a solution the minimum value of all guests as a quality value. The solver will try to find a solution in which the guest having the worst value has the best value possible (equity principle).

The maxsum function gives to a solution the sum of all guests' values as a quality value. The solver will try to maximize the average value of the guests, which can lead to having some guests neglicted for the common good.

To choose a function, write:

    problem:
        maxmin

or

    problem:
        maxsum

### Solve your problem

If your problem is well defined in your problem file, you can now ask the solver to solve it and give you a solution.

Two solving methods are available: the swap method and the bruteforce method.

The swap method begins by creating a random solution. Then it generates all neighboring solutions by swapping two adjacent guests. It keeps doing this until the value of the solution can't be increased. The swap method can reach local optima, so the returned solution is not always the optimum.

The bruteforce solution computes every permutation possible and takes the one with the maximum score. It is **really** slow and is used to test the swap method on small instances. The solution is always the optimum.

To solve your problem, write the following command in the terminal:

    python solver.py <my-problem-file>.ta

The program will first solve it with the swap method, then with the brute force method (for comparison). To skip the bruteforce method, just comment the relevant part in the main function of solver.py.

In the terminal, you will get something like this:

    python .\solver.py .\example2.ta
    Swap method
    {'a': {'seat': '3', 'value': 0.0}, 'b': {'seat': '1', 'value': 5.0}, 'c': {'seat': '5', 'value': 4.0}, 'd': {'seat': '4', 'value': 5.0}, 'e': {'seat': '2', 'value': 0}, 'f': {'seat': '0', 'value': 0}, 'g': 
    {'seat': '6', 'value': 0}, 'h': {'seat': '7', 'value': 0}}
    0.0
    Brute force
    {'a': {'seat': '0', 'value': 4.0}, 'b': {'seat': '1', 'value': 5.0}, 'c': {'seat': '3', 'value': 4.0}, 'd': {'seat': '4', 'value': 5.0}, 'e': {'seat': '2', 'value': 0}, 'f': {'seat': '5', 'value': 0}, 'g': 
    {'seat': '6', 'value': 0}, 'h': {'seat': '7', 'value': 0}}
    0

For each method, it gives you the name, then a dictionary mapping to each guest its seat and its satisfaction score at the given seat. Under that, it gives you the score of the solution found.