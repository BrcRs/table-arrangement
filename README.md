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
