import numpy as np
from brian import *
from scipy.sparse import coo_matrix

class IzhikevichReset(object):
    '''
    A two-variable reset:
      v<-c
      u<-u+d
    '''
    def __init__(self, c, d):
        self.c = c
        self.d = d

    def __call__(self, P):
        '''
        Clamps membrane potential at reset value.
        '''
        spikes = P.LS.lastspikes()
        if len(spikes) == 0:
            return

        # ugly, but this takes care of multiple ways
        # of instantiating neuron parameters c & d
        try:
            P.v[spikes] = P.c[spikes]
            P.u[spikes] += P.d[spikes]
        except IndexError:
            P.v[spikes] = P.c
            P.u[spikes] += P.d
        except AttributeError:
            try:
                P.v[spikes] = self.c
                P.u[spikes] += self.d
            except IndexError:
                P.v[spikes] = self.c[spikes]
                P.u[spikes] += self.d[spikes]

def random_weights_delays(n,m,p,max_weight,max_delay):
    '''
    return two random sparse matrices where the nonzero
    elements align
    
    n,m - source,target population size
    p - probability of a nonzero connection, i.e. sparsity
    
    these are used in conjunction with DelayConnection
    to create a set of random synaptic weights and delays
    such that each nonzero random weight is paired with a
    nonzero random delay.
    '''
    
    def _sparse_rand(n,m,p):
        '''
        generate a sparse random matrix of size (n,m) with
        sparsity p
        
        scipy.sparse.rand doesn't work well
        '''
        uniq_ind = set()
        # guaranteed exact sparsity value at sake of speed
        while len(uniq_ind) < int(n*m*p):
            i = np.random.randint(n, size=int(n*m*p*1.2))
            j = np.random.randint(m, size=int(n*m*p*1.2))
            uniq_ind = uniq_ind.union(set(zip(i,j)))
        uniq_ind = list(uniq_ind)[0:int(n*m*p)]
        row,col = zip(*uniq_ind)
        data = np.random.rand(int(n*m*p))
        return coo_matrix((data,(row,col)),(n,m))
        
    w = max_weight * _sparse_rand(n,m,p)
    d = w.copy()
    d.data = (max_delay-1.0*ms) * np.ceil(np.random.rand(d.data.shape[0])) + np.ones_like(d.data)*ms
    
    return w,d.tolil()
