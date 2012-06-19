'''
This module contains convenience classes for instantiating
frequently used neuron groups
'''

from brian.library.IF import *
from brian.neurongroup import *
from brian import *
from utils import IzhikevichReset


class IzhikevichGroup(NeuronGroup):
    '''
    Group of Izhikevich spiking neurons
    '''
    
    def __init__(self, N, a, b, c, d, taue, taui, Vt=30*mV, rand_init=True):
        '''
        Initializes a group of Izhikevich spiking neurons with the
        following parameters:
        - a,b,c,d (Izhikevich neuron model parameters)
        - taue, taui -- exc/inh synaptic conductance parameters
        - Vt - threshold value
        
        These values can be floats or numpy arrays.
        
        Appropriate units from brian must be expressed in these
        parameters, 
        e.g. a/ms, b/ms, c*mV, d*mV/ms, taue*ms, taui*ms, Vt*mV
        
        This neuron group has three input channels:
        1.) 'I' current input (nA)
        2.) 'ge' excitatory synaptic input with conductance 'taue'
        3.) 'gi' inhibitory synaptic input with conductance 'taui'
        '''
        
        self.eqs = Equations('''
                    dv/dt = (0.04/ms/mV)*v**2+(5/ms)*v+140*mV/ms-u+I/nF+(ge-gi)/ms : volt
                    du/dt = a*(b*v-u) : volt/second
                    dge/dt = -ge/taue    : volt
                    dgi/dt = -gi/taui    : volt
                    I : amp
                    ''')
        
        NeuronGroup.__init__(self, N, self.eqs, threshold=Vt, reset=IzhikevichReset(c,d))
        
        if rand_init:
            self.rand_init()
        
    def rand_init(self):
        '''randomly initialize the values of v,u'''
        self.v = (-80 + randn(len(self)))* mV
        self.u = randn(len(self)) * mV/ms
        
if __name__ == "__main__":
    G=IzhikevichGroup(100, 0.02/ms, 0.2/ms, -65*mV, 8*mV/ms, 1*ms, 1*ms)
