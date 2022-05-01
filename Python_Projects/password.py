import stdiomask  #for password 
pswd = stdiomask.getpass("\ncreate password:") #getpass() for input password default print * for character if you want to change use getpass(mask="")
p = input("Enter Password:")
if p==pswd:
    print("Welcome")
else:
    print("Wronge password")