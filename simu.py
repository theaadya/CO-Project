regnum={"000":"r0" , "001":"r1" , "010":"r2" , "011":"r3" , "100":"r4" , "101":"r5" , "110":"r6"}
regval={"r0":"0000000000000000" , "r1":"0000000000000000" , "r2":"0000000000000000" , "r3":"0000000000000000" , "r4":"0000000000000000" , "r5":"0000000000000000" , "r6":"0000000000000000"}
def bintodec(n):
    num=0
    n=str(n)
    pow=0
    for i in n[::-1]:
        b=int(i)
        num+=((2**(pow))*b)
        pow+=1
    return num

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
for i in bin_list:
    opcode=i[:5]
    if opcode=="10000" or opcode=="10001" or opcode=="10110" or opcode=="11010" or opcode=="11011" or opcode=="11100":
        #type_a
        reg1=i[7:10]
        reg2=i[10:13]
        reg3=i[13:16]
        if opcode=="10000":
            val3=str(int(regval[regnum[reg1]]) + int(regval[regnum[reg2]]))
            regval[regnum[reg3]]=("0"*(16-len(val3)))+val3
        elif opcode=="10001":
            val1=int(regval[regnum[reg1]])
            val2=int(regval[regnum[reg2]])
            if val2>val1:
                regval[regnum[reg3]]="0000000000000000"
                #set overflow flag
            else:
                val3=str(val1-val2)
                regval[regnum[reg3]]=("0"*(16-len(val3)))+val3
        elif opcode=="10110":#multiply
        elif opcode=="11010":#bitwise xor
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
#           diff=len(val1)-len(val2)
#           if diff>0:
#               val2=("0"*diff)+val2
#           elif diff<0:
#               val1=("0"*diff)+val1
            val3=""
            for i in range(16):
#           for i in range(len(val1)):
                val3+=perform_xor(val1[i],val2[i])
            #regval[regnum[reg3]]=("0"*(16-len(val3)))+val3
            regval[regnum[reg3]]=val3
        elif opcode=="11011":#bitwise or
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
#           diff=len(val1)-len(val2)
#           if diff>0:
#               val2=("0"*diff)+val2
#           elif diff<0:
#               val1=("0"*diff)+val1
            val3=""
            for i in range(16):
#           for i in range(len(val1)):
                val3+=perform_or(val1[i],val2[i])
            regval[regnum[reg3]]=val3
        else:#bitwise and
            val1=regval[regnum[reg1]]
            val2=regval[regnum[reg2]]
#           diff=len(val1)-len(val2)
#           if diff>0:
#               val2=("0"*diff)+val2
#           elif diff<0:
#               val1=("0"*diff)+val1
            val3=""
            for i in range(16):
#           for i in range(len(val1)):
                val3+=perform_and(val1[i],val2[i])
            regval[regnum[reg3]]=val3
    elif opcode=="10010" or opcode=="11000" or opcode=="11001":
        #type_b
        reg1=i[5:8]

    elif opcode=="10011" or opcode=="10111" or opcode=="11101" or opcode=="11110":
        #type_c
        reg1=i[10:13]
        reg2=i[13:16]
        if opcode=="11101":
            notval1=""
            for i in range(16)
#           for i in range(len(regval[regnum[reg1]])):
                notval1+=perform_not(regval[regnum[reg1]])
            regval[regnum[reg2]]=not_val1
    elif opcode=="10100" or opcode=="10101":
        #type_d
        reg1=i[5:8]
        mem_addr=int(i[8:16])
        mem_addr=bintodec(mem_addr)
    elif opcode=="11111" or opcode=="01100" or opcode=="01101" or opcode=="01111":
        #type_e
        mem_addr=int(i[8:16])
        mem_addr=bintodec(mem_addr)
    elif opcode=="01010":
        #hlt
