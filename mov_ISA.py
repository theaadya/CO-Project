opcode_dic={"cmp":"11110", "mov":"10010", "ld":"10100", "st":"10101"}

with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}

machine_code_mov=""
words=lines.split() 

if words[0]=="mov":
    if type(words[2]) == str:
        #check if error handling
	    key_o=words[0]
	    machine_code_mov+=opcode_dic[key_o]
	    for i in range(1,3):
		    key_r=words[i][3]
		    machine_code_mov+=reg_dic[key_r]
    elif type(words[2]) == int:
        if 0 <= words[2] <= 255:
            key_o=words[0]
	        machine_code_mov+=str(int(opcode_dic[key_o])+1)
            machine_code_mov+=reg_dic[words[1]]

            #length adjustment to 16 bits
            newdectobin=str(dectobin(words[2]))
            newdectobin+=[(8-len(newdectobin))*"0"]
            machine_code_mov+=newdectobin
        else:
            print("Error: Number too large")

print(machine_code_mov)