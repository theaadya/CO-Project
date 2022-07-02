# make changes in this file

PC = 00000000
type_a = {"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100"}
type_c = {"div": "10111", "not": "11101", "cmp": "11110", "mov": "10011"} # mov r1 r2
type_e = {"jmp": "11111", "jlt": "01100", "je": "01111", "jgt": "01101"}
reg = {"r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110", "r7": "111"}
vars = {}
labels = {} # with line number where labels come
machine_code = []
line_nums = []
count = 0
flag = False

def parse_vars(lst, vars_dict, PC, count):
    for i in lst:
        if "var" not in i.lower():
            PC+=1
        else:
            vars_dict[f'var {count}'] = i[4]
            count+=1


with open('trial.txt') as f:
    lst1 = f.readlines()
    for i in range(len(lst1)):
        if lst1[i] != "\n":
            line_nums.append(i)
    c = lst1.count("\n")
    for i in range(c):
        lst1.remove("\n")
    for i in range(len(lst1)):
        lst1[i] = " ".join(lst1[i].split())

    parse_vars(lst1, vars, PC, count)

    inst_lst = []
    idx = 0
    for i in lst1:
        l = i.split()
        inst_lst.append(l)
        l.insert(0, line_nums[idx]+1)
        idx += 1

if len(inst_lst[-1]) != 2 or inst_lst[-1][1] != "hlt":
    print("Absent/Invalid hlt declaration")
    flag = True

if flag == False:
    for i in range(len(inst_lst)):

        if inst_lst[i][1].lower() in type_a:
            if len(inst_lst[i]) == 5:
                if inst_lst[i][2].lower() in reg and inst_lst[i][3].lower() in reg and inst_lst[i][4].lower() in reg:
                    op = type_a[inst_lst[i][1]]
                    r1 = reg[inst_lst[i][2].lower()]
                    r2 = reg[inst_lst[i][3].lower()]
                    r3 = reg[inst_lst[i][4].lower()]
                    machine_code.append(op+"00"+r1+r2+r3)
                else:
                    with open("output.txt", "a") as f:
                        f.write(f'Error in line: Undefined Register Name')
                        flag = True
            else:
                print(f'Error in line: Wrong format of instruction')
                flag = True

        elif inst_lst[i][1].lower() in type_c:
            if len(inst_lst[i]) == 4:
                if inst_lst[i][2].lower() in reg and inst_lst[i][3].lower() in reg:
                    op = type_c[inst_lst[1]]
                    r1 = reg[inst_lst[i][2].lower()]
                    r2 = reg[inst_lst[i][3].lower()]
                    machine_code.append(op+"00000"+r1+r2)
                else:
                    with open("output.txt", "a") as f:
                        print(f'Error in line: Undefined Register Name')
                        flag = True
            else:
                with open("output.txt", "a") as f:
                    print(f'Error in line: Wrong format of instruction')
                    flag = True

        elif inst_lst[i][1].lower() in type_e:
            if len(inst_lst[i]) == 3:
                if len(inst_lst[i][2]) == 8:
                    op = type_e[inst_lst[i][1]]
                    machine_code.append(op+"000"+inst_lst[i][1])
                ## condition to check if mem_addr is accessible n acceptable (?)
            else:
                with open("output.txt", "a") as f:
                    f.write(f'Error in line: Wrong format of instruction')
                    flag = True
        elif inst_lst[i][1].lower() == "hlt":
            machine_code.append("0101000000000000")

if not flag:
    with open("output.txt", "a") as f:
        for i in machine_code:
            f.write(i)
            f.write("\n")
