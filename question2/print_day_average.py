import pandas as pd
import os


df_no_duplicates = pd.DataFrame()


def remove_duplicates(data):
    data.drop_duplicates(inplace = True)


def validate_value(data):
    data["value"] = pd.to_numeric(data["value"], errors='coerce')
    data.dropna(subset=["value"], inplace = True)


def validate_date(data):
    data['timestamp'] = pd.to_datetime(data['timestamp'], format='%d/%m/%Y %H:%M', errors='coerce')
    data.dropna(subset=["timestamp"], inplace = True)


def validate_data(data):
    remove_duplicates(data)
    validate_value(data)
    validate_date(data)


def cal_average(data):
    data['timestamp'] = data['timestamp'].dt.strftime('%Y-%m-%d %H')
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    data['timestamp'] = data['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data = data.groupby('timestamp').agg(average = ('value','mean'))
    data['average'] = data['average'].round(1)
    
    data.to_csv('average_day_data.csv',  mode='a', header=False)


def main():

    file_path = r"C:\Users\User\Desktop\Hadasim\question2\time_series.csv.xlsx" 
  
    data = pd.read_csv('time_series.csv', parse_dates=['timestamp'],)
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
  


    data['date'] = data['timestamp'].dt.date
    average_data_file = pd.DataFrame()
    average_data_file.to_csv('average_day_data.csv', mode='w')
    
    for date, group in data.groupby('date'):
        validate_data(group)
        cal_average(group)
        print(f'Day for date {date}: {date.strftime("%A")}') 
            
    
    


if __name__ == "__main__":
    main()