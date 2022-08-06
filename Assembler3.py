import sys
from itertools import permutations

PC_var = 0
PC_label = 0
type_a = {"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100", "addf": "00000", "subf": "00001"}
type_b = {"ls":"11001", "rs":"11000", "mov":"10010"} #mov r1 imm
type_c = {"div": "10111", "not": "11101", "cmp": "11110", "mov": "10011"} # mov r1 r2
type_d = {"st": "10101", "ld": "10100"}
type_e = {"jmp": "11111", "jlt": "01100", "je": "01111", "jgt": "01101"}
reg = {"r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110"}
opcode = {"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100", "ls":"11001", "rs":"11000", "mov":"10010","div": "10111", "not": "11101", "cmp": "11110", "mov": "10011","st": "10100", "ld": "10101","jmp": "11111", "jlt": "01100", "je": "01111", "jgt": "01101", "hlt": "01010"}
lab_dic = {} 
vars = {}
vars_line = {}
machine_code = []
vars_count = 0 
flag = True
flag_a = True
flag_b=True
flag_c=True
flag_d = True
flag_e = True
flag_m=True
flag_h=True
flag_f = True

def check_bin(check_str):   
    flag = True
    for i in range(len(check_str)):
        if check_str[i] not in "01":
            flag = False
            break
    return flag


def convert(PC_var):
    b = bin(PC_var)
    mem = str(b).replace("0b", "")
    mem = format(int(mem), '#08')
    return str(mem)


def DecBin(string):
    if string.isdigit():
        lst=[int(i) for i in string]
        for i in lst:
            if i>=0 and i<=9:
                Flag=True
            else:
                Flag=False
                break
    else:
        Flag=False
  
    if Flag:   
        num=int(string)
        Bnumlst=[]
        q=1
        while q!=0:
            q=num//2
            Bnum=num%2
            Bnumlst.append(Bnum)
            num=q
        zeroes=8-len(Bnumlst)
        for i in range(zeroes):
            Bnumlst.append(0)
        Bnumlst.reverse()
        Anslst=[str(i) for i in Bnumlst]
        Binary_Number="".join(Anslst)
        return(Binary_Number)

def convertFloat(v):        # converts 8 bit binary to float
    exp = int(v[:3], 2)
    num = "1." + v[3:]
    numList = list(num)
    zero = exp - 4
    while zero > 0:
        numList.append("0")
        zero -= 1
    while exp > 0:
        dot = numList.index(".")
        digit = numList[dot + 1]
        numList[dot] = digit
        numList[dot + 1] = "."
        exp -= 1
    num = "".join(numList)
    float_num = num.split('.')
    return int(float_num[0], 2) + int(float_num[1], 2) / 2.**len(float_num[1])

floatNums = {}
bitList = ["11111111", "11111110", "11111100", "11111000", "11110000", "11100000", "11000000", "10000000", "00000000"]
for i in bitList:
    nums = list(i)
    perm = list(permutations(nums))
    permFinal = []
    [permFinal.append(i) for i in perm if i not in permFinal]
    for i in permFinal:
        binary = "".join(i)
        flt = convertFloat(binary)
        floatNums[("".join(i))] = str(flt)



s = sys.stdin.read()
line = s.split("\n")
line_copy = line
inst_lst = []
for i in line:
    ele = i.split()
    inst_lst.append(ele)

c = line.count("")
for i in range(c):
    line.remove("")
inst_lst2 = []
for i in line:
    ele = i.split()
    inst_lst2.append(ele)

for i in range(len(inst_lst2)):
    if inst_lst2[i][0] == "var":
        vars_count += 1

PC_var = len(inst_lst2) - vars_count
    
for i in range(len(inst_lst2)):
    if inst_lst2[i][0] == "var":
        continue
    else:
        if inst_lst2[i][0][-1] == ":" and len(inst_lst2[i]) > 1 and inst_lst2[i][1] in opcode:
            lab_dic[inst_lst2[i][0][:-1].lower()] = DecBin(str(PC_label))
        PC_label += 1

