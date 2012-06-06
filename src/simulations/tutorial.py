from brian import *

eqs= """
dV/dt = -(V-El)/tau : volt
"""

#parameters
tau = 20 * msecond      # membrane time constant
Vt = -50 * mvolt        # spike threshold
Vr = -60 * mvolt        # reset value
El = -49 * mvolt        # resting potential (same as reset)
N = 40                 # number of neurons to simulate
psp = 0.5* mvolt       # postsynaptic potential size


G = NeuronGroup(N, model=eqs, threshold=Vt, reset=Vr)
G.V = Vr + rand(N) * (Vt - Vr)

C = Connection(G,G, sparseness=0.1, weight=psp)

M = StateMonitor(G,'V',record=1)

run(200 * msecond)

plot(M.times / ms, M[1] / mV)
xlabel('Time (in ms)')
ylabel('Membrane Potential (in mV)')
title('Response for neuron 1')
show()
