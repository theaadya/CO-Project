PC = 0
type_a = {"add": "10000", "sub": "10001", "mul": "10110", "xor": "11010", "or": "11011", "and": "11100"}
type_b = {"ls":"11001", "rs":"11000", "mov":"10010"} #mov r1 imm
type_c = {"div": "10111", "not": "11101", "cmp": "11110", "mov": "10011"} # mov r1 r2
type_d = {"st": "10100", "ld": "10101"}
type_e = {"jmp": "11111", "jlt": "01100", "je": "01111", "jgt": "01101"}
reg = {"r0": "000", "r1": "001", "r2": "010", "r3": "011", "r4": "100", "r5": "101", "r6": "110", "r7": "111"}
vars = {}
labels = {} # with line number where labels come
machine_code = []
vars_count = 0 
flag = False

def check_bin(check_str):
    flag = False
    for i in range(len(check_str)):
        if check_str[i] not in "01":
            flag = True
            break
    return flag

def parse_vars(lst, vars_dict, PC):
    for i in lst:
        if "var" not in i.lower():
            PC+=1
        else:
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
    if Flag and Flag1:      # typo in Flag1 (?)     # also can use bin() function instead
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

    # parse_vars(lst1, vars, PC)

f=input()
lines=f.split("\n")
inst_lst=[]
for i in lines:
    new_line=i.split()
    inst_lst.append(new_line)

# alternative code to read multi line input
# import sys
# s = sys.stdin.read()
# line = s.split("\n")
# inst_lst = []
# for i in line:
#     ele = i.split()
#     inst_lst.append(ele)


if len(inst_lst[-1]) != 1 or inst_lst[-1][0] != "hlt":
        flag = True
        print(f'Error in line {len(inst_lst)}: Invalid/Absent hlt declaration')

if flag == False:
    for i in range(len(inst_lst)):
        if inst_lst[i][0].lower() in type_a:
            flag_a = True
            if len(inst_lst[i]) != 4:
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
            
        elif inst_lst[i][0] in type_b and inst_lst[i][2][1]=="$":
            flag_b=True
            if len(inst_lst[i])!=3:
                flag_b=False
                print(f'Error in line {i}: Number of operands exceed requirement')
            if int(inst_lst[i][1][3])<0 or int(inst_lst[i][1][3])>6:
                flag_b=False
                print(f'Error in line {i}: Undefined Register name')
            if inst_lst[i][2]=="FLAG":
                flag_b=False
                print(f'Error in line {i}: Illegal use of flags register')
            Imm=""
            for k in range(1,len(inst_lst[i][2])):
                Imm+=inst_lst[i][2][k]
            if int(Imm)<0 or int(Imm)>255:
                flag_b=False
                print(f'Error in line {i}: Illegal immediate values')
            if flag_b:
                op=type_b[inst_lst[i][0]]
                r1=reg[inst_lst[i][1]]
                Im=DecBin(Imm)
                machine_code.append(op+r1+Im)
               
        elif inst_lst[i][0] in type_c:
            flag_c=True
            if len(inst_lst[i]) == 3:
                flag_c=False
                print(f'Error in line {i}: Number of operand exceed requirement')
            if int(inst_lst[i][1][3])<0 or int(inst_lst[i][1][3])>6:
                flag_c=False
                print(f'Error in line {i}: Undefined Register name')
            if inst_lst[i][2]=="FLAG":
                if inst_lst[i][0]!="mov":
                    flag_c=False
                    print(f'Error in line {i}: Illegal use of flag register')
            if inst_lst[i][1]=="FLAG":
                flag_c=False
                print(f'Error in line {i}: Illegal use of flag register')
            if inst_lst[i][2]!="FLAG":
                if int(inst_lst[i][1][3])<0 or int(inst_lst[i][1][3])>6:
                    flag_c=False
                    print(f'Error in line {i}: Undefined register name')
            if flag_c:
                op=type_c[inst_lst[i][0]]
                r1=reg[inst_lst[i][1]]
                if inst_lst[i][2]=="FLAG":
                    r2="111"
                else:
                    r2=reg[inst_lst[i][2]]
                machine_code.append(op+"00000"+r1+r2)  
          
        elif inst_lst[i][1].lower() in type_d:
            flag_d=True
            new_st=""
            if len(inst_lst[i]) == 4:
                new_st.append(type_d[inst_lst[i][1]])
            else:
                flag_d=False
                machine_code.append(f'Error in line: Wrong format of instruction')
            if inst_lst[i][2].lower() in reg:
                new_st.append(reg[inst_lst[i][2]])
            else:
                flag_d=False
                machine_code.append(f'Error in line: Undefined register name')
            if len(inst_lst[i][3])==8 and check_bin(inst_lst[i][3]):
                new_st.append(inst_lst[i][3])
            else:
                flag_d=False
                machine_code.append(f'Error in line: Memory address is not accessible/acceptable')   
            if flag_d:
                machine_code.append(new_st)
                
        elif inst_lst[i][1].lower() in type_e:
            flag_e=True
            new_st=""
            if len(inst_lst[i]) == 3:
                new_st.append(type_e[inst_lst[i][1]])
            else:
                flag_e=False
                machine_code.append(f'Error in line: Wrong format of instruction')
            if len(inst_lst[i][2]) == 8:
                new_st.append(inst_lst[i][1])
                # condition to check if mem_addr is accessible (?)
            else:
                flag_e=False
                machine_code.append(f'Error in line: Memory address is not accessible/acceptable')   
                                    
            if flag_e:
                machine_code.append(new_st) 

        elif inst_lst[i][0].lower() == "hlt":
            machine_code.append("0101000000000000")
            
        elif inst_lst[i][0] == "":
            continue
if not flag:
    for i in machine_code:
        print(i, end = "\n")
