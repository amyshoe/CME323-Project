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

n = [20,50, 100, 150, 200]
plt.semilogy(n, seq[0], 'm^:', n, seq[1], 'm^-.', n, seq[2], 'm^--', n, seq[3], 'm^-')
plt.semilogy(n, par[0], 'co:', n, par[1], 'co-.', n, par[2], 'co--', n, seq[3], 'm^-')
plt.axis([10,210,0,750])
plt.ylabel('Time')
plt.xlabel('Number of Vertices')
plt.title('Sequential vs Parallel Blossom Performance')
plt.legend()
plt.show()