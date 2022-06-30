def DecBin(string):
    #checking if number is decimal
    if string.isdigit():
        lst=[int(i) for i in string]
        for i in lst:
            if i>=0 and i<=9:
                Flag=True
            else:
                Flag=False
                break
    else:
        Flag=False

    Flag1=True

    if int(string)>=255 or int(string)<=0:
    	Flag1=False
  

    #converting decimal to binary
    if Flag and Flag1:
        num=int(string)
        Bnumlst=[]
        q=1
        while q!=0:
            q=num//2
            Bnum=num%2
            Bnumlst.append(Bnum)
            num=q
        zeroes=8-len(Bnumlst)
        for i in range(zeroes):
        	Bnumlst.append(0)
        Bnumlst.reverse()
        Anslst=[str(i) for i in Bnumlst]
        Binary_Number="".join(Anslst)
        return(Binary_Number)

    if not(Flag or Flag1):
        return("Enter the correct number")

# Main
opcode_dic={"sub":"10001", "rs":"11000", "ls":"11001", "and":"11100", "not":"11101", "hlt":"01010"}

with open("as_code.txt", "r") as f:
	lines=f.readline()

reg_dic={'0':'000', '1':'001', '2':'010', '3':'011', '4':'100', '5':'101', '6':'110'}

machine_code_rs=""
words=lines.split() 

if words[0]=="rs":
	key_o=words[0]
	machine_code_rs+=opcode_dic[key_o]

	key_r=words[1][3]
	machine_code_rs+=reg_dic[key_r]

	Imm=""
	for i in range(1,len(words[2])):
		Imm+=words[2][i]

	Immb=DecBin(Imm)
	machine_code_rs+=Immb

print(machine_code_rs)