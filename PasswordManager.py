import os,configparser,pandas as pd,math,time,sys,getpass

#Global Varaibles
AccountDetails=''
PasswordDetails=''


def main():
	#initialize global varaibles and initial Login for Password Manager
	Selection=initialize()
	os.system("cls")
	#Depending upon user selection choose to Sign Up,Login or Quit
	if Selection == '1':
		signup('')
	elif Selection=='2':
		login()
	elif Selection=='-admin':
		print("Admin Access .")
		PWD=getpass.getpass("Admin Password :")
		if PWD=='admin':
			admin()
		else:
			print("Incorrect PAssword !!!")
			input("Press any Key to Continue...")
			main()
	else:
		os.system("cls")
		print("\n##############################################################\n")
		print("Program Ended . . .")
		print("\n##############################################################\n")
		input("Press any Key to Exit . . .")
		exit()


#Function to Initialize the Password Manager	
def initialize():
	#display Settings
	os.system("title Password Manager")
	os.system("color 06")
	os.system("cls")
	
	#initialize global variables
	global AccountDetails,PasswordDetails
	
	#set Working Directory and assign values from config.ini file
	WorkingDirectory=os.getcwd()
	
	#development purpose with notepad++
	#WorkingDirectory="C:\\Users\\Priyank\\Desktop\\PassWordManager-Python"
	#os.chdir("C:\\Users\\Priyank\\Desktop\\PassWordManager-Python")
	
	ConfigFilePath=WorkingDirectory+"\\config.ini"
	settings = configparser.ConfigParser()
	settings._interpolation = configparser.ExtendedInterpolation()
	settings.read(ConfigFilePath)
	AccountDetails=settings.get('General', 'AccountDetails')
	PasswordDetails=settings.get('General', 'PasswordDetails')
	AccountDetails=WorkingDirectory+"\\Data\\"+AccountDetails
	PasswordDetails=WorkingDirectory+"\\Data\\"+PasswordDetails
	
	#initialize the Program
	print("\n##############################################################")
	print("#                     Password Manager                       #")
	print("##############################################################\n")
	print("1:Sign Up")
	print("2:Login")
	print("3:Exit \n")
	print("Develpment purpose: type '-admin' for Administrator Access (Password:admin)\n")
	Selection=input("Please select one option : ")
	#Validation
	while Selection not in ['1','2','3','-admin']:
		print("ERROR: Invalid Selection !!!")
		Selection=input("Please select one option : ")	
	print("\n##############################################################\n")
	
	return Selection

#Function to Perform Sign Up Activities
def signup(Mode):
	print("\n##############################################################")
	print("#                         Sign Up                            #")
	print("##############################################################\n")
	UserName=input("Enter Your Name : ")
	global AccountDetails
	UserName=validationAccountUnique(AccountDetails,UserName,'')
	PassWord=getpass.getpass("Enter Your Password : ")

	
	#Read and Update the File
	Accounts=READ_CSV(AccountDetails)
	#print("Before Append",Accounts)
	Accounts=Accounts.append({'AccountName':UserName,'Password':PassWord}, ignore_index=True)
	#print("After Append",Accounts)
	TO_CSV(Accounts,AccountDetails)
	print("You have sucessfully created your Account")
	print("\n##############################################################\n")
	input("Enter to Continue...")
	os.system("cls")
	if Mode in [1,'1']:
		admin()
	else:
		main()

def admin():
	print("\n##############################################################")
	print("#                       Administror                          #")
	print("##############################################################\n")		
	
	print("Accounts : \n")

	#Get Account Details for User
	global PasswordDetails,AccountDetails
	AccDetails=READ_CSV(AccountDetails)
	#Display Details of Accounts
	print(AccDetails[['AccountName','Password']],"\n")
	
	print("\n##############################################################")
	print("#                     Account Manager                       #")
	print("##############################################################\n")
	print("1:View Account")
	print("2:Add Account")
	print("3:Modify Account")
	print("4:Delete Account")
	print("5:Log Out")
	print("6:Exit \n")
	Sel=input("Please select one option : ")
	#Validation
	while Sel not in ['1','2','3','4','5','6']:
		print("ERROR: Invalid Selection !!!")
		Sel=input("Please select one option : ")	
	
	print("\n##############################################################\n")

	
	#Perform Actions Accordingly
	if Sel == '1':
		UserName=input("Enter Name : ")
		print("\n##############################################################\n")
		os.system("cls")
		ViewAccounts(UserName,'1')
		
	elif Sel == '2':
		signup('1')
	elif Sel == '3':
		UserName=input("Enter Name : ")
		UserName=validationAccount(AccountDetails,UserName,'')
		print("\n##############################################################\n")
		os.system("cls")
		ModifyUser(UserName)
	elif Sel == '4':
		UserName=input("Enter Name : ")
		UserName=validationAccount(AccountDetails,UserName,'')
		print("\n##############################################################\n")
		os.system("cls")
		DeleteUser(UserName)
	elif Sel == '5':
		main()
	else:	
		os.system("cls")
		print("\n##############################################################\n")
		print("Program Termineted")
		print("\n##############################################################\n")
		input("Press any Key to Exit . . .")
		exit()

