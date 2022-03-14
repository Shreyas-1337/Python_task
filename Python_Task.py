#Importing necessary packages
import glob
import pandas as pd
from tkinter import *
from tkinter import filedialog
import locale
from locale import atof

#Creating GUI to enable user to select the folder 
root = Tk()
root.withdraw()
folder_select = filedialog.askdirectory() #stores the path of the selected directory


file_list = glob.glob(folder_select+"/*.csv") #Creates a list of all the .csv files in the given path
csv_dfs = []
files = []
for file in file_list:   #looping through the list of files to read and store them in a data frame
    x=file.split('\\')
    df = pd.read_csv(file) #Read and store the data from the csv file into a data frame
    csv_dfs.append(df) #creating a list of data frames
    files.append(x[-1])    # list of file names 
    
    
#Part 1 of the task 
for i in range(len(files)): 
    df = csv_dfs[i]
    print("\n",files[i])
    print("(Row, Column) = ", df.shape) #prints the number of rows(excluding the head) and columns in the data frame
    df.columns = df.columns.str.lower() #coverting all the columns name to lower case
    if 'country' in df.columns:
        print("Yes, Column named Country is Present in this file")
        if df['value'].dtype != 'float64':
            locale.setlocale(locale.LC_ALL, '')
            df['value'] = df['value'].map(atof)
        df1 = (df.query('year == 2015').groupby('country').agg( {"value":"sum"} )) #query to calculate the sum of values for the countries in the year 2015
        print(df1) #Prints all the distinct countries with the sum of values
        print("Total number of distinct Countries = ",df1.shape[0])
    else:
        print("No, Column named Country is not Present in this file")

        
#Function to calculate the sum of values for a 
def sum_values(df, name):
    print("\nNumber of Rows = ",df.query(f"country == '{name}'").shape[0])
    total_value = df.query(f"country == '{name}'").agg({"value":"sum"})
    print("Total value = ",total_value[0])   


flag = 1
while flag == 1:
    country_entered = input("\nEnter a country name or Quit to exit: ")
    country_entered = country_entered.lower()
    if country_entered  == "quit":
        break
    else:
        for i in range(len(files)):
            df = csv_dfs[i]
            df.columns = df.columns.str.lower()
            print("\n",files[i])
            if ('country' in df.columns):
                df['country'] = df['country'].str.lower()
                sum_values(df,country_entered)
            else:
                print("\nERROR!!!!!!\nCountry doesn't Exixt in this file") 
