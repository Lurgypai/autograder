#!/bin/python3
# REQUIRES:
# frequency
# wordPairs
# Datasets/*

import subprocess
import os
import sys
import re

# flag for if we should print out the expected and received values when they're the same (for testing this script)
# this is set by adding the '-V' flag when running
verbose = False

#the max number of lines of output to print from running the tests
max_lines = 10

#parse args
if len(sys.argv) > 1:
    if sys.argv[1] == '-V':
        verbose = True

# runs a command and returns the whitespace stripped stdout, and regular stderr, both as an array of strings
def runCommand(exe, command):
    command = [exe] + command
    out = open('stdout', 'w+')
    err = open('stderr', 'w+')

    timeout = False
    try:
        res = subprocess.run(command, timeout=10, stdout=out, stderr=err)
    except Exception as e:
        print(e)
        timeout = True;
    out.seek(0)
    err.seek(0)

    output_lines = out.readlines()
    output_lines = [x.strip() for x in output_lines]
    return output_lines, err.readlines(), timeout

# checks if two lists contain the same elements (in any order)
def outputEqual(out1, out2):
    ben_counts = {}
    student_counts = {}

    for row in out1:
        if row == "":
            continue
        if not row[0].isnumeric():
            print("Found unkown line:", row)
            continue
        key = re.search(r'\d+', row).group(0)
        if not key in ben_counts:
            ben_counts[key] = []
        ben_counts[key] += [row]
    for row in out2:
        if row == "":
            continue
        if not row[0].isnumeric():
            print("Found unkown line:", row)
            continue
        key = re.search(r'\d+', row).group(0)
        if not key in student_counts:
            student_counts[key] = []
        student_counts[key] += [row]
    
    for key in student_counts:
        if not key in ben_counts:
            print("Student had count not in correct output:", key)
            return False
    for key in ben_counts:
        if not key in student_counts:
            print("Student missing count:", key)
            return False
        ben_rows = ben_counts[key]
        student_rows = student_counts[key]
        if set(student_rows) != set(ben_rows):
            return False
    return True

# these are parallel arrays of the command, and its grade point value
valid_commands = [\
        ['-5', 'Datasets/dracula.txt'],\
        ['-10', 'Datasets/dracula.txt'],\
        ['Datasets/dracula.txt'],\
        ['-10', 'Datasets/dracula.txt', 'Datasets/frankenstein.txt'],\
        ['-10', 'Datasets/dracula.txt', 'Datasets/frankenstein.txt', 'Datasets/gettysburg.txt', 'Datasets/mobydick.txt', 'Datasets/frankenstein.txt', 'Datasets/frankenstein.txt']]
valid_scores = [5, 5, 5, 5, 10]

debug_commands = [\
        ['-5', 'Datasets/dracula.txt'],\
        ['-10', 'Datasets/dracula.txt']]
debug_scores = [5, 5]

# valid_commands = debug_commands
# valid_scores = debug_scores

# parallel arrays of commands that should throw to stderr
invalid_commands = [\
        ['-10'],\
        ['-hello'],\
        ['-5', 'adsfasd'],\
        ['asdfasdsfa']]
invalid_scores = [5, 5, 5, 5]


# run each valid command, make sure the outputs are the same
print("<--------------------- Testing valid commands... --------------------->")
valid_score = 0
command_num = 0
for command in valid_commands:
    msg = "Testing: "
    for arg in command:
        msg += arg + " "
    print(msg)
    freq_out, freq_err, _ = runCommand("./frequency", command)
    stud_out, stud_err, timeout = runCommand("./pairsofwords", command)
    
    if timeout:
        print("Student's executable timed out.")
        continue

    if outputEqual(freq_out, stud_out):
        print("Success...")
        if verbose:
            print("Expected:")
            line_total = 0
            for line in freq_out:
                if line_total == max_lines:
                    print("\t...")
                    break
                print('\t' + line)
                line_total += 1
            print("Received:")
            line_total = 0
            for line in stud_out:
                if line_total == max_lines:
                    print("\t...")
                    break
                print('\t' + line)
                line_total += 1
        valid_score += valid_scores[command_num]
    else:
        print("Failed...")
        print("Expected:")
        line_total = 0
        for line in freq_out:
            if line_total == max_lines:
                print("\t...")
                break
            print('\t' + line)
            line_total += 1
        print("Received:")
        line_total = 0
        for line in stud_out:
            if line_total == max_lines:
                print("\t...")
                break
            print('\t' + line)
            line_total += 1

    command_num += 1

print("TOTAL for valid commands:", str(valid_score) + "/30")
print()

# run each invalid command, make sure they print to stderr
print("<--------------------- Testing invalid commands... --------------------->")
invalid_score = 0
command_num = 0
for command in invalid_commands:
    msg = "Testing: "
    for arg in command:
        msg += arg + " "
    print(msg)
    stud_out, stud_err, _ = runCommand("./pairsofwords", command)

    if len(stud_err) != 0:
        print("Error expected, stderr was:")
        for line in stud_err:
            print('\t' + line)
        invalid_score += invalid_scores[command_num]
    else:
        print("!!! Missing output to stderr !!!")
        if len(stud_out) != 0:
            print("stdout was:")
            for line in stud_out:
                print('\t' + line)
            invalid_score += invalid_scores[command_num]
        else:
            print("Missing any error output!")

    command_num += 1

print("TOTAL for invalid commands:", str(invalid_score) + "/20")
print()

# run all the valid commands again, using valgrind. Look for the line saying "everythings okay" If its not present, get concerned
def noMemLeaks():
    print("<--------------------- Testing valgrind on valid commands... --------------------->")
    for command in valid_commands:
        command = ["./pairsofwords"] + command
        msg = "Testing: "
        for arg in command:
            msg += arg + " "
        print(msg)
        stud_out, stud_err, timeout = runCommand("valgrind", command)
        if timeout:
            print("Students executable timed out when checking for memory leaks...")
            return True
        no_leaks = False
        for line in stud_err:
            if "no leaks are possible" in line:
                no_leaks = True
                break
        if not no_leaks:
            print("!!!!!!!!!!!!!!!!!!!!!!! LEAK FOUND: !!!!!!!!!!!!!!!!!!!!!!!")
            for line in stud_err:
                print('\t' + line, end = '')
            return False
    return True

no_leaks = noMemLeaks()
print()

print("<--------------------- SUMMARY --------------------->")
print("Valid score:", str(valid_score) + "/30")
print("Invalid score:", str(invalid_score) + "/20")
print("Memeory leaks?:", "None" if no_leaks else "Found memory leaks.")
print("FINAL-" + str(valid_score) + ", " + str(invalid_score) + ", " + str("0" if no_leaks else "1"))
