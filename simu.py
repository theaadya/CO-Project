import sys

regnum={"000":"r0" , "001":"r1" , "010":"r2" , "011":"r3" , "100":"r4" , "101":"r5" , "110":"r6"}
regval={"r0":"0000000000000000" , "r1":"0000000000000000" , "r2":"0000000000000000" , "r3":"0000000000000000" , "r4":"0000000000000000" , "r5":"0000000000000000" , "r6":"0000000000000000"}
flag_dic={"v":"0" , "l":"0" , "g":"0" , "e":"0"}

s = sys.stdin.read()
machine_code = s.split("\n")
for i in range(machine_code.count("")):
    machine_code.remove("")

def reset_flags():
    for i in flag_dic.keys():
        flag_dic[i]="0"
def bintodec(n):
    n=str(n)
    if "." in n:
        ind=n.index(".")
        num1=bintodec(int(n[:(ind+1)]))
        pow=-1
        num2=0
        for j in n[(ind+1):]:
            b=int(j)
            num2+=b*(2**pow)
            pow-=1
        return (num1+num2)
    pow=0
    num=0
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

def ieeetodec(num):
    #input is string, output is num
    exp=num[:3]
    man=num[3:]
    exp=2**(bintodec(int(exp))-3)
    val="1"
    val+=man[:exp]
    val+="."
    if exp<len(man):
        val+=man[exp:]
    val=bintodec(float(val))
    return val

def dectoieee(num):
    #input is str, output is num

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
for i in machine_code:
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
            
    elif opcode=="10010" or opcode=="11000" or opcode=="11001":
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

    elif opcode=="10011" or opcode=="10111" or opcode=="11101" or opcode=="11110":
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
        else:
            val1=int(regval[regnum[reg1]])
            val2=int(regval[regnum[reg2]])
            if val1<val2:
                flag_dic["l"]="1"
            elif val1>val2:
                flag_dic["g"]="1"
            else:
                flag_dic["e"]="1"

    elif opcode=="10100" or opcode=="10101":
        #type_d
        reg1=i[5:8]
        mem_addr=int(i[8:16])
        mem_addr=bintodec(mem_addr)
    elif opcode=="11111" or opcode=="01100" or opcode=="01101" or opcode=="01111":
        #type_e
        mem_addr=int(i[8:16])
        mem_addr=bintodec(mem_addr)
    elif opcode=="00000" or opcode=="00001" or opcode=="00010":
        reg1=i[7:10]
        reg2=i[10:13]
        reg3=i[13:16]
        if opcode=="00000":#f_add
            val1=regval[regnum[reg1]][-8:]
            val2=regval[regnum[reg2]][-8:]
            val=dectoieee(ieeetodec(val1)+ieeetodec(val2))
            #check for range and put value in reg3
            # diff=8-len(val)
            # if diff<0:
            #     regval[regnum[reg3]]="0"+val[-8:]
            #     flag_dic["v"]="1"
            # else:
            #     regval[regnum[reg3]]=("0"*(8+diff))+val
        elif opcode=="00001":
            val1=regval[regnum[reg1]][-8:]
            val2=regval[regnum[reg2]][-8:]
            val=ieeetodec(val1)-ieeetodec(val2)
            #check for range everywhere
            if val<0:
                regval[regnum[reg3]]="0"*16
                flag_dic["v"]="1"
            else:
                val3=dectoieee(val)
                regval[regnum[reg3]]=("0"*(16-len(val3)))+val3

        else:
            #f_mov
            reg1=i[5:8]
            imm=i[8:]   #check for range
            #check for invalid
            imm=dectoieee(imm)
            regval[regnum[reg1]]=("0"*(16-len(imm)))+imm

    #elif opcode=="01010":
        #hlt
        
# code for printing memory
var_mem = []
zero_str = "0000000000000000"
for i in machine_code:
    if i[:5] == "10100" or i[:5] == "10101":
        var_mem.append("00000000"+i[8:])
    print(i, end = "\n")
for i in range(len(var_mem)):
    print(var_mem[i], end = "\n")
zero_nums = 256 - (len(machine_code) + len(var_mem))
for i in range(zero_nums):
    print(zero_str, end = "\n")
