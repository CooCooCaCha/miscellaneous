import hashlib
import string

hashLength = 10
charToRemove = '' + string.punctuation
userName = ''
pinNumber = '1234'

def computePassword(stringToHash):
	hasher = hashlib.sha512()
	newString = stringToHash + userName + pinNumber
	hasher.update(newString.encode())
	hashedString = hasher.hexdigest()
	hashedString = hashedString.translate(str.maketrans('','',charToRemove))[0:hashLength]
	return hashedString

passDict = {}

exit = False

print("Commands:")
print("1 - New Entry")
print("2 - List Entries")
print("3 - Delete Entry")
print("4 - Recompute Entries")
print("5 - Set Username")
print("6 - Set Pin")
print("0 - Exit")

try:
	while(exit == False):
		com = input("Command ->")
		
		if com == "0":
			exit = True
		elif com == "1":
			newEntry = input("New Entry ->")
			passDict[newEntry] = computePassword(newEntry)
		elif com == "2":
			keyList = list(passDict.keys())
			print("Entries:")
			for x in keyList:
				print("Entry:" + x + " Password:" + passDict[x])
		elif com == "3":
			delEntry = input("Name of Entry to Delete ->")
			del passDict[delEntry]
		elif com == "4":
			keyList = list(passDict.keys())
			for x in keyList:
				passDict[x] = computePassword(x)
			print("Done")
		elif com == "5":
			userName = input("New Username ->")
			print("Username Set To: " + userName);
		elif com == "6":
			pinNumber = input("New Pin ->")
			print("Pin Set To: " + pinNumber);
		
except Exception as e:
	print(e)