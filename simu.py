def bintodec(n):
    num=0
    n=str(n)
    pow=0
    for i in n[::-1]:
        b=int(i)
        num+=((2**(pow))*b)
        pow+=1
    return num
for i in bin_list:
    opcode=i[:5]
    if opcode=="10000" or opcode=="10001" or opcode=="10110" or opcode=="11010" or opcode=="11011" or opcode=="11100":
        #type_a
        reg1=i[7:10]
        reg2=i[10:13]
        reg3=i[13:16]
    elif opcode=="10010" or opcode=="11000" or opcode=="11001":
        #type_b
        reg1=i[5:8]
    elif opcode=="10011" or opcode=="10111" or opcode=="11101" or opcode=="11110":
        #type_c
        reg1=i[10:13]
        reg2=i[13:16]
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
