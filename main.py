'''
Title: Project task
Date: 23.5.2021
Made by: Aditya Mangal

'''


from os import write
from bs4 import BeautifulSoup
import requests
import pandas as pd
from termcolor import cprint
from time import sleep

with open("data.txt", 'rt') as file:
    title_list = []
    availability_list = []
    url_list = []
    try:
        cprint('Fetching the URL from file...', 'yellow')
        sleep(2)
        cprint('Fetching the Products data and availability...', 'yellow')
        sleep(2)
        cprint('Wait for processing...', 'yellow')
        a = file.readlines()
        for i in range(len(a)):
            url = a[i]
            if "\n" in url:
                url = a[i][:-1]
            else:
                url = a[i]
            url_list.append(url)
            data = requests.get(url).text
            html = BeautifulSoup(data, "html.parser")
            title = html.find('title')
            title = str(title)[7:-8]
            title_list.append(title)
            availability = html.find(
                class_="link-button text-bold product-block-status-availability")
            availability = str(availability)
            if "Available" in availability:
                current_av = 'In Stock'
                availability_list.append(current_av)
            elif "Out of Stock" and 'Temporarily unavailable' in availability:
                current_av = 'Out of Stock'
                availability_list.append(current_av)
            elif "Mixed Availability" in availability:
                current_av = 'Variant'
                availability_list.append(current_av)
            elif "Discontinued" in availability:
                current_av = 'Discontinued'
                availability_list.append(current_av)
    except:
        cprint('Somthing Wrong! Check your URL data txt.', 'yellow')

cprint('Fetching and writing the saving the data...', 'yellow')
sleep(2)
with open('output.txt', 'a') as file:
    try:
        for i in range(len(availability_list)):
            file.writelines(str(i+1))
            file.writelines(' ,')
            file.writelines(title_list[i])
            file.writelines(' ,')
            file.writelines(availability_list[i])
            file.writelines(' ,')
            file.writelines(url_list[i])
            file.write('\n')
    except:
        cprint("Some error occured.", 'yellow')
cprint("Saving Data to output.csv.", 'yellow')
sleep(2)
dataframe1 = pd.read_csv("output.txt", header=None)
dataframe1.columns = ['S.No', 'Products from given URL', 'Stock Status','Hyperlink']
dataframe1.to_csv('output.csv', index=None)
cprint("Saved Succesfully.", 'yellow')
