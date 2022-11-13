from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np

#0
x0 = [1236, 3966, 479, 964, 2163, 2023, 423, 175,   15, 31]
y0 =  [0.1278, 0.09847403, 0.24790259, 0.13300674, 0.08600513, 0.07065694,0.22535507, 0.36429053,   0.5279988, 0.45549261 ]
#1
x1 = [239, 91, 1279, 2070, 916, 1489,    32]
y1 = [0.3262, 0.44064891, 0.1107, 0.0637, 0.1738, 0.1029,   0.467794558224032]
#2
x2 = [218, 121, 5510, 888, 479,  3310, 505, 332,   23, 15]
y2 = [0.3020065, 0.3895091, 0.0995, 0.1383, 0.2401, 0.07891817, 0.2454,0.2634048,   0.43956875, 0.54482764]

#3 tx
x3 = [1600, 3673,2588, 508, 350, 847]
y3 = [0.07172562, 0.041314, 0.11459873, 0.21928673, 0.27913517, 0.20910224]

y0 = [i/2 for i in y0]
y1 = [i/2 for i in y1]
y2 = [i/2 for i in y2]
y3 = [i/2 for i in y3]

ax = plt.subplot()
plt.scatter(x0,y0,c='g')#0
plt.scatter(x1,y1,c='r')#1
plt.scatter(x2,y2,c='y')#2
plt.scatter(x3,y3,c='b')#3TX
plt.legend(['MA_eversource',"MA_nationalgrid","NY_nationalgrid","TX"])
ax.set_xscale('log')
ax.set_xlabel('N',fontsize=12)
plt.xlim(10,10**4)


def func(x, a, b, c):
    return a * np.exp(-(c * x) ** b)


x = x0 + x1 + x2 + x3
y = y0 + y1 + y2 + y3
popt, pcov = curve_fit(func, x, y, bounds=([0, 0, 0], [1., 1., 1.]))
print(popt[0], popt[1], popt[2])
xdata = np.linspace(-2, 6, 50)
xdata = [10 ** i for i in xdata]
yfit = [func(i, popt[0], popt[1], popt[2]) for i in xdata]
plt.plot(xdata, yfit, 'r--')
ax = plt.subplot()
plt.scatter(x, y)
ax.set_xscale('log')