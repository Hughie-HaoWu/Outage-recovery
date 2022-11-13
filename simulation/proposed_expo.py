from pandas import Series, DataFrame
import pandas as pd
from pylab import *
import numpy as np
import random
import math

def max_distance_points(x,y):
    dis_max = 0
    point_1 = 0
    point_2 = 0
    for i in range(len(x)):
        for j in range(i+1,len(y)):
            dis_square = (x[i]-x[j])**2+(y[i]-y[j])**2
            if dis_square>dis_max:
                dis_max = dis_square
                point_1 = i
                point_2 = j
    return point_1,point_2


def clustering(x, y ,point_1, point_2):
    if y[point_2]==y[point_1]:
        dis2line = [abs(x[point_1]-x[i]) for i in range(len(x))]
    else:
        k = -(x[point_2]-x[point_1])/(y[point_2]-y[point_1])
        dis2line = [abs((k*x[i]-y[i]+y[point_1]-k*x[point_1])/math.sqrt(k**2+1)) for i in range(len(x))]
    sorted_id = sorted(range(len(dis2line)), key=lambda i: dis2line[i])
    cluster_size = random.choice(np.arange(1,len(x) ))
    cluster_1 = sorted_id[0:cluster_size]
    cluster_2 = sorted_id[cluster_size:]
    return cluster_1, cluster_2


df = pd.read_csv('D:/Lab/CCNR/DataSource/new_england_outages_to_2020-04-28.csv',usecols=['cust_a','util','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp','county','state'])
# df = pd.read_csv('D:/Lab/CCNR/DataSource/entergy_to_Aug12_2020.csv',usecols=['cust_a','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp'])

df2 = DataFrame(df)

company_list = [['MA','eversource_boston'],['MA','nationalgrid_boston'],['NY','nationalgrid_ny']]
company_index = 0  #----------------could be changed--------------------
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
    ["2019-10-25 00:00:00", "2019-10-31 00:00:00"], \
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
list = []
for i in range(start_min, end_max + 1, step):
    temp = countNumber(df3, i)
    list.append(temp)

max_slot = [i for i, j in enumerate(list) if j == max(list)]
max_timestep = (max_slot[0]) * step + start_min
df3 = df3[(df3.start_timestamp < max_timestep) & (df3.end_timestamp > max_timestep)]
df_index = df3.index
df3 = df3.sort_values(by=['start_timestamp', 'end_timestamp'], ascending=True)
df3.reset_index(drop=True, inplace=True)



ini = [[0]] * len(df3)
df_FT_total = pd.DataFrame(ini, columns=["FinTime"], dtype=np.int)
unrepaired_frac_total = []

realizations = 10000
for realization in range(realizations):
    print((realization + 1) / realizations * 100, '%')

    clusters = [np.arange(len(df3)).tolist()]
    unrepaired_num = len(df3)

    ini = [[-1]] * len(df3)
    df_FT = pd.DataFrame(ini, columns=["FinTime"], dtype=np.int)

    t = 0
    while unrepaired_num > 0:
        clusters_tmp = []
        for cluster in clusters:
            if len(cluster) == 1:
                df_FT.loc[cluster[0], 'FinTime'] = t - 1
            elif random.random() > (1 - len(cluster) / len(df3)):
                x = df3.loc[cluster, 'lng'].tolist()
                y = df3.loc[cluster, 'lat'].tolist()
                point_1, point_2 = max_distance_points(x, y)
                id_1, id_2 = clustering(x, y, point_1, point_2)
                #                 id_1, id_2 = clustering_2(x, y )
                cluster_1 = [cluster[i] for i in id_1]
                cluster_2 = [cluster[i] for i in id_2]
                clusters_tmp.append(cluster_1)
                clusters_tmp.append(cluster_2)
            else:
                clusters_tmp.append(cluster)
        clusters = clusters_tmp
        unrepaired_num = sum([len(i) for i in clusters])
        t += 1

    df_FT_total = df_FT_total.append(df_FT)
df_FT_total = df_FT_total[df_FT_total['FinTime'] != 0]

#----------------------------------------------------------------------------
durationh_interval = []
inter_step = 5
for i in np.arange( 0, math.ceil(max(df_FT_total['FinTime'])),inter_step):
        durationh_interval.append( len(df_FT_total[df_FT_total['FinTime']>=i]) - len(df_FT_total[df_FT_total['FinTime']>=(i+inter_step)]) )
percent = [i/sum(durationh_interval) for i in durationh_interval]
unrepaired_frac = [1-sum(percent[0:i]) for i in range(len(durationh_interval))]
unrepaired_frac = [ i for i in unrepaired_frac if i>=0.00099]

phi = 0.06875393612058874
x = np.arange(len(unrepaired_frac)) / (phi*len(df3)) * inter_step
y = unrepaired_frac
ax = plt.subplot()
ax.plot(x,y)
ax.set_xlabel('Time step x',fontsize=12)
ax.set_ylabel('Unrepaired fraction after x steps',fontsize=12)
yscale('log')
