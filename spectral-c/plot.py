import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np 

df = pd.read_csv('cmake-build-debug/logs.csv', sep=", ") 
df.plot(y="in")
df.plot(y="mag")
plt.show()
