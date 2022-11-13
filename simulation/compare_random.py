import numpy as np
from pandas import Series, DataFrame
import pandas as pd
import random
import time

df = pd.read_csv('D:/Lab/CCNR/DataSource/new_england_outages_to_2020-04-28.csv',usecols=['cust_a','util','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp','county','state'])
# df = pd.read_csv('D:/Lab/CCNR/DataSource/entergy_to_Aug12_2020.csv',usecols=['cust_a','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp'])

df2 = DataFrame(df)

company_list = [['MA','eversource_boston'],['MA','nationalgrid_boston'],['NY','nationalgrid_ny']]
company_index = 0   #----------------could be changed--------------------
state = company_list[company_index][0]
util = company_list[company_index][1]

df2 = df2[df2["state"]== state]#MA,CT,NY
df2 = df2[df2["util"]== util]# nationalgrid_ny,eversource_boston,nationalgrid_boston


# convert str time to timestamp
def str2stamp(str):  # format of str is "2017-09-29 14:33:42"
    time_array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_array)  # - 4*60*60 #4means 4 hours time difference between UTC and Esstern time
    return timestamp


def countNumber(df2, timeNum):
    return (len(df2[(df2.start_timestamp <= timeNum) & (df2.end_timestamp > timeNum)]))

# time_list for company_index=0
time_list = [
    ["2019-12-25 20:00:00", "2019-12-27 00:00:00"], \
    ["2019-02-25 00:00:00", "2019-02-28 00:00:00"], \
    ["2019-10-16 00:00:00", "2019-10-20 00:00:00"], \
    ["2019-10-31 00:00:00", "2019-11-04 00:00:00"], \
    ["2020-02-07 00:00:00", "2020-02-10 00:00:00"], \
    ["2020-04-13 00:00:00", "2020-04-16 00:00:00"], \
    ["2019-07-23 00:00:00", "2019-07-26 00:00:00"], \
    ["2019-01-24 00:00:00", "2019-01-27 00:00:00"], \
    ["2020-03-06 00:00:00", "2020-03-08 00:00:00"], \
    ["2019-11-15 00:00:00", "2019-12-15 00:00:00"] \
    ]

time_index = 1  # ----------------could be changed--------------------
begin_time = time_list[time_index][0]
end_time = time_list[time_index][1]
begin_range_time = str2stamp(begin_time)
end_range_time = str2stamp(end_time)
df3 = df2.drop(df2[(df2.start_timestamp > end_range_time) | (df2.end_timestamp < begin_range_time)].index)
df3.reset_index(drop=True, inplace=True)


# get plot data
start_min = int(begin_range_time)
end_max = int(end_range_time)
step = 15 * 60  # 15minutes
list_num = []
for i in range(start_min, end_max + 1, step):
    temp = countNumber(df3, i)
    list_num.append(temp)

max_slot = [i for i, j in enumerate(list_num) if j == max(list_num)]
max_timestep = (max_slot[0]) * step + start_min
df3 = df3[(df3.start_timestamp < max_timestep) & (df3.end_timestamp > max_timestep)]
df_index = df3.index
df3 = df3.sort_values(by=['start_timestamp', 'end_timestamp'], ascending=True)
df3.reset_index(drop=True, inplace=True)



middle_point_total = []
durationh_interval_total = []

realizations = 10000
for realization in range(realizations):
    print((realization + 1) / realizations * 100, '%')

    clusters = np.arange(len(df3)).tolist()

    ini = [[-1]] * len(df3)
    df_FT = pd.DataFrame(ini, columns=["FinTime"], dtype=np.int)
    clusters_fin = []
    phi = 0.31 * np.exp(-(len(df3) / 496) ** 0.47)

    t = 1
    while len(clusters) > 0:
        clusters_fin = []
        for node in clusters:
            if random.random() < 0.1:  # 满足概率，修复
                df_FT.loc[node, 'FinTime'] = t
                clusters_fin.append(node)
        clusters = list(set(clusters) - set(clusters_fin))
        #     print(len(clusters))
        t += 1
    df_FT["FinTime"] = df_FT["FinTime"] / (max(df_FT['FinTime'])) * 27.031666666666666

    # --------------------------------------------------------------------------------
    nearN = 5
    ave_near_duration = []

    for i in np.arange(len(df3)):
        df4 = df3.loc[:, ['lat', 'lng']]
        df4['durationh'] = df_FT["FinTime"]
        df4['dis'] = (df4['lat'] - df4.loc[i, 'lat']) ** 2 + (df4['lng'] - df4.loc[i, 'lng']) ** 2
        df_nearby = df4.sort_values(by='dis', ascending=True)[1:1 + nearN]
        ave_near_duration.append(sum(df_nearby['durationh']) / len(df_nearby))

    df5 = DataFrame(ave_near_duration, columns=['ave_near_duration'])
    df5['durationh'] = df_FT["FinTime"]

    # --------------------------------------------------------------------------------
    durationh_interval = []
    middle_point = []
    inter_step = 1
    for i in np.arange(0, max(df5['ave_near_duration']), inter_step):
        #         middle_point.append( i + inter_step/2 )
        df_tmp = df5[(df5['ave_near_duration'] >= i) & (df5['ave_near_duration'] < (i + inter_step))]
        if len(df_tmp) == 0:
            durationh_interval.append(0)
        else:
            durationh_interval.append(sum(df_tmp['durationh']) / len(df_tmp))
    durationh_interval_total.append(durationh_interval)


len_durationh_interval = max([len(durationh_interval_total[i]) for i in range(len(durationh_interval_total))])

ave_duration = []
for i in range(len_durationh_interval):
    count = 0
    total = 0
    for k in range(len(durationh_interval_total)):
        if len(durationh_interval_total[k]) > i:
            if durationh_interval_total[k][i] != 0:
                count += 1
                total += durationh_interval_total[k][i]
    if count <= 10:#realizations/10:
        ave_duration.append(-1)
    else:
        ave_duration.append(total/count)

ave_duration_new = [ (ave_duration[i]+ave_duration[i-1])/2 for i in range(1,len(ave_duration[:-1]),2)]
DataFrame(ave_duration_new).to_csv('D:/Desktop/id.csv',index = False)

# from pylab import *
# x = np.arange(len(ave_duration))
# y = ave_duration
# plt.scatter(x,y)