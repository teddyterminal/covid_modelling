import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime 
from scipy.optimize import curve_fit

def sigmoid(x, L ,x0, k):
    y = L / (1 + np.exp(-k*(x-x0)))
    return (y)

def fit(df): 
    p0 = [max(df["cases"]), np.median(df.reset_index().index), 1] # this is an mandatory initial guess

    popt, pcov = curve_fit(sigmoid, df.reset_index().index, df["cases"],p0, method='lm', maxfev=5000)
    return popt, pcov

if __name__ == "__main__":
    states = pd.read_csv("us-states.csv")
    states["date"] = [datetime.datetime.strptime(i, "%Y-%m-%d") for i in states["date"]]

    pc = 0
    cc = 0
    print("SIGMOID MODEL")

    for state in set(states["state"]): 
        ss = states[states["state"] == state]
        print(state)
        print("Current Cases:", list(ss[ss["date"] == "2020-04-04"]["cases"])[0])    
        cc += list(ss[ss["date"] == "2020-04-04"]["cases"])[0]
        try: 
            f = fit(ss)[0]
            if f[0] <= 500000: 
                pc += f[0]
            print(cc, pc)
            print("Projected Cases:", f[0])
            print("Start Date: ", list(ss["date"])[0])
            print("Days to Inflection: ", f[1])
            print("Yeet factor:", f[2], "\n")
        except: 
            print("\n")

    print(cc, pc)

