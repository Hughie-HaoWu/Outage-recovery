import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit

df = pd.read_csv('D:/Lab/CCNR/DataSource/new_england_outages_to_2020-04-28.csv',usecols=['cust_a','util','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp','county','state'])
# df = pd.read_csv('D:/Lab/CCNR/DataSource/entergy_to_Aug12_2020.csv',usecols=['cust_a','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp'])
df2 = DataFrame(df)

company_list = [['MA','eversource_boston'],['MA','nationalgrid_boston'],['NY','nationalgrid_ny']]
company_index = 0   #----------------could be changed--------------------
state = company_list[company_index][0]
util = company_list[company_index][1]

df2 = df2[df2["state"]== state]#MA,CT,NY
df2 = df2[df2["util"]== util]# nationalgrid_ny,eversource_boston,nationalgrid_boston

#convert str time to timestamp
def str2stamp(str): #format of str is "2017-09-29 14:33:42"
    time_array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_array)# - 4*60*60 #4means 4 hours time difference between UTC and Esstern time
    return timestamp

def countNumber(df2,timeNum):
    return(len(df2[(df2.start_timestamp<=timeNum) & (df2.end_timestamp>timeNum)]))

def func(x, b):
    return max(y) * np.exp(-b * x)

# time_list for company_index=0
time_list = [["2019-02-25 00:00:00","2019-02-28 00:00:00"],\
             ["2019-10-16 00:00:00","2019-10-20 00:00:00"],\
             ["2019-10-31 00:00:00","2019-11-04 00:00:00"],\
             ["2020-02-07 00:00:00","2020-02-10 00:00:00"],\
             ["2020-04-13 00:00:00","2020-04-16 00:00:00"],\
             ["2019-07-23 00:00:00","2019-07-26 00:00:00"],\
             ["2019-01-24 00:00:00","2019-01-27 00:00:00"],\
             ["2020-03-06 00:00:00","2020-03-08 00:00:00"],\
            ]


time_index = 0   #----------------could be changed--------------------
begin_time = time_list[time_index][0]
end_time = time_list[time_index][1]
begin_range_time = str2stamp(begin_time)
end_range_time = str2stamp(end_time)
df3 = df2.drop(df2[(df2.start_timestamp>end_range_time) | (df2.end_timestamp<begin_range_time)].index)
df3.reset_index(drop=True, inplace=True)

# get plot data
start_min = int(begin_range_time)
end_max = int(end_range_time)
step = 15*60  #15minutes
list_num = []
for i in range(start_min,end_max+1,step):
    temp = countNumber(df3,i)
    list_num.append(temp)

max_slot = [i for i, j in enumerate(list_num) if j == max(list_num)]
max_timestep = (max_slot[0])*step + start_min
df3 = df3[(df3.start_timestamp<max_timestep) & (df3.end_timestamp>max_timestep)]
df3 = df3.sort_values(by=['start_timestamp','end_timestamp'],ascending = True)
df3.reset_index(drop=True, inplace=True)


# plot the data
x = np.arange(start_min,end_max+1,step)
y = list_num

# trick to get the axes
fig,ax = plt.subplots(figsize = (20,4.8))
plt.figure(2,figsize=(20,4.8))
plt.subplots_adjust(hspace=1, wspace=0.1)

# make ticks and tick labels
interval = 60*60*8
xticks =range(min(x),max(x)+1,interval)
xticklabels = [time.strftime("%Y-%m-%d %H",time.localtime(i)) for i in xticks]

# plot data
ax.plot(x,y)

# set ticks and tick labels
ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels,rotation=15)
ax.set_xlabel('Times',fontsize=12)
ax.set_ylabel('Number of outages',fontsize=12)
ax.set_title(f'{begin_time} to {end_time}, {util}, {state}')

# show the figure, figure varies when laptop time zone changes due to str2stamp
plt.show()

#get expo
index_y_max = y.index(max(y))
ydata = y[index_y_max:-1]
xdata = (x[index_y_max:-1] - x[index_y_max]) / (60 * 60)
popt, pcov = curve_fit(func, xdata, ydata, maxfev=2000)
print(popt, pcov)