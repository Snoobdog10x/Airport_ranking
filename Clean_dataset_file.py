import os
import csv


def clean_data_csv(filename: str, index: []):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        fname = filename.split('/')[-1].split('.')[0]
        file_path = os.path.join('dataset', fname + '_clean_scr_des.csv')
        with open(file_path, newline='', mode='w') as csv_write_file:
            fieldnames = index
            writer = csv.DictWriter(csv_write_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                row_dicts = {}
                if row['Passengers'] != "0" and row['Origin_airport'] != row["Destination_airport"]:
                    for i in index:
                        row_dicts[i] = row[i]
                    writer.writerow(row_dicts)
                    line_count += 1
            print(f'Processed {line_count} lines.')


def clean_top_5_data_csv(filename: str, index: [], IATAS: {}):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        fname = filename.split('/')[-1].split('.')[0]
        file_path = os.path.join('dataset', fname + '_top5_clean_scr_des.csv')
        with open(file_path, newline='', mode='w') as csv_write_file:
            fieldnames = index
            writer = csv.DictWriter(csv_write_file, fieldnames=fieldnames)
            writer.writeheader()
            for row in csv_reader:
                if line_count == 0:
                    print(f'Column names are {", ".join(row)}')
                    line_count += 1
                row_dicts = {}
                if row['Passengers'] != "0" and row[
                    'Origin_airport'] in IATAS and row['Destination_airport'] in IATAS and row['Origin_airport'] != row[
                    "Destination_airport"]:
                    for i in index:
                        row_dicts[i] = row[i]
                    writer.writerow(row_dicts)
                    line_count += 1
            print(f'Processed {line_count} lines.')


clean_data_csv('./dataset/Airports2.csv',
               ["Origin_airport", "Destination_airport", "Origin_city", "Destination_city", "Passengers"])
# {"ATL","ORD","DFW","LAX","MSP"}
clean_top_5_data_csv('./dataset/Airports2.csv',
                     ["Origin_airport", "Destination_airport", "Origin_city", "Destination_city", "Passengers"],
                     {"LAW", "ELP", "DFW", "LAX", "DTW"})
