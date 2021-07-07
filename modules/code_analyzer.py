#!/usr/bin/env python3
import os

def name():
    return "code_analyzer"

def help():
    return "Usage: ./bladestorm.py code_analyzer <directory>"

def args():
    return ["directory"]

def run(args):

    dir = (args.directory)
    c_dangerous_functions = [
        # Overflow: https://github.com/Naetw/CTF-pwn-tips
        "scanf", "gets", "read", "strcpy",
        "strcat", "strcmp", "memcpy",
        # Format string: https://owasp.org/www-community/attacks/Format_string_attack
        "fprint", "printf", "sprintf", "snprintf",
        "vfprintf", "vprintf", "vsprintf", "vsnprintf",
        # Command execution: https://linux.die.net/man/3/exec
        "system", "execl", "execlp", "execle",
        "execv", "execvp", "execvpe", "shell_exec",
        # Linux permission
        "chown", "chgrp", "chmod",
    ]

    try:
        for folder, dirs, files in os.walk(dir):
            for file in files:
                if file.endswith(".c"):
                    path = os.path.join(folder, file)
                    with open(path, "r") as fhand:
                        for line in fhand:
                            for c_dangerous_function in c_dangerous_functions:
                                if c_dangerous_function in line:
                                    print(f"{path} contains dangerous function {c_dangerous_function}")
                                    break
    except:
        print("Code analysis failed.")