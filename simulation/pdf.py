import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from datetime import datetime
import time

def countNum(df3,duration_temp,count_step):
    return(len(df3[(df3.duration<(duration_temp+count_step)) & (df3.duration>=duration_temp)]))

df = pd.read_csv('D:/Lab/CCNR/DataSource/new_england_outages_to_2020-04-28.csv',usecols=['cust_a','util','duration','start_time','start_timestamp', 'lat', 'lng','end_timestamp','county','state'])
# df = pd.read_csv('D:/Lab/CCNR/DataSource/entergy_to_Aug12_2020.csv',usecols=['cust_a','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp'])
df2 = DataFrame(df)
df3 = df2[( df2['cust_a']<=10) ]
df3 = df3[df3.duration<100000]
count_step = 1000
list = []
i = 0
while i <= max(df3['duration']):
    temp = countNum(df3,i,count_step)
    list.append(temp/len(df3))
    i += count_step

