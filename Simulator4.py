# final code for SIM
import sys
from itertools import permutations
import matplotlib.pyplot as plt

s = sys.stdin.read()
machine_code = s.split("\n")
for i in range(machine_code.count("")):
    machine_code.remove("")
lstCopy = machine_code.copy()

machine_code_dic = {}
for idx, val in enumerate(machine_code):
    machine_code_dic[idx] = val
codeCopy = machine_code_dic.copy()

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
    binary = bin(n).replace("0b", "") 
    return int(binary)

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

def printPCReg(pc):
    pcFormat = format(int(pc), "#010b").replace("0b", "") 
    sys.stdout.write(pcFormat)
    sys.stdout.write(" ")
    for i in regval:
        sys.stdout.write(regval[i])
        sys.stdout.write(" ")
    sys.stdout.write("0" * 12)
    for i in flag_dic:
        sys.stdout.write(flag_dic[i])
    sys.stdout.write("\n")

var_mem = []
memory = {}
zero_str = "0"*16
for idx, val in enumerate(machine_code):
    if val[:5] == "10100" or val[:5] == "10101":
        var_mem.append(val[8:])
    memory[idx] = val
var_final = []
[var_final.append(i) for i in var_mem if i not in var_final]
zero_nums = 256 - len(machine_code)
for i in range(zero_nums):
    memory[len(memory)] = "0"*16

x_axis, y_axis = [], []
cycle = 0

def main(i):
    reset_flags()
    opcode=i[:5]
    if opcode=="10000" or opcode=="10001" or opcode=="10110" or opcode=="11010" or opcode=="11011" or opcode=="11100":
        #type_a
        reg1=i[7:10]
        reg2=i[10:13]
        reg3=i[13:16]
        if opcode=="10000":     #add
            val3 = ((bintodec(int(regval[regnum[reg1]])) + bintodec(int(regval[regnum[reg2]]))))
            val3 = str(dectobin(val3))
            if int(val3, 2) > (2**(16)):
                regval[regnum[reg3]] = "1"*16
                flag_dic["v"]="1"
            else:
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
            if int(val3, 2) > (2**16):
                flag_dic["v"]="1"
                regval[regnum[reg3]] = "1"*16
            else:
                regval[regnum[reg3]] = ("0"*(16-len(val3)))+val3
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
        
    if opcode=="10010" or opcode=="11000" or opcode=="11001":
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
        if opcode=="10100":     # load instruction
            regval[regnum[reg]] = memory[var_address]
        if opcode=="10101":     # store instruction
            memory[var_address] = regval[regnum[reg]]
        
    elif opcode=="00000" or opcode=="00001" or opcode=="00010":     #floating point operations
        if opcode == "00000":       # addf
            r1 = i[7:10]
            r2 = i[10:13]
            r3 = i[13:16]
            val1 = convertFloat(regval[regnum[r1]][8:])
            val2 = convertFloat(regval[regnum[r2]][8:])
            val3 = float(val1) + float(val2)
            if val3 > 252:
                regval[regnum[r3]] = "0"*8 + "1"*8
                flag_dic["v"]="1"
            elif str(float(val3)) not in floatNums.values():
                regval[regnum[r3]] = "0"*16
                flag_dic["v"]="1"
            else:
                val = list(floatNums.keys())[list(floatNums.values()).index(str(float(val3)))]
                regval[regnum[r3]] = "0"*8 + val
        elif opcode == "00001":         # subf
            r1 = i[7:10]
            r2 = i[10:13]
            r3 = i[13:16]
            val1 = convertFloat(regval[regnum[r1]][8:])
            val2 = convertFloat(regval[regnum[r2]][8:])
            val3 = float(val1) - float(val2)
            if str(float(val3)) not in floatNums.values():
                regval[regnum[r3]] = "0"*16
                flag_dic["v"] = "1"
            else:
                val = list(floatNums.keys())[list(floatNums.values()).index(str(float(val3)))]
                regval[regnum[r3]] = "0"*8 + val
        elif opcode == "00010":     # movf
            r1 = i[5:8]
            regval[regnum[r1]] = "0"*8 + i[8:]

    if opcode=="01010": #hlt
        pass
    return

