import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime 
from gf_model import growth_factor
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

if __name__ == "__main__": 
	counties = pd.read_csv("us-counties.csv")
	counties["date"] = [datetime.datetime.strptime(i, "%Y-%m-%d") for i in counties["date"]]


	vv = {}
	debut = {}

	for county in set(counties["fips"].dropna()): 
	    ct = counties[counties["fips"] == county]
	    
	    dates = list(ct["date"])
	    cts = list(ct["county"])
	    sts = list(ct["state"])
	    cases = list(ct["cases"])
	    fips = list(ct["fips"])
	    
	    debut[fips[0]] = dates[0]
	    
	    if len(ct) >= 4: 
	        growth_factor(ct)
	        gfs = list(ct["gf"])

	        for i in range(len(dates)): 
	            if dates[i] not in v: 
	                vv[dates[i]] = []
	            
	            if gfs[i] > 2.5: 
	                vv[dates[i]].append(fips[i])
	                
	            if gfs[i] > 2.5 and dates[i] == datetime.date(2020, 4, 4): 
	                print(dates[i], cts[i], sts[i], cases[i], gfs[i])

	debutd = {}
	for k in debut: 
	    if debut[k] not in debutd: 
	        debutd[debut[k]] = []
	    
	    debutd[debut[k]].append(k)

	des = sorted(debutd.items())
	vvs = sorted(vv.items())

	KM = 1000.
	clat = 39.3
	clon = -94.7333
	wid = 5500 * KM
	hgt = 3500 * KM
	m = Basemap(width=wid, height=hgt, rsphere=(6378137.00,6356752.3142),
	        resolution='i', area_thresh=2500., projection='lcc',
	        lat_1=38.5, lat_2=38.5, lat_0=clat, lon_0=clon)
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.set_facecolor('#729FCF')
	m.fillcontinents(color='#FAFAFA', ax=ax, zorder=0)
	m.readshapefile('cshp/tl_2019_us_county','counties',drawbounds=True)
	m.drawstates(ax=ax)
	m.drawcountries(ax=ax)
	m.drawcoastlines(ax=ax)

	visited = set()

	for ddd in des: 
	    for i, county in enumerate(m.counties_info): 
	        if county["GEOID"] not in visited: 
	            for idx in ddd[1]: 
	                if int(idx) == int(county["GEOID"]): 
	                    poly = Polygon(m.counties[i], facecolor="red")  # edgecolor="white"
	                    ax.add_patch(poly)
	                    visited.add(county["GEOID"])
	        else: 
	            poly = Polygon(m.counties[i], facecolor="gray")  # edgecolor="white"
	            ax.add_patch(poly)

	    plt.title("Counties with Cases, " + str(ddd[0]))
	    fig = plt.gcf()
	    fig.set_size_inches(15, 10)
	    plt.savefig("cases/" + str(ddd[0]) + ".jpg", bbox_inches = "tight")

	for ddd in vvs: 
	    for i, county in enumerate(m.counties_info): 
	        if county["GEOID"] not in visited: 
	            for idx in ddd[1]: 
	                if int(idx) == int(county["GEOID"]): 
	                    poly = Polygon(m.counties[i], facecolor="red")  # edgecolor="white"
	                    ax.add_patch(poly)
	                    visited.add(county["GEOID"])
	        else: 
	            poly = Polygon(m.counties[i], facecolor="gray")  # edgecolor="white"
	            ax.add_patch(poly)

	    plt.title("Counties with Cases, " + str(ddd[0]))
	    fig = plt.gcf()
	    fig.set_size_inches(15, 10)
	    plt.savefig("gf/" + str(ddd[0]) + ".jpg", bbox_inches = "tight")




