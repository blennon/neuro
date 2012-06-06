from brian import *

class Nucleus(object):
    def __init__(self):
        pass
    
    def receive(self, src_nuc, conn_type):
        pass
    
    def get_neurons(self):
        return self.neurons

class AbducensNucleus(Nucleus):
    
    def __init__(self, N, T):
        eqs = ''' 
        dV/dt=(0.04/ms/mV)*V**2+(5/ms)*V+140*mV/ms-W+I : volt 
        dW/dt=a*(b*V-W) : volt/second 
        I : volt/second'''
        
        Vt,Vr = -30 * mvolt, -65 * mvolt       
        a, b = 0.02/ms, 0.2/ms

        noise_amp = 7
              
        self.neurons = NeuronGroup(N, eqs, threshold=Vt, reset=Vr)
        self.neurons.v = -60 + 10*(rand(N)-0.5)
        self.neurons.I = TimedArray(noise_amp*rand(T,N)*mV/ms, dt=1*ms)

class VestibularNucleus(Nucleus):
    pass

class OculomotorNucleus(Nucleus):
    pass

if __name__ == "__main__":
    r_ABD = AbducensNucleus(100,1000)
    l_ABD = AbducensNucleus(100,1000)
