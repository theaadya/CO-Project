opcode_dic={"sub":"10001", "rs":"11000", "ls":"11001", "and":"11100", "not":"11101", "hlt":"01010"}

with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}

machine_code_not=""
words=lines.split() 

if words[0]=="not":
	key_o=words[0]
	machine_code_not+=opcode_dic[key_o]
	machine_code_not+="00000"

	for i in range(1,3):
		key_r=words[i][3]
		machine_code_not+=reg_dic[key_r]

print(machine_code_not)
