import sys


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

def main(i,var_dic):
    opcode=i[:5]
    if opcode=="10000" or opcode=="10001" or opcode=="10110" or opcode=="11010" or opcode=="11011" or opcode=="11100":
        #type_a
        reg1=i[7:10]
        reg2=i[10:13]
        reg3=i[13:16]
        if opcode=="10000":
            val3=str(dectobin(bintodec(int(regval[regnum[reg1]])) + bintodec(int(regval[regnum[reg2]]))))
            regval[regnum[reg3]]=("0"*(16-len(val3)))+val3
        elif opcode=="10001":
            val1=bintodec(int(regval[regnum[reg1]]))
            val2=bintodec(int(regval[regnum[reg2]]))
            if val2>val1:
                regval[regnum[reg3]]="0000000000000000"
                flag_dic["v"]="1"
            else:
                val3=str(dectobin(val1-val2))
                regval[regnum[reg3]]=("0"*(16-len(val3)))+val3
        elif opcode=="10110":#multiply
            val1=bintodec(int(regval[regnum[reg1]]))
            val2=bintodec(int(regval[regnum[reg2]]))
            res=str(dectobin(val1*val2))
            diff=16-len(val3)
            if diff<0:
                flag_dic["v"]="1"
                val3=val3[(len(val3)-16):]
                regval[regnum[reg3]]=val3
            else:
                regval[regnum[reg3]]=("0"*diff)+val3
        elif opcode=="11010":#bitwise xor
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            val3=""
            for i in range(16):
                val3+=perform_xor(val1[i],val2[i])
            regval[regnum[reg3]]=val3
        elif opcode=="11011":#bitwise or
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            val3=""
            for i in range(16):
                val3+=perform_or(val1[i],val2[i])
            regval[regnum[reg3]]=val3
        else:#bitwise and
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
        if opcode=="10010":
            regval[regnum[reg1]]=("0"*8)+imm
        elif opcode=="11000":
            #right shift
            imm=bintodec(int(imm))
            st1="0"*imm
            st2=(regval[regnum[reg1]][:(-imm)])
            regval[regnum[reg1]]=st1+st2
        else:
            #left shift
            imm=bintodec(int(imm))
            st1=regval[regnum[reg1]][imm:]
            st2="0"*imm
            regval[regnum[reg1]]=st1+st2

    if opcode=="10011" or opcode=="10111" or opcode=="11101":
        #type_c
        reg1=i[10:13]
        reg2=i[13:16]
        if opcode=="11101":
            notval1=""
            for i in range(16):
                notval1+=perform_not(regval[regnum[reg1]])
            regval[regnum[reg2]]=notval1
        elif opcode=="10111":
            val1=bintodec(int(regval[regnum[reg1]]))
            val2=bintodec(int(regval[regnum[reg2]]))
            q=val1//val2
            r=val1%val2
            q=str(dectobin(q))
            r=str(dectobin(r))
            regval["r0"]=("0"*(16-len(q)))+q
            regval["r1"]=("0"*(16-len(r)))+r
        elif opcode=="10011":
            regval[regnum[reg2]]=regval[regnum[reg1]]


    #type_d
    if opcode=="10100" or opcode=="10101":
        reg=i[5:8]
        var_address=i[8:]
        if opcode=="10100":#load instruction
            regval[regnum[reg]]=var_dic[var_address]
        if opcode=="10101":#store instruction
            var_dic[var_address]=regval[regnum[reg]]
        
    #elif opcode=="00000" or opcode=="00001" or opcode=="00010":#floating point operations
    if opcode=="01010":#hlt
        pass
    return

def simulator(machine_code,regval,flag_dic):
    pc=1
    for i in machine_code:
        opcode=i[:5]
        #cmp instruction, flag is set
        if opcode=="11110":
            reg1=i[10:13]
            reg2=i[13:16]
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
            if val1<val2: #less than
                flag_dic["l"]=="1"
            if val1>val2: #greater than
                flag_dic["g"]=="1"
            if val1==val2: #equal to
                flag_dic["e"]=="1"

        else:
            if opcode=="01100" or "01101" or "01111" or "11111": #jump, flag not reset
                mem_addr=int(i[8:])
                label_addr=bintodec(mem_addr)
                
                if opcode=="01100" and flag_dic["l"]==1: #less than
                    new_machine_code=machine_code[label_addr+1:]
                    simulator(new_machine_code,regval,flag_dic)
                    break
                if opcode=="01101" and flag_dic["g"]==1: #greater than
                    new_machine_code=machine_code[label_addr+1:]
                    simulator(new_machine_code,regval,flag_dic)
                    break
                if opcode=="01111" and flag_dic["e"]==1: # equal to
                    new_machine_code=machine_code[label_addr+1:]
                    simulator(new_machine_code,regval,flag_dic)
                    break
                if opcode=="11111": # uncondtional jump
                    new_machine_code=machine_code[label_addr+1:]
                    simulator(new_machine_code,regval,flag_dic)
                    break
            else: #any other instruction, flag is reset after execution 
                main(i,var_dic)
                reset_flags()
        print(pc)
        print(regval)
        print(flag_dic)
        pc+=1    
    return

machine_code=['1001000100001010','1001001000001010','1111000000001010','0110000000000101','1000100001001010','1000000001001010','0101000000000000']
regnum={"000":"r0" , "001":"r1" , "010":"r2" , "011":"r3" , "100":"r4" , "101":"r5" , "110":"r6"}
regval={"r0":"0000000000000000" , "r1":"0000000000000000" , "r2":"0000000000000000" , "r3":"0000000000000000" , "r4":"0000000000000000" , "r5":"0000000000000000" , "r6":"0000000000000000"}
flag_dic={"v":"0" , "l":"0" , "g":"0" , "e":"0"}
var_dic={}
pc=1

simulator(machine_code,regval,flag_dic)
