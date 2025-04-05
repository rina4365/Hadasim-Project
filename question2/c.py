import os
import re

date_pattern = r"\b\d{2}/\d{2}/\d{4} \d{2}\b"
number_pattern = r"\b\d{1,6}\.\d{0,3}\b"
my_set = set()
my_list = [[] for _ in range(30)]

def print_average(data_of_day):
    average = 0
    count = 0
    for line in data_of_day:
        split_data = line.split() 
        hour = split_data[1].split(':')[0]
        if hour == '06':
            num = float(split_data[2])
            average += num
            count += 1
    if count != 0:
        print(average/count)


def add_to_list(line):
    #lines = data.splitlines(True)
    #for line in lines:
    day = line[:2]
    if day.isdigit():
        day_num = int(day)
        my_list[day_num-1].append(line)


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
            if check_number(split_data) or date_line_num:
                add_to_list(line)
           

def readFile(file_path):
    file = open(file_path, "r")
    print("read file")
    data = file.read()
    if not data:
        print("empty")
        return
    validate_data(data)
    print_average(my_list[0])



def main():
    file_path = r"C:\Users\User\Desktop\first question\targilB\time_series.txt"
    if os.path.exists(file_path):
        print("File found!")
    else:
        print("File not found. Please check the path.")
        return
    
    readFile(file_path)


if __name__ == "__main__":
    main()