for i in range(len(inst_lst2)):
    if inst_lst2[i][0] == "var":
        if len(inst_lst2[i]) == 2:
            if inst_lst2[i][1] not in opcode and inst_lst2[i][1] not in lab_dic and inst_lst2[i][1] not in reg:
                vars[inst_lst2[i][1].lower()] = convert(PC_var)
                PC_var += 1
                vars_line[inst_lst2[i][1].lower()] = i + 1
            else:
                print(f'Error in line {i+1}: Not a valid variable')
                flag = False
                break
        else:
            print(f'Error in line {i+1}: Not a valid variable syntax')
            flag = False
            break
    else:
        continue

if flag == True:
    for i in range(len(inst_lst2)):
        
        if inst_lst2[i][0][-1]==":":
            label=inst_lst2[i][0]
            inst_lst2[i].pop(0)
            flag_l=True

        if inst_lst2[i][0].lower() in type_a:
            flag_a = True
            if len(inst_lst2[i]) == 4:
                if inst_lst2[i][1].lower() in reg and inst_lst2[i][2].lower() in reg and inst_lst2[i][3].lower() in reg:
                    op = type_a[inst_lst2[i][0]]
                    r1 = reg[inst_lst2[i][1].lower()]
                    r2 = reg[inst_lst2[i][2].lower()]
                    r3 = reg[inst_lst2[i][3].lower()]
                    machine_code.append(op+"00"+r1+r2+r3)
                else:
                    print(f'Error in line {i+1}: Undefined Register name')
                    flag_a = False
                    break
            else:
                print(f'Error in line {i+1}: Wrong Instruction syntax for {inst_lst[i][0].lower()}')
                flag_a = False
                break

        if inst_lst2[i][0].lower() == "movf":
            flag_f = True
            if len(inst_lst2[i]) == 3 or inst_lst2[i][2][0] == "$":
                if inst_lst2[i][1].lower() in reg:
                    if str(float(inst_lst2[i][2][1:])) in floatNums.values():
                        val = list(floatNums.keys())[list(floatNums.values()).index(str(float(inst_lst2[i][2][1:])))]
                        op = "00010"
                        r1 = reg[inst_lst2[i][1].lower()]
                        machine_code.append(op + r1 + val)
                    else:
                        print(f'Error in line {i+1}: Number can not be represented in our system')
                        flag_f = False
                        break
                else:
                    print(f'Error in line {i+1}: Undefined Register name')
                    flag_f = False
                    break
            else:
                print(f'Error in line {i+1}: Wrong Instruction syntax for {inst_lst[i][0].lower()}')
                flag_f = False
                break
                    
        elif inst_lst2[i][0].lower() in type_b and inst_lst2[i][2][0]=="$":
            flag_b = True
            if len(inst_lst2[i])!=3:
                flag_b=False
                print(f'Error in line {i+1}: Number of operands exceed requirement')
            if int(inst_lst2[i][1][1])<0 or int(inst_lst2[i][1][1])>6:
                flag_b=False
                print(f'Error in line {i+1}: Undefined Register name')
            if inst_lst2[i][2].lower()=="flag":
                flag_b=False
                print(f'Error in line {i+1}: Illegal use of flags register')
            Imm=inst_lst2[i][2][1:]
            if int(Imm)<0 or int(Imm)>255:
                flag_b=False
                print(f'Error in line {i+1}: Illegal immediate values')
            if flag_b:
                op=type_b[inst_lst2[i][0].lower()]
                r1=reg[(inst_lst2[i][1]).lower()]
                Im=DecBin(Imm)
                machine_code.append(op+r1+Im)
        
        elif inst_lst2[i][0] in type_c:
            flag_c = True
            if len(inst_lst2[i]) != 3:
                flag_c=False
                print(f'Error in line {i+1}: Number of operand exceed requirement')
            if not(inst_lst2[i][2][1].isnumeric()) or int(inst_lst2[i][2][1])<0 or int(inst_lst2[i][2][1])>6:
                flag_c=False
                print(f'Error in line {i+1}: Undefined Register name')
            if inst_lst2[i][1].lower()=="flags":
                if inst_lst2[i][0]!="mov":
                    flag_c=False
                    print(f'Error in line {i+1}: Illegal use of flag register')
            if inst_lst2[i][2].lower()=="flags":
                flag_c=False
                print(f'Error in line {i+1}: Illegal use of flag register')
            if flag_c:
                op=type_c[inst_lst2[i][0]]
                r2=reg[(inst_lst2[i][2]).lower()]
                if inst_lst2[i][1].lower()=="flags":
                    r1="111"
                else:
                    r1=reg[(inst_lst2[i][1]).lower()]
                machine_code.append(op+"00000"+r1+r2)  
            
        elif inst_lst2[i][0].lower() in type_d:  
            flag_d = True
            if len(inst_lst2[i]) == 3:
                if inst_lst2[i][1].lower() in reg:
                    if inst_lst2[i][2] in vars:
                        op = type_d[inst_lst2[i][0]]
                        r1 = reg[inst_lst2[i][1].lower()]
                        mem = vars[inst_lst2[i][2].lower()]
                        machine_code.append(op + r1 + mem)
                    elif inst_lst2[i][2] in lab_dic:
                        print(f'Error in line {i+1}: Use of labels as variables')
                        flag_d = False
                        break
                    else:
                        print(f'Error in line {i+1}: Use of undefined variable')
                        flag_d = False
                        break
                else:
                    print(f'Error in line {i+1}: Undefined Register name')
                    flag_d = False
                    break
            else:
                print(f'Error in line {i+1}: Wrong Instruction syntax for {inst_lst[i][0].lower()}')
                flag_d = False
                break
    
        elif inst_lst2[i][0].lower() in type_e:
            flag_e = True
            if len(inst_lst2[i]) == 2:
                if inst_lst2[i][1].lower() in lab_dic:
                    op = type_e[inst_lst2[i][0]]
                    mem = lab_dic[inst_lst2[i][1].lower()]
                    machine_code.append(op+"000"+mem)
                elif inst_lst2[i][1].lower() in vars:
                    print(f'Error in line {i+1}: Use of variables as labels')
                    flag_e = False
                    break
                else:
                    print(f'Error in line {i+1}: Memory address is not a label')
                    flag_e = False
                    break
            else:
                print(f'Error in line {i+1}: Wrong Instruction syntax for {inst_lst2[i][0].lower()}')
                flag_e = False
                break
        
        elif (inst_lst2[i][0].lower() == "hlt") and (i < (len(inst_lst2) - 1)):
            flag_h = False
            print(f'Error in line {i+1}: Invalid hlt declaration')
            break
        
        elif inst_lst2[i][0].lower() == "hlt":
            machine_code.append("0101000000000000")
            flag_h=True

        elif inst_lst2[i][0].lower() not in opcode and (inst_lst2[i][0].lower() != "var") and (":" not in inst_lst2[i][0].lower()):
            print(f'Error in line {i+1}: Not an instruction syntax')
            flag = False
            break

if flag and (len(inst_lst2[-1]) != 1 or inst_lst2[-1][0] != "hlt") and flag_h:
    flag = False
    print(f'Error in line {len(inst_lst2)}: Invalid/Absent hlt declaration')

for i in range(len(vars)):
    if inst_lst2[0][0].lower() == "var":
        inst_lst2.remove(inst_lst2[0])

for i in range(len(inst_lst2)):
    if flag and inst_lst2[i][0] == "var":
        flag = False
        print(f'Error in line {vars_line[inst_lst2[i][1]]}: Variable not declared at the begining')
    
if len(machine_code) > 256:
    print(f'Number of instructions exceed limit')
    machine_code = machine_code[:256]
if flag and flag_a and flag_b and flag_c and flag_d and flag_e and flag_f and flag_h:
    for i in machine_code:
        sys.stdout.write(i)
        sys.stdout.write("\n")
