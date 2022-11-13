from pandas import Series, DataFrame
import pandas as pd
import math
from pylab import *
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

df = pd.read_csv('D:/Lab/CCNR/DataSource/new_england_outages_to_2020-04-28.csv',usecols=['cust_a','util','durationh','start_time','start_timestamp', 'lat', 'lng','end_timestamp','county','state'])
df2 = DataFrame(df)

company_list = [['MA','eversource_boston'],['MA','nationalgrid_boston'],['NY','nationalgrid_ny']]
company_index = 0   #----------------could be changed--------------------
state = company_list[company_index][0]
util = company_list[company_index][1]

df2 = df2[df2["state"]== state]#MA,CT,NY
df2 = df2[df2["util"]== util]# nationalgrid_ny,eversource_boston,nationalgrid_boston

#count the number of affected customers at time instant timeNum
def countCustomer(df,timeNum):
    df_satisfy=df[(df.start_timestamp<=timeNum) & (df.end_timestamp>timeNum)]
    customer_num = df_satisfy['cust_a'].sum()
    return customer_num

def get_intensity (begin_range_time,end_range_time,df3):
    start_min = int(begin_range_time)
    end_max = int(end_range_time)
    step = 15*60  #15minutes
    list = []
    for i in range(start_min,end_max+1,step):
        temp = countCustomer(df3,i)
        list.append(temp)
    return round(sum(list)*step/(end_max-start_min))

def get_event_customer(begin_range_time,end_range_time,df):
    df_satisfy=df[(df.start_timestamp<=end_range_time) & (df.start_timestamp>begin_range_time)]
    customer_total = df_satisfy['cust_a'].sum()
    event_total = len(df_satisfy)
    return event_total, customer_total


#convert str time to timestamp
def str2stamp(str): #format of str is "2017-09-29 14:33:42"
    time_array = time.strptime(str, "%Y-%m-%d %H:%M:%S")
    timestamp = time.mktime(time_array)# - 4*60*60 #4means 4 hours time difference between UTC and Esstern time
    return timestamp

def get_function(xcord,ycord):
    (xcord*ycord).mean()
    xcord.mean()* ycord.mean()
    pow(xcord,2).mean()
    pow(xcord.mean(),2)
    m = ((xcord*ycord).mean() - xcord.mean()* ycord.mean())/(pow(xcord,2).mean()-pow(xcord.mean(),2))
    c = ycord.mean() - m*xcord.mean()
    return m[0]#, c[0]   #y=m*x+c

def get_slope(x,y):
    xcord=pd.DataFrame(list(x))  #xcord and ycord must be dataframe
    ycord=pd.DataFrame(pd.DataFrame(log10(y)))
    slope = get_function(xcord,ycord)
    alpha = abs(slope)
    return alpha

# get the data in needed interval
time_list = [["2019-02-25 00:00:00", "2019-02-28 00:00:00"], \
             ["2019-10-16 00:00:00", "2019-10-20 00:00:00"], \
             ["2019-10-31 00:00:00", "2019-11-04 00:00:00"], \
             ["2020-02-07 00:00:00", "2020-02-10 00:00:00"], \
             ["2020-04-13 00:00:00", "2020-04-16 00:00:00"], \
             ["2019-07-23 00:00:00", "2019-07-26 00:00:00"], \
             ["2019-01-24 00:00:00", "2019-01-27 00:00:00"], \
             ["2019-10-30 00:00:00", "2019-11-03 00:00:00"], \
             ["2019-11-15 00:00:00", "2019-12-15 00:00:00"], \
             ["2019-03-20 00:00:00", "2019-07-20 00:00:00"] \
             ]

durationh_x = [[] for _ in range(len(time_list))]
durationh_interval = [[] for _ in range(len(time_list))]
for i in range(len(time_list)):
    begin_time = time_list[i][0]
    end_time = time_list[i][1]
    begin_range_time = str2stamp(begin_time)
    end_range_time = str2stamp(end_time)

    # filter data happend between the given timespan
    df3 = df2.drop(df2[(df2.start_timestamp > end_range_time) | (df2.end_timestamp < begin_range_time)].index)

    step_ccdf = 0.1
    durationh_x_temp = []
    durationh_interval_temp = []
    for j in np.arange(0, math.ceil(max(df3['durationh'])), step_ccdf):
        durationh_x_temp.append(j)
        durationh_interval_temp.append(len(df3[df3['durationh'] >= j]) / len(df3))
    durationh_x[i] = durationh_x_temp
    durationh_interval[i] = durationh_interval_temp


# plot two subfigures
plt.figure(figsize=(10,5))
plt.subplots_adjust(hspace=0.3, wspace=0.15)
ax = plt.subplot()


alpha = [[] for _ in range(len(time_list))]
for i in range(len(time_list)):
    x = durationh_x[i]#duration_interval
    y = durationh_interval[i]
    title_begin_time = time_list[i][0].split(" ")[0]
    title_end_time = time_list[i][1].split(" ")[0]
    label_event = f"{title_begin_time} to {title_end_time}"#", I={intensity[i]}, alpha = {alpha[i]}"
    ax.plot(x,y,label=label_event)

xmajorLocator = MultipleLocator(3) #将x主刻度标签设置为3的倍数
ax.xaxis.set_major_locator(xmajorLocator)
plt.xlim(0,72)

#set title and axis of subfigure 2
ax.set_title('Data from eversource_boston, MA')
ax.set_xlabel('Duration hours x',fontsize=12)
ax.set_ylabel('Unrepaired fraction after x hours',fontsize=12)
yscale('log')

plt.legend()