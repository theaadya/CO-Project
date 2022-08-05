import math as m

n=input("Enter the number for required operation \n1.ISA and Instruction Related \n2.System Enhancement Type-A \n3.System Enhancement Type-B\n")
val=""
unit=""
if n=='1' or n=='2':
    space=input("Enter space in memory with units  ")
    mem_type=int(input("Enter the number corresponding to memory addressable type \n1.Bit Adressable Memory \n2.Nibble Adressable Memory \n3.Byte Adressable Memory \n4.Word Adressable Memory\n"))
    for i in space:
        if i.isalpha():
            unit+=i
        else:
            val+=i
    val=int(val)
    unit_dic={'KB':1024*8, 'MB':((1024**2)*8), 'GB':((1024**3)*8), 'TB':((1024*4)*8), 'Kb':1024, 'Mb':(1024**2), 'Gb':(1024**3), 'Tb':(1024**4), 'kWord':1024, 'mWord':(1024**2), 'gWord':(1024**3), 'tWord':(1024**4)}
    word_dic={'kWord':1024, 'mWord':(1024**2), 'gWord':(1024**3), 'tWord':(1024**4)}
    
    mem_dic={1:1,2:4,3:8,}
    if mem_type!=4:
        tot_space=(val)*(unit_dic[unit])
        address=tot_space/(mem_dic[mem_type])
        p_address=int(m.log(address,2))
    else:
        cpu_bits=int(input("Input number of bits of CPU "))
        if unit in word_dic:
            tot_space=(val*(word_dic[unit])*cpu_bits)
            address=tot_space/cpu_bits
            p_address=int(m.log(address,2))
        else:
            tot_space=(val)*(unit_dic[unit])
            address=tot_space/cpu_bits
            p_address=int(m.log(address,2))

    if n=='1':
        len_inst=int(input("Enter the length of instruction in bits  "))
        len_reg=int(input("Enter the length of register in bits  "))    
        q_opcode=(len_inst-len_reg)-p_address
        filler=len_inst-(2*(len_reg))-q_opcode
        num_inst=2**(q_opcode)
        num_reg=2**(len_reg)
        print("The minimum number of bits to represent an address in this architecture is",p_address )
        print("Number of bits needed by opcode are",q_opcode)
        print("Number of filler bits in Instruction type 2 are", filler)
        print("Maximum number of instructions the ISA can support are", num_inst)
        print("Maximum number of registers this ISA can support is", num_reg)

    if n=='2':
        bits_cpu=int(input("Enter the number of bits of CPU "))
        mem_type2=int(input("Enter the number corresponding to current addressable memory type \n1.Bit Adressable Memory \n2.Nibble Adressable Memory \n3.Byte Adressable Memory \n4.Word Adressable Memory\n"))
        if mem_type2!=4:
            address2=tot_space/(mem_dic[mem_type2])
            p_address2=int(m.log(address2,2))
        else:
            address2=tot_space/bits_cpu
            p_address2=int(m.log(address2,2))
        print(p_address2-p_address)

if n=='3':
    mem_dic={1:1,2:4,3:8,}
    cpu_bits1=int(input("Enter the number of bits in CPU "))
    address_pins=int(input("Enter the number of address pins "))
    mem_type3=int(input("Enter the number corresponding to memory addressal type \n1.Bit Adressable Memory \n2.Nibble Adressable Memory \n3.Byte Adressable Memory \n4.Word Adressable Memory\n"))
    if mem_type3!=4:
        total_address_bits=2**address_pins
        total_mem_bits=total_address_bits*(mem_dic[mem_type3])
    if mem_type3==4:
        total_address_bits=2**address_pins
        total_mem_bits=total_address_bits*(cpu_bits1)
    
    total_mem_bytes=int(total_mem_bits/8)
    range_value=m.log(total_mem_bytes,2)
    if range_value<10:
        print(f'{total_mem_bytes} bytes')
    elif range_value>=10 and range_value<20:
        total_mem_kilobytes=int(total_mem_bytes/1024)
        print(f'{total_mem_kilobytes} KB')
    elif range_value>=20 and range_value<30:
        total_mem_megabytes=int(total_mem_bytes/(1024**2))
        print(f'{total_mem_megabytes} MB')
    elif range_value>=30 and range_value<40:
        total_mem_gigabytes=int(total_mem_bytes/(1024**3))
        print(f'{total_mem_gigabytes} GB')
    else: #range value more than equal to 40
        total_mem_terabytes=int(total_mem_bytes/(1024**4))
        print(f'{total_mem_terabytes} TB')  
