# final code for SIM
import sys

s = sys.stdin.read()
machine_code = s.split("\n")
for i in range(machine_code.count("")):
    machine_code.remove("")

machine_code_dic = {}
for idx, val in enumerate(machine_code):
    machine_code_dic[idx] = val

def reset_flags():
    for i in flag_dic.keys():
        flag_dic[i]="0"
def bintodec(n):
    num=0
    n=str(n)
    pow=0
    for i in n[::-1]:
        b=int(i)
        num+=((2**(pow))*b)
        pow+=1
    return num
def dectobin(n):
    num=n
    val=""
    while num>0:
        val+=str(num%2)
        num=num//2
    val=val[::-1]
    return int(val)
def perform_xor(a,b):
    if a==b:
        return "0"
    else:
        return "1"
def perform_or(a,b):
    if a=="1" or b=="1":
        return "1"
    else:
        return "0"
def perform_and(a,b):
    if a=="0" or b=="0":
        return "0"
    else:
        return "1"
def perform_not(a):
    if a=="0":
        return "1"
    else:
        return "0"
def convertFloat(val):
    v = val[8:]
    exp = bin(int(v[:3]))
    num = "1." + v[3:]
    while exp > 0:
        dot = num.index(".")
        digit = num[dot + 1]
        num[dot] = digit
        num[dot + 1] = "."
        exp -= 1
    float_num = num.split('.')
    return int(float_num[0], 2) + int(float_num[1], 2) / 2.**len(float_num[1])

def convertCSE112(val):


var_mem = []
memory = []
zero_str = "0000000000000000"
for i in machine_code:
    if i[:5] == "10100" or i[:5] == "10101":
        var_mem.append("00000000"+i[8:])
    memory.append(i)
for i in range(len(var_mem)):
    memory.append(var_mem[i])
zero_nums = 256 - (len(machine_code) + len(var_mem))

x_axis, y_axis = [], []
for i in range(len(memory)):
    if memory[i] != "0101000000000000":
        x_axis.append(i+1)
    else:
        break

def main(i,var_dic):
    opcode=i[:5]
    if opcode=="10000" or opcode=="10001" or opcode=="10110" or opcode=="11010" or opcode=="11011" or opcode=="11100":
        #type_a
        reg1=i[7:10]
        reg2=i[10:13]
        reg3=i[13:16]
        if opcode=="10000":     #add
            val3=str(dectobin(bintodec(int(regval[regnum[reg1]])) + bintodec(int(regval[regnum[reg2]]))))
            regval[regnum[reg3]]=("0"*(16-len(val3)))+val3
        elif opcode=="10001":   #sub
            val1=bintodec(int(regval[regnum[reg1]]))
            val2=bintodec(int(regval[regnum[reg2]]))
            if val2>val1:
                regval[regnum[reg3]]="0000000000000000"
                flag_dic["v"]="1"
            else:
                val3=str(dectobin(val1-val2))
                regval[regnum[reg3]]=("0"*(16-len(val3)))+val3
        elif opcode=="10110":   #multiply
            val1=bintodec(int(regval[regnum[reg1]]))
            val2=bintodec(int(regval[regnum[reg2]]))
            val3=str(dectobin(val1*val2))
            diff=16-len(val3)
            if diff<0:
                flag_dic["v"]="1"
                val3=val3[(len(val3)-16):]
                regval[regnum[reg3]]=val3
            else:
                regval[regnum[reg3]]=("0"*diff)+val3
        elif opcode=="11010":   #bitwise xor
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            val3=""
            for i in range(16):
                val3+=perform_xor(val1[i],val2[i])
            regval[regnum[reg3]]=val3
        elif opcode=="11011":   #bitwise or
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            val3=""
            for i in range(16):
                val3+=perform_or(val1[i],val2[i])
            regval[regnum[reg3]]=val3
        else:   #bitwise and
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            val3=""
            for i in range(16):
                val3+=perform_and(val1[i],val2[i])
            regval[regnum[reg3]]=val3
        
    if opcode=="10010" or opcode=="11000" or opcode=="11001" or opcode == "00010":
        #type_b
        reg1=i[5:8]
        imm=i[8:]
        if opcode=="10010": #mov imm
            regval[regnum[reg1]]=("0"*8)+imm
        elif opcode=="11000":   #right shift
            imm=bintodec(int(imm))
            st1="0"*imm
            st2=(regval[regnum[reg1]][:(-imm)])
            regval[regnum[reg1]]=st1+st2
        elif opcode=="11001":   #left shift
            imm=bintodec(int(imm))
            st1=regval[regnum[reg1]][imm:]
            st2="0"*imm
            regval[regnum[reg1]]=st1+st2
        # else:     # mov float

    if opcode=="10011" or opcode=="10111" or opcode=="11101":
        #type_c
        reg1=i[10:13]
        reg2=i[13:16]
        if opcode=="11101":     # Invert
            notval1=""
            for i in range(16):
                notval1+=perform_not(regval[regnum[reg1]])
            regval[regnum[reg2]]=notval1
        elif opcode=="10111":   # divide
            val1=bintodec(int(regval[regnum[reg1]]))
            val2=bintodec(int(regval[regnum[reg2]]))
            q=val1//val2
            r=val1%val2
            q=str(dectobin(q))
            r=str(dectobin(r))
            regval["r0"]=("0"*(16-len(q)))+q
            regval["r1"]=("0"*(16-len(r)))+r
        elif opcode=="10011":   # mov
            regval[regnum[reg2]]=regval[regnum[reg1]]


    #type_d
    if opcode=="10100" or opcode=="10101":
        reg=i[5:8]
        mem_addr = i[8:]
        var_address = int(mem_addr,2)
        if opcode=="10100":     #load instruction
            regval[regnum[reg]]=var_dic[var_address]
        if opcode=="10101":     #store instruction
            var_dic[var_address]=regval[regnum[reg]]
        
    elif opcode=="00000" or opcode=="00001" or opcode=="00010":     #floating point operations
        r1 = i[7:10]
        r2 = i[10:13]
        r3 = i[13:16]
        val1 = convertFloat(regval[regnum[r1]])
        val2 = convertFloat(regval[regnum[r2]])
        if opcode == "00000":
            val3 = val1 + val2
            if convertCSE112(val3) == False:
                regval[regnum[r3]] = "0000000000000000"
                flag_dic["v"]="1"
            else:
                val = convertCSE112(val3)
                regval[regnum[r3]] = val
        elif opcode == "00001":
            


    if opcode=="01010":#hlt
        pass
    return

