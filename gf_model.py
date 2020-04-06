import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime 


def growth_factor(df): 
    new = [0]
    for i in range(1, len(df)): 
        new.append(list(df["cases"])[i] - list(df["cases"])[i-1])
        
    gf = [0, 0, 0]
    for i in range(3, len(new)): 
        if new[i-1] + new[i-2] + new[i-3] == 0: 
            gf.append(0)
        else: 
            gf.append((new[i] + new[i-1] + new[i-2])/(new[i-1] + new[i-2] + new[i-3]))
            
    df["new"] = new.copy()
    df["gf"] = gf.copy()

def slv(y, new, factor_start = 1.05, iterations = 30, dropoff = 0.01, ns = 0.05): 
    yy = y.copy()
    nn = new.copy()
    fs = factor_start
    
    for i in range(iterations): 
        last_3 = nn[-1] + nn[-2] + nn[-3]
        last_2 = nn[-1] + nn[-2]
        
        fs -= dropoff*(fs**3)
        noise = (np.random.random()-0.5)*ns
        
        fss = fs + noise
        
        n0 = fss*last_3 - last_2
        
        if n0 < 0: 
            n0 = 0
        
        y0 = yy[-1] + n0

        nn.append(n0)
        yy.append(y0)
        
    
    return yy, nn

def wa(x): 
    s = 0
    for i in range(len(x)): 
        s += i*x[i]
    return s/sum(x)
    
if __name__ == "__main__": 
    states = pd.read_csv("us-states.csv")
    states["date"] = [datetime.datetime.strptime(i, "%Y-%m-%d") for i in states["date"]]

    print("GROWTH MODEL")

    pc = 0
    cc = 0
    proj = {}

    for state in set(states["state"]): 
        ss = states[states["state"] == state]
        print(state)
        proj[state] = {}
        print("Current Cases:", list(ss[ss["date"] == "2020-04-04"]["cases"])[0])
        proj[state]["current"] = list(ss[ss["date"] == "2020-04-04"]["cases"])[0]
        cc += list(ss[ss["date"] == "2020-04-04"]["cases"])[0]

        growth_factor(ss)
        
        dist = []
        
        ss["gf"][-5:]
        
        start = min(np.average(ss["gf"][-5:]), 1.2)
        if list(ss["cases"])[-1] < 700: 
            start = 1.2
        
        peaks = 0
        hpeaks = 0
        hidx = 0
        for i in range(1000): 
            yy, nn = slv(list(ss["cases"]), list(ss["new"]), factor_start = start, iterations = 100, dropoff = 0.005, ns = 0.25)
            dist.append(yy[-1])
            
            nnpeak = []
            for i in range(len(nn)): 
                if i < 14: 
                    nnpeak.append(np.sum(nn[:i+1]))
                else: 
                    nnpeak.append(np.sum(nn[i-14:i+1]))
            
            peaks += wa(nn)
            hidx += np.argmax(nnpeak)
            hpeaks += np.max(nnpeak)
       
        peaks /= 1000
        hpeaks /= 5000
        hidx /= 1000

        pc += np.median(dist)
        print(cc, pc)
        print("Projected Cases:", np.median(dist))
        proj[state]["proj"] = np.median(dist)
        print("Start Date: ", list(ss["date"])[0])
        proj[state]["start"] = list(ss["date"])[0]
        print("Starting GF: ", start)
        proj[state]["sgf"] = start
        print("Date of Inflection: ", list(ss["date"])[0] + datetime.timedelta(peaks))
        print("Peak Hospital: ", list(ss["date"])[0] + datetime.timedelta(hidx), hpeaks, "\n")

        proj[state]["inf"] = list(ss["date"])[0] + datetime.timedelta(peaks)
        proj[state]["hidx"] = list(ss["date"])[0] + datetime.timedelta(hidx)
        proj[state]["hpeaks"] = hpeaks

    print(cc, pc)
    proj = pd.DataFrame.from_dict(proj).T
    proj.to_csv("projections.csv")

