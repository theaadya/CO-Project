opcode_dic={"sub":"10001", "rs":"11000", "ls":"11001", "and":"11100", "not":"11101", "hlt":"01010"}

with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}

machine_code_hlt=""
words=line.split()

if words[0]=="hlt":
	key_o=words[0]
	machine_code_hlt+=opcode_dic[key_o]

print(machine_code_hlt)