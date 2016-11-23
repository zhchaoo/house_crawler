#!/usr/bin/python

import sys
import csv
import string

class HouseItem():
    def __init__(self, line):
        self.address = line[1]
        self.size = string.atof(line[2])
        self.data = line[3]
        self.price = string.atof(line[4])
        self.url_token = line[5]
        self.amount = string.atof(line[6])
        self.zone = line[7]


house_list = []
with open('result.csv', 'r') as f:
    reader = csv.reader(f)
    # read csv
    title_flag = True
    for line in reader:
        if title_flag:
            title_flag = False
            continue
    
        house_item = HouseItem(line)
        house_list.append(house_item)

if len(sys.argv) > 2:
    house_filtered_list = [item for item in house_list if item.data[:7] == sys.argv[1] and item.zone == sys.argv[2]]
elif len(sys.argv) > 1:
    house_filtered_list = [item for item in house_list if item.data[:7] == sys.argv[1]]
else:
    house_filtered_list = house_list

count = 0
price = 0
size = 0
amount = 0
for item in house_filtered_list:
    count += 1
    price += item.price
    size += item.size
    amount += item.amount

print "count[%f] avg_price[%f] size[%f] amount[%f]" %(count, amount / size, size, amount)




