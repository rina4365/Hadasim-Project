import re
import os
from collections import OrderedDict
from datetime import datetime



date_pattern = r"\b\d{2}/\d{2}/\d{4} \d{2}\b"
number_pattern = r"\b\d{1,6}\.\d{0,3}\b"
time_list = dict()
my_set = set()


def add_to_list(date, number):
        num = float(number)
        if date in time_list.keys():
            a,b = time_list[date]
            if isinstance(a, (int)):
                a = a + 1
                b = b + num
            else:
                b = b + 1 
                a = a + num
            time_list[date] = {b,a}
        else:
            time_list[date] = {num,1}


def remove_duplicates(data):
    lines = data.splitlines(True)
    for line in lines:
        my_set.add(line)


def check_number(split_data):
    if len(split_data) == 3 and split_data[2].isdigit():
        return True
    return False
   




def validate_data(data):
    remove_duplicates(data)
    for line in my_set:
        date_line = re.search(date_pattern,line)#validate date
        split_data = line.split() 
        date_line_num = re.findall(number_pattern,line)#validate if there is number
        if date_line:
            if check_number(split_data):
                add_to_list(date_line.group(0), split_data[2])
            elif date_line_num:
                add_to_list(date_line.group(0), date_line_num[0])
           


def readFile(file_path):
    file = open(file_path, "r")
    print("read file")
    data = file.read()
    if not data:
        print("empty")
        return
    validate_data(data) 
    

def printfile():
    sorted_data = OrderedDict(sorted(time_list.items(), key=lambda x: datetime.strptime(x[0], "%d/%m/%Y %H")))
    for key,value in sorted_data.items():
        a,b = value
        if isinstance(a, (int)):
            ave = b / a
        else:
            ave = a / b

        print(f"start time: {key}:00:00, average: {round(ave,1)}")



def main():
    file_path = r"C:\Users\User\Desktop\first question\targilB\time_series.txt"
    if os.path.exists(file_path):
        print("File found!")
    else:
        print("File not found. Please check the path.")
        return
    
    readFile(file_path)
    print(count)
    printfile()


if __name__ == "__main__":
    main()