def simulator(machine_code,regval,flag_dic, machine_code_dic):
    for i in machine_code:
        opcode=i[:5]
        pc = list(machine_code_dic.keys())[list(machine_code_dic.values()).index(i)]
        del machine_code_dic[pc]
        if opcode=="11110":     # cmp instruction, all flags reset and then set
            reset_flags()
            reg1=i[10:13]
            reg2=i[13:16]
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            if val1<val2: #less than
                flag_dic["l"]=="1"
            elif val1>val2: #greater than
                flag_dic["g"]=="1"
            elif val1==val2: #equal to
                flag_dic["e"]=="1"

        else:
            if opcode=="01100" or "01101" or "01111" or "11111": #jump, flag not reset
                mem_addr=i[8:]
                label_addr=int(mem_addr,2)
                
                if opcode=="01100" and flag_dic["l"]==1: #less than
                    print(format(int(pc), "#010b").replace("0b", ""))
                    new_machine_code=machine_code[label_addr:]
                    simulator(new_machine_code,regval,flag_dic, machine_code_dic)
                    break
                if opcode=="01101" and flag_dic["g"]==1: #greater than
                    print(format(int(pc), "#010b").replace("0b", ""))
                    new_machine_code=machine_code[label_addr:]
                    simulator(new_machine_code,regval,flag_dic, machine_code_dic)
                    break
                if opcode=="01111" and flag_dic["e"]==1: # equal to
                    print(format(int(pc), "#010b").replace("0b", ""))
                    new_machine_code=machine_code[label_addr:]
                    simulator(new_machine_code,regval,flag_dic, machine_code_dic)
                    break
                if opcode=="11111": # uncondtional jump
                    print(format(int(pc), "#010b").replace("0b", ""))
                    new_machine_code=machine_code[label_addr:]
                    simulator(new_machine_code,regval,flag_dic, machine_code_dic)
                    break
            else: #any other instruction, flags reset
                main(i,var_mem)
                reset_flags()
        print(format(int(pc), "#010b").replace("0b", ""))
        # print(regval)
        # print(flag_dic)
    return

regnum={"000":"r0" , "001":"r1" , "010":"r2" , "011":"r3" , "100":"r4" , "101":"r5" , "110":"r6"}
regval={"r0":"0000000000000000" , "r1":"0000000000000000" , "r2":"0000000000000000" , "r3":"0000000000000000" , "r4":"0000000000000000" , "r5":"0000000000000000" , "r6":"0000000000000000"}
flag_dic={"v":"0" , "l":"0" , "g":"0" , "e":"0"}
# var_dic={}  # what to store? , see load n store

simulator(machine_code,regval,flag_dic, machine_code_dic)

# code for printing memory
for i in machine_code:
    print(i, end = "\n")
for i in range(len(var_mem)):
    print(var_mem[i], end = "\n")
for i in range(zero_nums):
    print(zero_str, end = "\n")

# trial machine_code
# 1000000100101110
# 1000100100101110
# 1111000000110000
# 1000000100101110
# 1111100000000111
# 1000000100101110
# 1000100100101110
# 1000000100101110
# 0101000000000000