def DeleteUser(UserName):
	print("\n##############################################################")
	print("#                 Delete Account User                        #")
	print("##############################################################\n")
	print("Account : ",UserName)
	global AccountDetails,PasswordDetails
	AccPassDetails=READ_CSV(AccountDetails)
	PassDetails=READ_CSV(PasswordDetails)
	print("\nCurrent User :")
	print(AccPassDetails[ (AccPassDetails['AccountName'] == UserName) ])
	print("\nCurrent Accounts :")
	print(PassDetails[ (PassDetails['AccountUser'] == UserName) ])
	print("\nAre you Sure you want to delete Account (",UserName,") ? (Y)es/(N)o ",sep='')
	Choice=input("( (Y)es/(N)o) >>")
	while Choice not in ['Y','y','N','n']:
		print("Error:Incorrect Choice!!")
		Choice=input("( (Y)es/(N)o) >>")
	if Choice in ['Y','y']:
		AccPassDetails=AccPassDetails[ (AccPassDetails['AccountName'] != UserName)]
		TO_CSV(AccPassDetails,AccountDetails)
		PassDetails=PassDetails[ (PassDetails['AccountUser'] != UserName)]
		TO_CSV(PassDetails,PasswordDetails)
		print("\nYou have sucessfully Deleted the Account")
	else:
		print("\nAccount Deletion Cancelled !!!")
	print("\n##############################################################\n")
	input("Enter to Continue...")
	os.system("cls")
	admin()
	
		
		
def ModifyUser(UserName):
	print("\n##############################################################")
	print("#                 Modify Account User                        #")
	print("##############################################################\n")
	
	print("Account : ",UserName)
	global AccountDetails
	
	AccPassDetails=READ_CSV(AccountDetails)
	print("Current Values :")
	print(AccPassDetails[ (AccPassDetails['AccountName'] == UserName) ])
	
	AccountPass=input("\nEnter Your New Account Password : ")
	
	#Remove the Account to be modified
	AccPassDetails=AccPassDetails[ (AccPassDetails['AccountName'] != UserName)]
	
	#Append the modified Results
	AccPassDetails=AccPassDetails.append({'AccountName':UserName,'Password':AccountPass}, ignore_index=True)
	TO_CSV(AccPassDetails,AccountDetails)
	print("\nYou have sucessfully Updated your Account")	
	print("\n##############################################################\n")
	input("Enter to Continue...")
	os.system("cls")
	admin()
	
	
#Function to Validate the Account Name Uniqueness	
def validationAccountUnique(FileName,Value,Value2):
	if Value2=='':
		DataFrame=READ_CSV(FileName)
		Flag=any(DataFrame.AccountName == Value)
		while Flag==True:
			print("Error: AccountName (",Value,") Already Exists",sep ='')
			Value=input("Enter Your Account Name :")
			Flag=any(DataFrame.AccountName == Value)
	else:
		DataFrame=READ_CSV(FileName)
		Flag=any((DataFrame.AccountName == Value) & (DataFrame.AccountUser == Value2))
		while Flag==True:
			print("Error: AccountName (",Value,") Already Exists for User (",Value2,")",sep ='')
			Value=input("Enter Your Account Name :")
			Flag=any((DataFrame.AccountName == Value) & (DataFrame.AccountUser == Value2))
	
	return(Value)

