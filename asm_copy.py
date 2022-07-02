# make changes in this file

PC = 00000000
type_a = {"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100", }
type_c = {"div": "10111"}
type_e = {"jmp": "11111", "jlt": "01100"}
reg = {"r1": "000", "r2": "001", "r3": "010", "r4":"011"}
vars = {}
labels = {} # with line number where labels come
count = 0


def parse_vars(lst, vars_dict, PC, count):
    for i in lst:
        if "var" not in i.lower():
            PC+=1
        else:
            vars_dict[f'var {count}'] = i[4]
            count+=1


with open('trial.txt') as f:
    new = f.readlines()
    c = new.count("\n")
    for i in range(c):
        new.remove("\n")
    for i in range(len(new)):
        new[i] = " ".join(new[i].split())

    parse_vars(new, vars, PC, count)

    inp = []
    for i in new:
        l = i.split()
        inp.append(l)

for i in range(len(inp)):
    if inp[i][0].lower() in type_a:
        if len(inp[i]) == 4:
            if inp[i][1].lower() in reg and inp[i][2].lower() in reg and inp[i][3].lower() in reg:
                op = type_a[inp[i][0]]
                r1 = reg[inp[i][1].lower()]
                r2 = reg[inp[i][2].lower()]
                r3 = reg[inp[i][3].lower()]
                print(op+"00"+r1+r2+r3)
            else:
                print(f'Error in line: Undefined Register Name')
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inp[i][0].lower() in type_c:
        if len(inp[i]) == 3:
            if inp[i][1].lower() in reg and inp[i][2].lower() in reg:
                op = type_c[inp[0]]
                r1 = reg[inp[i][1].lower()]
                r2 = reg[inp[i][2].lower()]
                print(op+"00000"+r1+r2)
            else:
                print(f'Error in line: Undefined Register Name')
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inp[i][0].lower() in type_e:
        if len(inp[i]) == 2:
            if len(inp[i][1]) == 8:
                op = type_e[inp[i][0]]
                print(op+"000"+inp[i][1])
            ## condition to check if mem_addr is accessible n acceptable (?)
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inp[i][0].lower() == "hlt":
        print("0101000000000000")
