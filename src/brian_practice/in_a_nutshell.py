'''
Brian Simulator, in a nutshell -- notes to self

Fundamental Objects:
- NeuronGroup
- Connection
'''

from brian.neurongroup import *
from brian import *

######## NEURON MODEL #########

# start with model parameters -- brian considers units of measurement
tau = 20 * ms      # membrane time constant
Vt = -50 * mV        # spike threshold
Vr = -60 * mV        # reset value
E = -49 * mV       # resting potential

# define neuron dynamics (differential equations)
eqns = 'dV/dt = - (V - E) / tau : volt'


######## NEURON POPULATION ########
G = NeuronGroup(N=40, model=eqns, threshold=Vt, reset=Vr)
G.V = Vr + rand(len(G)) * (Vt - Vr)     # randomly initialize neurons membrane potential

######## CONNECTIONS ########
psp = 0.5 * mvolt       # post-synaptic potential
C = Connection(G,G)
C.connect_random(sparseness=0.1, weight=psp)

######## MONITORING ########
M = SpikeMonitor(G)
Mstate = StateMonitor(G, 'V', record=0)

######## SIMULATION ########
run(200 * msecond)
figure()
raster_plot()
figure()
plot(Mstate.times / ms, Mstate[0] / mV)
show()
print M.nspikes