'''
Created on Oct 25, 2010

@author: joel
'''
import pypyr.extra.poisson as pep
import pypyr.utils as pu
import pypyr.mesh as pm
import pypyr.physics.stokes as pps
import numpy as np
import math

def convergence():
    f = open("sc.dat", "w")
    f.write("k,N,e,dofs\n")
    points, weights = pu.cubequadrature(12)
    up, ddup = pep.poisson(60, points[:,np.array([1,2])])
    l2 = lambda f: math.sqrt(np.sum(f.flatten() **2 * weights.flatten()))
    l2up = l2(up)
    for N in range(2,15):
        for k in range(1,10):
            meshevents = lambda m: pps.stokescubemesh(N, m)
        
            u, dofs = pps.stokespressure(k,meshevents,{pps.inputbdytag:pps.pfn(-0.5), pps.outputbdytag:pps.pfn(0.5)}, points, True,N==1)
            pt = points.transpose()
            ut = u.transpose()
            
            
            e = [l2(ut[0] - up)/l2up, l2(ut[1])/l2up, l2(ut[2])/l2up]
            print k, N, e, dofs
            f.write("%s, %s, %s, %s\n"%(k,N,e,dofs))
            f.flush()
            if dofs > 30000: break
    f.close()
  

if __name__ == '__main__':
    convergence()
