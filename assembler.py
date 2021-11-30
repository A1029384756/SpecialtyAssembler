def fullAdd(A, B, cin):
	output = (bool(int(A))^bool(int(B))) ^ bool(int(cin))
	cout = (bool(int(A) and bool(int(B)))) or ((bool(int(A))^bool(int(B))) and bool(int(cin)))
	if output:
		output = "1"
	else:
		output = "0"

	if cout:
		cout = "1"
	else:
		cout = "0"
	return output, cout

def add3B(A, B):
	output = [0,0,0]
	carry = [0,0,0]
	output[2], carry[2] = fullAdd(A[2],B[2], "0")
	output[1], carry[1] = fullAdd(A[1],B[1], carry[2])
	output[0], carry[0] = fullAdd(A[0],B[0], carry[1])
	return ''.join(output)

def tokenToBinary(token):
	negative = False
	negativeValue = ""
	value = int(token)
	print("Token value: " + str(value))
	if value < 0:
		value *= -1
		negative = True
	output = ""
	while value >= 1:
		output = str(value % 2) + output
		value = int(value / 2)
	if negative:
		for char in output:
			if char == "0":
				negativeValue = negativeValue + "1"
			elif char == "1":
				negativeValue = negativeValue + "0"
		output = add3B(negativeValue, "001")



	return output;

def printList(list):
	for i in list:
		print(i)

def commandToHex(command):
	value = int(command, 2)
	output = hex(value)
	output = output[2:]
	for i in range(4 - len(output)):
		output = "0" + output
	return output

duoOpsA = ["MOVA","NOTA","NOTB","LD"]
duoOpsB = ["DIV4", "MOD8","INC2B","DEC2B","ST"]
trioOps = ["ADDAB","SUBAB","OR","XOR","SUBBA","ADDI","SUBI","ANDI","AND"]
instToOp = {"JMP":"1110000","BRNZ":"1100000", "ADDAB":"0000100", "SUBAB":"0001111","MOVA":"0001011","NOTA":"0000001","DIV4":"0000010","MOD8":"0001100","AND":"0001001","ADDI":"1000100","SUBI":"1001111","ANDI":"1001001","SUBBA":"0000011","INC2B":"0001101","DEC2B":"0000101","OR":"0001110","XOR":"0001010","NOTB":"0000110","LDI":"1001100","LD":"0010000","ST":"0100000"}

commandList = []
hexList = []

filename = input("Input the filepath for the program: ")

file = open(filename, "r")
lines = file.readlines()

for line in lines:
	line += " "
	opToken = ""
	token = ""
	command = ""
	count = 0
	for character in line:
		if not (character.isspace()):
			token += character;

		elif character == "\n":
			pass

		else:
			if token in instToOp.keys():
				command += instToOp[token]
				opToken = token
				print("Added token " + token)
				token = ""
			else:
				commandStr = tokenToBinary(token)
				print("Unedited token: " + commandStr)
				for i in range(3 - len(commandStr)):
					commandStr = "0" + commandStr

				if opToken == "BRNZ":
					if count == 0:
						command += commandStr
						count += 1
					else:
						for i in range(6 - len(commandStr)):
							commandStr = commandStr[0] + commandStr

						command = command[:7] + commandStr[:3] + command[7:] + commandStr[3:]
						count += 1

				elif opToken in trioOps:
					command += commandStr

				elif opToken in duoOpsA:
					if count < 1:
						command += commandStr

					else:
						command += commandStr + "000"
					count += 1

				elif opToken in duoOpsB:
					if count == 1:
						command += "000" + commandStr
					else:
						command += commandStr
					count += 1

				elif opToken == "JMP":
					command += "000" + commandStr + "000"

				print("Added token " + commandStr)
				token = ""

	print(command)
	print(len(command))
	commandList.append(command)

printList(commandList)

for command in commandList:
	hexList.append(commandToHex(command))

printList(hexList)
