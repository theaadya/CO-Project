opcode_dic={"sub":"10001", "rs":"11000", "ls":"11001", "and":"11100", "not":"11101", "hlt":"01010"}

with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}

machine_code_and=""
words=lines.split() 

if words[0]=="and":
	key_o=words[0]
	machine_code_and+=opcode_dic[key_o]
	machine_code_and+="00"

	for i in range(1,4):
		key_r=words[i][3]
		machine_code_and+=reg_dic[key_r]

print(machine_code_and)
