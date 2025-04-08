import re
import os


errors_list = dict()



def process(line):
    split_line = line.split()  
    if len(split_line) != 5:
        return
    if split_line[4] in errors_list.keys():
        errors_list[split_line[4]] += 1
    else:
        errors_list[split_line[4]] = 1


def readFile(file_path):
    chunk_size = 1024*1024
    file = open(file_path, "r")
    buffer=''

    while True:
        data = file.read(chunk_size)
        if not data:
            break
        buffer += data
        lines = buffer.split('\n')
        for line in lines[:-1]:
            process(line)
        buffer = lines[-1]
    

def main():
    file_path = r"C:\Users\User\Desktop\Hadasim\question1\logste.txt.txt"
    if os.path.exists(file_path):
        print("File found!")
    else:
        print("File not found. Please check the path.")
        return
    
    readFile(file_path)

    n = int(input("Enter a number: "))
    if n > len(errors_list):
        n = len(errors_list)

    sorted_errors_list =dict(sorted(errors_list.items(), key=lambda x: x[1],reverse = True))
    for key in list(sorted_errors_list)[:n]:
        print(key, sorted_errors_list[key])
    

if __name__ == "__main__":
    main()
