import sys


file_path = sys.argv[1]

program_lines = []
with open(file_path, 'r') as file:
    program_lines = [line.strip() for line in file.readlines()]

program = []
token_counter = 0
label_tracker = {}

for line in program_lines:
    parts = line.split(" ")
    opcode = parts[0]

    if opcode == "":
        continue

    if opcode.endswith(":"):
        label_tracker[opcode[:-1]] = token_counter
        continue

    program.append(opcode)
    token_counter += 1

    if opcode == "PUSH":
        number = int(parts[1])
        program.append(number)
        token_counter += 1
    elif opcode == "PRINT":
        string_literal = " ".join(parts[1:])[1:-1]
        program.append(string_literal)
        token_counter += 1
    elif opcode == "JUMP.EQ.0":
        label = parts[1]
        program.append(label)
        token_counter += 1
    elif opcode == "JUMP.GT.0":
        label = parts[1]
        program.append(label)
        token_counter += 1

class Stack():
    def __init__(self, size):
        self.buf = [0 for _ in range(size)]
        self.sp = -1

    def push(self, number):
        self.sp += 1
        self.buf[self.sp] = number

    def pop(self):
        number = self.buf[self.sp]
        self.sp -= 1
        return number

    def top(self):
        return self.buf[self.sp]

pc = 0
stack = Stack(256)

while program[pc] != 'HALT':
    opcode = program[pc]
    pc += 1

    if opcode == "PUSH":
        number = program[pc]
        stack.push(number)
        pc += 1
    elif opcode == "POP":
        stack.pop()
    elif opcode == "ADD":
        a = stack.pop()
        b = stack.pop()
        stack.push(a + b)
    elif opcode == "SUB":
        a = stack.pop()
        b = stack.pop()
        stack.push(b - a)
    elif opcode == "READ":
        number = int(input())
        stack.push(number)
    elif opcode == "PRINT":
        string_literal = program[pc]
        print(string_literal)
        pc += 1
    elif opcode == "JUMP.EQ.0":
        label = program[pc]
        if stack.top() == 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    elif opcode == "JUMP.GT.0":
        label = program[pc]
        if stack.top() > 0:
            pc = label_tracker[program[pc]]
        else:
            pc += 1
    elif opcode == "HALT":
        break
    else:
        pc += 1