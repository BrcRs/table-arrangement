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

By topology, I mean who can talk to who at a given seat. take the following table:

                    |    ||          ||
        1   2   3   4   5   6   7
    0
                                    8
    10
        11  12  13  14  15  16  9
                    |

Each seat is given a number. From the seat 7, we can imagine that we can talk to 6, to 8, to 9 and to 16. However, it will be hard to talk to someone at seat 10, because they're so far away! This is what we want to define in the topology.

First, write

    topology:

somewhere, then you need to list adjacent seats, in the following fashion:

    <seat 1><seat 2>

Example, with the previous example with 7:

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

It's a big tedious. Maybe in next versions we'll add more comprehensive ways to define the topology.