# create pull request to make changes

PC = 00000000
type_a = {"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100"}
type_c = {"div": "10111", "not": "11101", "cmp": "11110", "mov": "10011"} # mov r1 r2
type_e = {"jmp": "11111", "jlt": "01100", "je": "01111", "jgt": "01101"}
reg = {"r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110", "r7": "111"}
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
    lst1 = f.readlines()
    c = lst1.count("\n")
    for i in range(c):
        lst1.remove("\n")
    for i in range(len(lst1)):
        lst1[i] = " ".join(lst1[i].split())

    parse_vars(lst1, vars, PC, count)

    inst_lst = []
    for i in lst1:
        l = i.split()
        inst_lst.append(l)

for i in range(len(inst_lst)):
    if inst_lst[i][0].lower() in type_a:
        if len(inst_lst[i]) == 4:
            if inst_lst[i][1].lower() in reg and inst_lst[i][2].lower() in reg and inst_lst[i][3].lower() in reg:
                op = type_a[inst_lst[i][0]]
                r1 = reg[inst_lst[i][1].lower()]
                r2 = reg[inst_lst[i][2].lower()]
                r3 = reg[inst_lst[i][3].lower()]
                print(op+"00"+r1+r2+r3)
            else:
                print(f'Error in line: Undefined Register Name')
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inst_lst[i][0].lower() in type_c:
        if len(inst_lst[i]) == 3:
            if inst_lst[i][1].lower() in reg and inst_lst[i][2].lower() in reg:
                op = type_c[inst_lst[0]]
                r1 = reg[inst_lst[i][1].lower()]
                r2 = reg[inst_lst[i][2].lower()]
                print(op+"00000"+r1+r2)
            else:
                print(f'Error in line: Undefined Register Name')
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inst_lst[i][0].lower() in type_e:
        if len(inst_lst[i]) == 2:
            if len(inst_lst[i][1]) == 8:
                op = type_e[inst_lst[i][0]]
                print(op+"000"+inst_lst[i][1])
            ## condition to check if mem_addr is accessible n acceptable (?)
        else:
            print(f'Error in line: Wrong format of instruction')
    elif inst_lst[i][0].lower() == "hlt":
        print("0101000000000000")
