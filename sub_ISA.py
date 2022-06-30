
# Main
opcode_dic={"sub":"10001", "rs":"11000", "ls":"11001", "and":"11100", "not":"11101", "hlt":"01010"}

with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}

machine_code_sub=""
words=lines.split()
if words[0]=="sub":
 	key_o=words[0]
 	machine_code_sub+=opcode_dic[key]

 	for i in range(1,4):
 		key_r=words[i][3]
 		machine_code_sub+=reg_dic[key]

with open('mach_code.txt', 'w') as f:
	f.write(machine_code_sub)