#Function to Validate the Account Name Presence	
def validationAccount(FileName,Value,Value2):
	if Value2=='':
		DataFrame=READ_CSV(FileName)
		Flag=any(DataFrame.AccountName == Value)
		while Flag==False:
			print("Error: AccountName (",Value,") Does Not Exists",sep ='')
			Value=input("Enter Your Account Name :")
			Flag=any(DataFrame.AccountName == Value)
	else:
		DataFrame=READ_CSV(FileName)
		Flag=any((DataFrame.AccountName == Value) & (DataFrame.AccountUser == Value2))
		while Flag==False:
			print("Error: AccountName (",Value,") Does Not Exists for User (",Value2,")",sep ='')
			Value=input("Enter Your Account Name :")
			Flag=any((DataFrame.AccountName == Value) & (DataFrame.AccountUser == Value2))
	
	return(Value)	
	
#Function to Login an User	
def login():
	print("\n##############################################################")
	print("#                         Login                              #")
	print("##############################################################\n")
	global AccountDetails
	UserName=input("Enter Your Name : ")
	UserName=validationAccount(AccountDetails,UserName,'')
	
	#Getting the Key and Password Values
	Accounts=READ_CSV(AccountDetails)
	CurrentUser=Accounts[(Accounts['AccountName'] == UserName)]
	CurrentPassword=CurrentUser[['Password']].to_string(header=False,index=False).lstrip()


	PassWord=getpass.getpass("Enter Your Password : ")
	#Password Validation
	MinAttempt=1
	MaxAttempt=3
	
	while PassWord != CurrentPassword:
		print("Error: Incorrect Password , Attempt:",(MinAttempt)," Attempt Left :",(MaxAttempt-MinAttempt))
		PassWord=getpass.getpass("Enter Your Correct Password : ")
		MinAttempt+=1
		if MinAttempt>MaxAttempt:
			os.system("cls")
			print("Too Many Unsucessfull Attempts")
			print("Terminate Program.")
			print("##############################################################\n")
			exit()
	
	print("Login Sucessfully")
	print("##############################################################\n")
	
	os.system("cls")
	ViewAccounts(UserName,'')
	
def ViewAccounts(UserName,Mode):
	print("\n##############################################################")
	print("#                    Account Details                         #")
	print("##############################################################\n")
	
	print("Account User Name : ",UserName)

	#Get Account Details for User
	global PasswordDetails
	AccPassDetails=READ_CSV(PasswordDetails)
	#filter Rows
	AccPassDetails=AccPassDetails[(AccPassDetails['AccountUser'] == UserName)]
	#Display required Details for USer
	print(AccPassDetails[['AccountName','UserName','Password']],"\n")
	
	print("\n##############################################################")
	print("#                    Account Options                         #")
	print("##############################################################\n")
	print("1:Add Another Account")
	print("2:Modify Account Password")
	print("3:Delete Account ")
	print("4:Logout ")
	print("5:Exit\n")
	AccountOption=input("Please select one option : ")
	#Validation
	while AccountOption not in ['1','2','3','4','5']:
		print("ERROR: Invalid Selection !!!")
		AccountOption=input("Please select one option : ")
	
	print("\n##############################################################\n")
	os.system("cls")
	
	#Choose Functions based on Selection
	if AccountOption == '1':
		AddAccount(UserName)
	elif AccountOption == '2':
		ModAccount(UserName)
	elif AccountOption == '3':
		DelAccount(UserName)
	elif AccountOption == '4':
		if Mode in [1,'1']:
			admin()
		else:
			main()
	else:	
		os.system("cls")
		print("\n##############################################################\n")
		print("Program Termineted")
		print("\n##############################################################\n")
		input("Press any Key to Exit . . .")
		exit()
	
	
def AddAccount(UserName):
	print("\n##############################################################")
	print("#                     Add Account                            #")
	print("##############################################################\n")
	AccountName=input("Enter Your New Account Name : ")
	#Validation
	global PasswordDetails
	AccountName=validationAccountUnique(PasswordDetails,AccountName,UserName)
	
	AccountUser=input("Enter Your New Account User Name : ")
	AccountPass=getpass.getpass("Enter Your New Account Password : ")
	
	#Update File with new Account
	AccPassDetails=READ_CSV(PasswordDetails)
	AccPassDetails=AccPassDetails.append({'AccountUser':UserName,'AccountName':AccountName,'UserName':AccountUser,'Password':AccountPass}, ignore_index=True)
	TO_CSV(AccPassDetails,PasswordDetails)
	print("\nYou have sucessfully Added your Account")
	print("\n##############################################################\n")
	input("Enter to Continue...")
	os.system("cls")
	
	ViewAccounts(UserName,'')
	

