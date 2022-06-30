def parse_vars(lst, vars_dict, PC):
    for i in lst:
        if "var" not in i.lower():
            PC+=1
        else:
            vars_dict[f'var {count}'] = i[4]


PC = 00000000
type_a = {"add": "10000", "mul": "10110"}
type_c = {"div": "10111"}
type_e = {"jmp": "11111", "jlt": "01100"}
reg = {"r1": "000", "r2": "001", "r3": "010", "r4":"011"}
vars = {}
count = 0


with open('trial.txt') as f:
    inp = f.readlines()
    c = inp.count("\n")
    for i in range(c):
        inp.remove("\n")
    for i in range(len(inp)):
        inp[i] = " ".join(inp[i].split())

    # parse_vars(inp, vars, PC)

    new = []
    for i in inp:
        l = i.split()
        new.append(l)
    print(new)

    if type_a not in i and type_c not in i and type_e not in i and "var" not in i:
        print(f'Error in line: Undefined Instruction Name')
    elif inp[0].lower() in type_a:
        if len(inp) == 4:
            if inp[1].lower() in reg and inp[2].lower() in reg and inp[3].lower() in reg:
                op = type_a[inp[0]]
                r1 = reg[inp[1].lower()]
                r2 = reg[inp[2].lower()]
                r3 = reg[inp[3].lower()]
                print(op+"00"+r1+r2+r3)
            else:
                print(f'Error in line: Undefined Register Name')
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inp[0].lower() in type_c:
        if len(inp) == 3:
            if inp[1].lower() in reg and inp[2].lower() in reg:
                op = type_c[inp[0]]
                r1 = reg[inp[1].lower()]
                r2 = reg[inp[2].lower()]
                print(op+"00000"+r1+r2)
            else:
                print(f'Error in line: Undefined Register Name')
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inp[0].lower() in type_e:
        if len(inp) == 2:
            if len(inp[1]) == 8:
                op = type_e[inp[0]]
                print(op+"000"+inp[1])
            ## condition to check if mem_addr is accessible n acceptable (?)
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inp[0].lower() == "hlt":
        print("0101000000000000")
