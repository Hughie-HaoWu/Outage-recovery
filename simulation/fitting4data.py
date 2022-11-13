import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

x = [2,6,10,14,18,22,26,30,34,38]
y1 = [7.85317,7.48972,12.50469,16.04613,18.6301,21.96574,22.82616,24.55972,17.96978,32.2575]
y2 = [6.32004,9.20313,12.56627,13.90096,19.05732,22.10203,25.83609,27.38473,26.53421,29.31769]
y3 = [3.34312,6.29471,10.35562,14.41527,17.3125,22.25835,24.93653,28.03138,30.43965,29.41689]
y4 = [4.40534,7.5526,14.11099,14.75247,17.80914,24.42808,29.46015,31.32976,29.31438,26.74223]
df = pd.DataFrame({'x': x+x+x+x,'y': y1+y2+y3+y4})

x = np.asarray(df[['x']])
y = np.asarray(df[['y']])
reg = LinearRegression().fit(x, y)
print("Equation:  Y = %.5fX + (%.5f)" % (reg.coef_[0][0], reg.intercept_[0]))
print("R square: %s" % reg.score(x, y))

plt.scatter(x, y,  color='black')
plt.plot(x, reg.predict(x), color='red', linewidth=1)
plt.show()