/********************************************************
 * Condution-Radiation Coupling  March-2023
 * Authors: David Becerril Rodriguez 
 * Affilitation: CNR-ISM
 *
 * Runs Statistical analysis on AFM data of SAOS-Cells 
 *************************************************************/
 
import os
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import numpy as np
from PIL import Image
import io

filename  = "filename.csv"
DataPath  =  os.getcwd() + filename
df0       = pd.read_csv(DataPath)

df0.Sample = df0.Sample.apply(lambda x: "ctrl" if x == "statica" else "1 Hz")
df0["Eccentricity"] = df0["NucleusMinAxis"]/df0["NucleusMajAxis"]
df0["AreaCalc"] = (np.pi/4)*df0["NucleusMinAxis"]*df0["NucleusMajAxis"]

#fig, ax = plt.subplots(1,2,figsize = (9,3.5))

sns.set(font_scale = 2.0)

#ax[0].set_xlim(0,0.2)
#sns.boxplot(data = df0[df0.CellPart == cpart], x=vary_over , y= cvariable,ax = ax[1]).set(title = ptitle)
#sns.swarmplot(x=vary_over, y=cvariable,ax=ax[1], data=df0[df0.CellPart == cpart], color=".25")
#ax[1].set_ylim(0,0.25)
sns.histplot(df0,x = "PerimeterRms" , hue = "Sample" , 
             common_norm = False,kde = True,label = "Static")
             
             

samplei = list( df0.Sample.unique() )
mat1 = np.zeros((len(samplei)) )
mat2 = np.zeros((len(samplei)) )
###########################
#### Make Histograms
#########################
cpart  = "Nucleus"
cvariable = "RMS"

for i in np.arange(len(samplei)):
        dfi = df0[(df0.Sample == samplei[i] ) & (df0.CellPart == cpart)]
        dfv = df0[(df0.Sample == samplei[i] ) & (df0.CellPart == cpart)]

        mat1[i] = dfi[cvariable].mean()
        mat2[i] = dfi[cvariable].std()

print(samplei,mat1,mat2)
###########################
#### Axis Histograms
#########################

df1 = df0.dropna()
df1 = df1.drop(df1[ df1.MinorAxis > 50].index )
cpart  = "OffNucleus"
cvariable = "MajorAxis"df0.Eccentricity[df0.Sample == "1hz"]

fig, ax = plt.subplots(1,2,figsize = (9,3.5))

sns.histplot(df1[df1.CellPart == cpart ],x = cvariable , hue = vary_over , 
             common_norm = False,stat = "density",kde = True,label = "Static",ax= ax[0]).set( title = ptitle)
#ax[0].set_xlim(0,0.2)
cvariable = "MinorAxis"
vary_over = "Sample"
ptitle = cpart + cvariable
sns.histplot(df1[df1.CellPart == cpart ],x = cvariable , hue = vary_over , 
             common_norm = False,stat = "density",kde = True,label = "Static",ax= ax[1]).set( title = ptitle)#sns.swarmplot(x=vary_over, y=cvariable,ax=ax[1], data=df0[df0.CellPart == cpart], color=".25")
#ax[1].set_ylim(0,0.25)


samplei = list( df1.Sample.unique() )
mat1 = np.zeros((len(samplei)) )
mat2 = np.zeros((len(samplei)) )

cpart  = "OffNucleus"
cvariable = "MajorAxis"

for i in np.arange(len(samplei)):
        dfi = df1[(df1.Sample == samplei[i] ) & (df1.CellPart == cpart)]
        dfv = df1[(df1.Sample == samplei[i] ) & (df1.CellPart == cpart)]

        mat1[i] = dfi[cvariable].mean()
        mat2[i] = dfi[cvariable].std()

print(samplei,mat1,mat2)


###########################
#### Bar Plots
#########################
fig = plt.figure( dpi=300)
plt.tight_layout()

sns.set(font_scale = 2.3)
sns.set_style(style='white')  
 
#ax = sns.barplot(x="Sample", y="AreaCalc", data=df0,capsize =0.2)
#ax.set_ylabel(r"$(\mu m)^2$ ")
#ax.set_xlabel("")
#ax.set_title("Nucleus Area")

ax = sns.barplot(x="Sample", y="Eccentricity", data=df0,capsize =0.2)
ax.set_ylabel(r"$(\mu m)$")
ax.set_xlabel("")
ax.set_title("Eccentricity")

fig.savefig(os.getcwd()+ "/Eccentricity.tiff",dpi=300,bbox_inches='tight')


###########################
#### Make profiel Graph
#########################
#filename = "profile_ctrl_data"
#filename = "profile_ctrl_data_cut.txt"
filename = "figure3A_profile.txt"
#filename = "profile_c1hz_data"
#filename = "Peri_exmample.txt"
#filename = "profile2d_smoothed.txt"
DataPath  =  os.getcwd() + '/images/draft1/' + filename


profile = pd.read_csv(DataPath,header=None, delimiter=r"\s+") / 1E-6
profile.rename(columns = {0:"x",1:"Topography"}, inplace = True)
profile["x"] = profile["x"] - profile["x"][0]
#profile["Topography"] = profile["Topography"] - profile["Topography"].min()

fig = plt.figure(figsize=(6,4), dpi=300)

sns.set(font_scale = 2)
sns.set_style('whitegrid',{'axes.linewidth': 0.5})  
ax = sns.lineplot(data = profile, x = "x", y  = "Topography", linewidth = 3 )
ax.set_ylabel(r"Height $(\mu m)$")
ax.set_xlabel(r"x $(\mu m)$")
plt.ylim(profile["Topography"].min()-0.05, profile["Topography"].max()+0.3)
ax.tick_params(bottom=True, left=True)
plt.tight_layout()
fig.savefig(filename + ".tiff")


#### Run T-test
d1 = df0["PerimeterRms"][df0.Sample == "1 Hz"].mean()/df0["PerimeterRms"][df0.Sample == "ctrl"].mean()
d2 = df0["AreaCalc"][df0.Sample == "1 Hz"].mean()/df0["AreaCalc"][df0.Sample == "ctrl"].mean()
print(d1,d2)


