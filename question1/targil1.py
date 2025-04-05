import re
import os


errors_list = dict()
err_pattern = re.compile(r'\bERR_\w+\b')



def process(chunk):
    lines = chunk.splitlines(True)
    for line in lines:
        err_type_line = re.search(err_pattern,line)
        if err_type_line:
            if err_type_line.group(0) in errors_list.keys():
                errors_list[err_type_line.group(0)] += 1
            else:
                errors_list[err_type_line.group(0)] = 1



def readFile(file_path):
    chunk_size = 1024
    file = open(file_path, "r")
    while True:
        data = file.read(1024*1024)
        if not data:
            break
        process(data) 
    


def main():
    file_path = r"C:\Users\User\Desktop\first question\logste.txt.txt"
    if os.path.exists(file_path):
        print("File found!")
    else:
        print("File not found. Please check the path.")
        return
    
    readFile(file_path)

    x = int(input("Enter a number: "))
    if x > len(errors_list):
        x = len(errors_list)

    sorted_errors_list =dict(sorted(errors_list.items(), key=lambda x: x[1],reverse = True))
    for key in list(sorted_errors_list)[:x]:
        print(key, sorted_errors_list[key])
    

if __name__ == "__main__":
    main()
