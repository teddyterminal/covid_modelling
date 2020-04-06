import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime 
from gf_model import growth_factor

if __name__ == "__main__": 
	states = pd.read_csv("us-states.csv")
	states["date"] = [datetime.datetime.strptime(i, "%Y-%m-%d") for i in states["date"]]

	for state in set(states["state"]): 
	    ss = states[states["state"] == state]
	    if len(ss) >= 4: 
	        growth_factor(ss)
	        plt.plot(ss["date"], ss["gf"])
	        plt.plot(ss["date"], [1] * len(ss["gf"]))
	        print(state)
	        fig = plt.gcf()
	        fig.set_size_inches(20, 15)
	        plt.xticks(rotation = 45)
	        plt.xlim(datetime.date(2020, 3, 1))
	        plt.title("Growth Factor chart for" + state)
	        plt.savefig("state_gfs/" + state + ".jpg", bbox_inches = "tight")
	        plt.clf()