import numpy as np

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
        if spikes == []:
            return
        try:
            # for the case that c,d are numpy arrays
            P.v[spikes] = self.c[spikes]
            P.u[spikes] += self.d[spikes]
        except IndexError:
            P.v[spikes] = self.c
            P.u[spikes] += self.d
