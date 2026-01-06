import time
import os

user_time = int(input("Enter the seconds: "))


for i in range(user_time):
    os.system("cls")
    print("Remaining:", user_time - i)
    time.sleep(1)
    
os.system("cls")
print("Finish", end='')