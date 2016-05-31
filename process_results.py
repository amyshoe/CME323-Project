import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.axes as ax
#import sys

seq_file = "seq_results.npy"
par_file = "par_results.npy"

seq = np.load(seq_file)
par = np.load(par_file)
seq_sparse = np.load("sparse_seq_results.npy")
par_sparse = np.load("sparse_par_results.npy")

print "seq\n", seq
print "par\n", par


n = [20,50, 100, 150, 200]
plt.semilogy(n, seq_sparse[0], 'm^:', label="Seq, d=0.1")
plt.semilogy(n, seq[0], 'm^-.', label="Seq, d=0.3")
# plt.semilogy(n, seq[1], 'm^--', label="Seq, d=0.5") 
plt.semilogy(n, seq[2], 'm^--', label="Seq, d=0.7")
plt.semilogy(n, seq[3], 'm^-', label="Seq, d=0.9")
plt.semilogy(n, par_sparse[0], 'co:', label="Par, d=0.1")
plt.semilogy(n, par[0], 'co-.', label="Par, d=0.3")
# plt.semilogy(n, par[1], 'co-.', label="Par, d=0.5")
plt.semilogy(n, par[2], 'co--', label="Par, d=0.7")
plt.semilogy(n, par[3], 'co-', label="Par, d=0.9")
plt.axis([10,210,0,750])
plt.ylabel('Time')
plt.xlabel('Number of Vertices')
plt.title('Sequential vs Parallel Blossom Performance')
plt.legend(loc='lower right')
plt.show()