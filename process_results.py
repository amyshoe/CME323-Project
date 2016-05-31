import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.axes as ax
#import sys

seq_file = "seq_results.npy"
par_file = "par_results.npy"

seq = np.load(seq_file)
par = np.load(par_file)

print "seq\n", seq
print "par\n", par

print seq[0]


n = [20,50]#,100,200]
plt.semilogy(n, seq[0], 'm^-.', n, seq[1], 'r^-.', n, seq[2], 'g^-.')#, n, seq[3], 'c^', n, seq[4], 'c-')
#plt.semilogy(n, par[0], 'mo-', n, par[1], 'ro-', n, par[2], 'go-')#, n, seq[3], 'm^', n, seq[4], 'm-')
plt.axis([10,210,0,750])
#ax.Axes(yscale='log')
plt.ylabel('Time')
plt.xlabel('Number of Vertices')
plt.title('Sequential vs Parallel Blossom Performance')
plt.legend()
plt.show()