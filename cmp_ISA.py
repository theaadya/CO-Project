#cmp
opcode_dic={"cmp":"11110", "mov":"10010", "ld":"10100", "st":"10101"}
with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}

machine_code_cmp=""
words=lines.split() 

if words[0]=="cmp":
	machine_code_cmp+=opcode_dic["cmp"]
    newl=[]
	for i in range(1,3):
		key_r=words[i][3]
		machine_code_cmp+=reg_dic[key_r]
        newl.append(key_r)
    #if newl[0]==newl[1]:flag
        

print(machine_code_cmp)