def simulator(machine_code, machine_dic, cycle):
    for i in machine_code:
        global codeCopy
        global lstCopy
        opcode=i[:5]
        pc = list(machine_dic.keys())[list(machine_dic.values()).index(i)]
        del machine_dic[pc]
        if opcode=="11110":     # cmp instruction, all flags reset and then set
            reset_flags()
            reg1=i[10:13]
            reg2=i[13:16]
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            if val1<val2: #less than
                flag_dic["l"]="1"
            elif val1>val2: #greater than
                flag_dic["g"]="1"
            elif val1==val2: #equal to
                flag_dic["e"]="1"

        else:
            if opcode=="01100" or opcode == "01101" or opcode == "01111" or opcode == "11111": #jump, flag not reset
                mem_addr=i[8:]
                label_addr=int(mem_addr,2)
                
                if opcode=="01100" and flag_dic["l"]=="1": #less than
                    reset_flags()
                    printPCReg(pc)
                    x_axis.append(cycle)
                    y_axis.append(pc)
                    cycle += 1
                    machine_lst = lstCopy
                    lstCopy = lstCopy.copy()
                    new_machine_code = machine_lst[label_addr:]
                    machine_dic = codeCopy
                    codeCopy = codeCopy.copy()
                    simulator(new_machine_code, machine_dic, cycle)
                    break
                if opcode=="01101" and flag_dic["g"]=="1": #greater than
                    reset_flags()
                    printPCReg(pc)
                    x_axis.append(cycle)
                    y_axis.append(pc)
                    cycle += 1
                    machine_lst = lstCopy
                    lstCopy = lstCopy.copy()
                    new_machine_code = machine_lst[label_addr:]
                    machine_dic = codeCopy
                    codeCopy = codeCopy.copy()
                    simulator(new_machine_code, machine_dic, cycle)
                    break
                if opcode=="01111" and flag_dic["e"]=="1": # equal to
                    reset_flags()
                    printPCReg(pc)
                    x_axis.append(cycle)
                    y_axis.append(pc)
                    cycle += 1
                    machine_lst = lstCopy
                    lstCopy = lstCopy.copy()
                    new_machine_code = machine_lst[label_addr:]
                    machine_dic = codeCopy
                    codeCopy = codeCopy.copy()
                    simulator(new_machine_code, machine_dic, cycle)
                    break
                if opcode=="11111": # uncondtional jump
                    reset_flags()
                    printPCReg(pc)
                    x_axis.append(cycle)
                    y_axis.append(pc)
                    cycle += 1
                    machine_lst = lstCopy
                    lstCopy = lstCopy.copy()
                    new_machine_code = machine_lst[label_addr:]
                    machine_dic = codeCopy
                    codeCopy = codeCopy.copy()
                    simulator(new_machine_code, machine_dic, cycle)
                    break
                else:
                    reset_flags()
            else: # any other instruction, flags reset
                main(i)
        printPCReg(pc)
        x_axis.append(cycle)
        y_axis.append(pc)
        cycle += 1
    return

regnum={"000":"r0" , "001":"r1" , "010":"r2" , "011":"r3" , "100":"r4" , "101":"r5" , "110":"r6"}
regval={"r0":"0000000000000000" , "r1":"0000000000000000" , "r2":"0000000000000000" , "r3":"0000000000000000" , "r4":"0000000000000000" , "r5":"0000000000000000" , "r6":"0000000000000000"}
flag_dic={"v":"0" , "l":"0" , "g":"0" , "e":"0"}
# var_dic={}

simulator(machine_code, machine_code_dic, cycle)

# code for printing memory
for i in memory.values():
    sys.stdout.write(i)
    sys.stdout.write("\n")

plt.scatter(x_axis, y_axis, c ="blue")
plt.show()
