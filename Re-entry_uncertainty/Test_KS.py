from scipy import stats

import numpy as np
import matplotlib.pyplot as plt


shape=2;
location=7
scale=1

Nsamples1=200
Nsamples2=200

Nruns=1000
VV=[];
Calpha05=1.358
Calpha01=1.628
nrj05=0
nrj01=0
for i in range(Nruns):
	xs1 = stats.skewnorm.rvs(shape, loc=location, scale=scale, size=Nsamples1)
	xs2 = stats.skewnorm.rvs(2, loc=6, scale=2, size=Nsamples2)
	KsStat,Ks_pvalue=stats.ks_2samp(xs1, xs2)

	DT05=Calpha05*np.sqrt((Nsamples1+Nsamples2)/Nsamples1/Nsamples2)
	if KsStat>DT05:
		rj05=1;
		nrj05=nrj05+1
	else:
		rj05=0;
	DT01=Calpha01*np.sqrt((Nsamples1+Nsamples2)/Nsamples1/Nsamples2)
	if KsStat>DT01:
		rj01=1;
		nrj01=nrj01+1
	else:
		rj01=0;
	VV.append([KsStat,Ks_pvalue, DT05, DT01, rj05, rj01])
    

VV=np.array(VV)
sortedVV = VV[VV[:,1].argsort()]
np.savetxt('VVKS2s.dat', sortedVV, delimiter=' ')
plt.figure()
plt.plot(sortedVV[:,0])
plt.figure()
plt.plot(sortedVV[:,1])
print("The Null Hypothesis (distributions are equal) is rejected ",nrj05," times over ",Nruns," (",nrj05/Nruns*100,"%) with alpha=0.05")
print("The Null Hypothesis (distributions are equal) is rejected ",nrj01," times over ",Nruns," (",nrj01/Nruns*100,"%) with alpha=0.01")
