import sys
PC = 0
type_a = {"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100"}
type_b = {"ls":"11001", "rs":"11000", "mov":"10010"} #mov r1 imm
type_c = {"div": "10111", "not": "11101", "cmp": "11110", "mov": "10011"} # mov r1 r2
type_d = {"st": "10100", "ld": "10101"}
type_e = {"jmp": "11111", "jlt": "01100", "je": "01111", "jgt": "01101"}
reg = {"r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110", "r7": "111"}
labels = {} 
vars = {}
machine_code = []
vars_count = 0 
flag = True

opcode={"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100", "ls":"11001", "rs":"11000", "mov":"10010","div": "10111", "not": "11101", "cmp": "11110", "mov": "10011","st": "10100", "ld": "10101","jmp": "11111", "jlt": "01100", "je": "01111", "jgt": "01101"}

def check_bin(check_str):   
    flag = True
    for i in range(len(check_str)):
        if check_str[i] not in "01":
            flag = False
            break
    return flag

def parse_vars(lst, vars_dict, vars_count):
    for i in lst:
        if "var" in i.lower():
            vars_count += 1
            vars_dict[f'var {vars_count}'] = i[4]

def DecBin(string):
    #checking if number is decimal
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
  
    #converting decimal to binary
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

    if not(Flag):
        return("Enter the correct number")

    
def BinDec(string):
    #Checking if input number is binary.
    if string.isdigit():
        lst=[int(i) for i in string]
        for i in lst:
            if i>=0 and i<=1:
                Flag=True
            else:
                Flag=False
                break
    else:
        Flag=False


    #Converting binary number to decimal number.
    if Flag:
        lst=[int(i) for i in string]
        DecNum=0
        highestPower=len(lst)
        for i in range(len(lst)):
            DecNum+=(lst[i]*(2**(highestPower-1)))
            highestPower-=1
        return(DecNum)

    if not(Flag):
        return("Enter the correct number")

    
# f=input()
# lines=f.split("\n")
# inst_lst=[]
# for i in lines:
#     new_line=i.split()
#     inst_lst.append(new_line)

s = sys.stdin.read()
line = s.split("\n")
inst_lst = []
for i in line:
    ele = i.split()
    inst_lst.append(ele)

parse_vars(line, vars, vars_count)

c = line.count("")
for i in range(c):
    line.remove("")
inst_lst2 = []
for i in line:
    ele = i.split()
    inst_lst2.append(ele)

PC = len(inst_lst2) - len(vars) - 1

if len(inst_lst2[-1]) != 1 or inst_lst2[-1][0] != "hlt":
        flag = False
        print(f'Error in line {len(inst_lst2)}: Invalid/Absent hlt declaration')
    
lab_dic={}
for i in range(len(inst_lst)):
    elif inst_lst[i][0][-1]==":" and inst_lst[i][1] in opcode:
        lab_dic[DecBin(string(i))]=inst_lst[i][0][:-1].lower()

if flag == True:
    for i in range(len(inst_lst)):
        
        if len(inst_lst[i]) == 0:
            continue
            
        if inst_lst[i][0].lower() in type_a:
            flag_a = True
            if len(inst_lst[i]) != 4:
                flag_a=False
                print(f'Error in line {i+1}: Wrong Instruction syntax for {inst_lst[i][0].lower()}')
            if inst_lst[i][1].lower() not in reg or inst_lst[i][2].lower() not in reg or inst_lst[i][3].lower() not in reg:
                flag_a = False
                print(f'Error in line {i+1}: Undefined Register name')
            if flag_a:
                op = type_a[inst_lst[i][0]]
                r1 = reg[inst_lst[i][1].lower()]
                r2 = reg[inst_lst[i][2].lower()]
                r3 = reg[inst_lst[i][3].lower()]
                machine_code.append(op+"00"+r1+r2+r3)
            
        elif inst_lst[i][0].lower() in type_b and inst_lst[i][2][1]=="$":
            flag_b=True
            if len(inst_lst[i])!=3:
                flag_b=False
                print(f'Error in line {i+1}: Number of operands exceed requirement')
            if int(inst_lst[i][1][1])<0 or int(inst_lst[i][1][1])>6:
                flag_b=False
                print(f'Error in line {i+1}: Undefined Register name')
            if inst_lst[i][2].lower()=="flag":
                flag_b=False
                print(f'Error in line {i+1}: Illegal use of flags register')
            Imm=inst_lst[i][2][1:]
            if int(Imm)<0 or int(Imm)>255:
                flag_b=False
                print(f'Error in line {i+1}: Illegal immediate values')
            if flag_b:
                op=type_b[inst_lst[i][0].lower()]
                r1=reg[inst_lst[i][1]]
                Im=DecBin(Imm)
                machine_code.append(op+r1+Im)
               
        elif inst_lst[i][0] in type_c:
            flag_c=True
            if len(inst_lst[i]) != 3:
                flag_c=False
                print(f'Error in line {i+1}: Number of operand exceed requirement')
            if int(inst_lst[i][1][1])<0 or int(inst_lst[i][1][1])>6:
                flag_c=False
                print(f'Error in line {i+1}: Undefined Register name')
            if inst_lst[i][2].lower()=="flag":
                if inst_lst[i][0]!="mov":
                    flag_c=False
                    print(f'Error in line {i+1}: Illegal use of flag register')
            if inst_lst[i][1].lower()=="flag":
                flag_c=False
                print(f'Error in line {i+1}: Illegal use of flag register')
            if inst_lst[i][2].lower()!="flag":
                if int(inst_lst[i][1][1])<0 or int(inst_lst[i][1][1])>6:
                    flag_c=False
                    print(f'Error in line {i+1}: Undefined register name')
            if flag_c:
                op=type_c[inst_lst[i][0]]
                r1=reg[inst_lst[i][1]]
                if inst_lst[i][2].lower()=="flag":
                    r2="111"
                else:
                    r2=reg[inst_lst[i][2]]
                machine_code.append(op+"00000"+r1+r2)  
                
        elif inst_lst[i][0].lower() in type_d:
            if len(inst_lst[i]) == 3:
                if inst_lst[i][1].lower() in reg:
                    if inst_lst[i][2] in vars.values():
                        op = type_d[inst_lst[i][0]]
                        r1 = reg[inst_lst[i][1].lower()]
                        PC += 1
                        b = bin(PC)
                        mem = str(b).replace("0b", "")
                        mem = format(int(mem), '#08')
                        machine_code.append(op+r1+mem)
                    elif inst_lst[i][2] in labels:
                        print(f'Error in line {i+1}: Use of labels as variables')
                    else:
                        print(f'Error in line {i+1}: Use undefined variables')
                else:
                    print(f'Error in line {i+1}: Undefined Register name')
            else:
                print(f'Error in line {i+1}: Wrong Instruction syntax for {inst_lst[i][0].lower()}')
                
        elif inst_lst[i][0].lower() in type_e:
            flag_e=True
            if len(inst_lst[i])!=2:
                flag_e=False
                print(f' Error in line {i+1}: Number of operands exceed requirement')
            if inst_lst[i][1] not in lab_dic:
                flag_e=False
                print(f'Error in line {i+1}: memory address is not a label')
            if flag_e:
                op=type_e[inst_lst[i][0]]
                mem=inst_lst[i][1]
                machine_code.append(op+mem)

        elif inst_lst[i][0].lower() == "hlt":
            machine_code.append("0101000000000000")           
            
if flag:
    for i in machine_code:
        print(i, end = "\n")