def ModAccount(UserName):	
	print("\n##############################################################")
	print("#                     Modify Account                         #")
	print("##############################################################\n")
	
	AccountName=input("Enter Your Account Name : ")
	#Validation
	global PasswordDetails
	AccountName=validationAccount(PasswordDetails,AccountName,UserName)
	
	
	AccPassDetails=READ_CSV(PasswordDetails)
	print("Current Values :")
	print(AccPassDetails[ (AccPassDetails['AccountUser'] == UserName) &(AccPassDetails['AccountName'] == AccountName) ])

	AccountUser=input("\nEnter Your New Account User Name : ")
	AccountPass=getpass.getpass("Enter Your New Account Password : ")
	
	#Store other Accounts Details
	AccPassDetailsOthers=AccPassDetails[ (AccPassDetails['AccountUser'] != UserName)]
	#Remove the Account to be modified
	AccPassDetails=AccPassDetails[ (AccPassDetails['AccountUser'] == UserName) & (AccPassDetails['AccountName'] != AccountName) ]
	
	#Append the other Accounts details
	AccPassDetails=AccPassDetails.append(AccPassDetailsOthers)
	#Append the modified Results
	AccPassDetails=AccPassDetails.append({'AccountUser':UserName,'AccountName':AccountName,'UserName':AccountUser,'Password':AccountPass}, ignore_index=True)
	TO_CSV(AccPassDetails,PasswordDetails)
	print("\nYou have sucessfully Updated your Account")	
	print("\n##############################################################\n")
	input("Enter to Continue...")
	os.system("cls")
	
	ViewAccounts(UserName,'')

	
def DelAccount(UserName):
	print("\n##############################################################")
	print("#                     Delete Account                         #")
	print("##############################################################\n")
	AccountName=input("Enter Your Account Name : ")
	#Validation
	global PasswordDetails
	AccountName=validationAccount(PasswordDetails,AccountName,UserName)	
	
	AccPassDetails=READ_CSV(PasswordDetails)
	#Store other Accounts Details
	AccPassDetailsOthers=AccPassDetails[ (AccPassDetails['AccountUser'] != UserName)]
	#Remove the Account to be modified
	AccPassDetails=AccPassDetails[ (AccPassDetails['AccountUser'] == UserName) & (AccPassDetails['AccountName'] != AccountName) ]
	
	#Append the other Accounts details
	AccPassDetails=AccPassDetails.append(AccPassDetailsOthers)
	TO_CSV(AccPassDetails,PasswordDetails)
	print("\nYou have sucessfully Deleted your Account")	
	print("\n##############################################################\n")
	input("Enter to Continue...")
	os.system("cls")
	
	ViewAccounts(UserName,'')

def READ_CSV(FileName):
	Cipher(FileName,'decrypt')
	Value=pd.read_csv(FileName)
	Cipher(FileName,'encrypt')
	return Value
	
def TO_CSV(DataFrame,FileName):
	Cipher(FileName,'decrypt')
	DataFrame.to_csv(FileName,index=False)
	Cipher(FileName,'encrypt')

#Encryption
def encryptMessage(Key, Message):
    CipherText = [''] * Key

    for col in range(Key):
        pointer = col

        while pointer < len(Message):
            CipherText[col] += Message[pointer]
            pointer += Key

    return ''.join(CipherText)

#Decryption
def decryptMessage(key, message):

    NumOfColumns = math.ceil(len(message) / key)
    NumOfRows = key
    NumOfShadedBoxes = (NumOfColumns * NumOfRows) - len(message)
    PlainText = [''] * NumOfColumns

    col = 0
    row = 0

    for symbol in message:
        PlainText[col] += symbol
        col += 1 

        if (col == NumOfColumns) or (col == NumOfColumns - 1 and row >= NumOfRows - NumOfShadedBoxes):
            col = 0
            row += 1

    return ''.join(PlainText)

#Cipher File
def Cipher(FileName,Mode):

    myKey = 10
    myMode = Mode # set to 'encrypt' or 'decrypt'

    # If the input file does not exist, then the program terminates early.
    if not os.path.exists(FileName):
        print('The file %s does not exist. Quitting...' % (FileName))
        sys.exit()

    FileObj = open(FileName)
    Content = FileObj.read()
    FileObj.close()

    StartTime = time.time()
    if myMode == 'encrypt':
        Translated = encryptMessage(myKey, Content)
    elif myMode == 'decrypt':
        Translated = decryptMessage(myKey, Content)
    TotalTime = round(time.time() - StartTime, 2)

    outputFileObj = open(FileName, 'w')
    outputFileObj.write(Translated)
    outputFileObj.close()
	
main()