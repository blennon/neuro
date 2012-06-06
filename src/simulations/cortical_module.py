'''
Created on May 2, 2012

@author: bill
'''
from brian import *

class Layer3(NeuronGroup):
    '''
    Model of layer 3 cortical module
    '''

    def __init__(self, N, t):
        
        eqs = ''' 
        dV/dt=(0.04/ms/mV)*V**2+(5/ms)*V+140*mV/ms-W+I : volt 
        dW/dt=a*(b*V-W) : volt/second 
        I : volt/second'''
        
        Vt,Vr = -30 * mvolt, -65 * mvolt       
        a, b = 0.02/ms, 0.2/ms

        NeuronGroup.__init__(self, N, eqs, threshold=Vt, reset=Vr)
        
        noise_amp = 7
        self.v = -60 + 10*(rand(N)-0.5) # rand init membrane potential
        
if __name__ == "__main__":
    N = 100
    t = 1000
    L3 = Layer3(N,t)
    
    L3.I = TimedArray(noise_amp*rand(t,N)*mV/ms, dt=1*ms)

    M = StateMonitor(L3, 'V', record=0)

    run(t*msecond)

    plot(M.times / ms, M[0] / mV)
    show()