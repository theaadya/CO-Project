opcode_dic={"cmp":"11110", "mov":"10010", "ld":"10100", "st":"10101"}
with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}
machine_code_st=""
words=lines.split() 

if words[0]=="ld":
    with open("as_code.txt","r") as f:
        num=0
        lines=f.readlines()
        for i in range(len(lines)):
            words=lines[i].split()
            if (words[0]!="var" and words[0]!="/n" and words[0]!=" "):
                num+=1

    machine_code_st+=opcode_dic["st"]
    machine_code_st+=reg_dic[words[1]]
    machine_code_st+=str(dectobin(num))
