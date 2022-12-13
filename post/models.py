import csv

with open("test.csv", 'r') as f:
        reader = csv.reader(f)
        print(reader)
