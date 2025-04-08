import pandas as pd

data = pd.DataFrame()


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
    average_data = data.groupby('timestamp').agg(average = ('value','mean'))
    average_data['average'] = average_data['average'].round(1)
    average_data.to_csv('average_parquet.csv', header=True)


def main():

    file_path = r"C:\Users\User\Desktop\Hadasim\question2\time_series.parquet" 
   
    data = pd.read_parquet(file_path)
 
    data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
    validate_data(data)
    cal_average(data)

if __name__ == "__main__":
    main()