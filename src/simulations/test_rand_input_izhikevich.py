from brian import *
import numpy as np

tau = 20 * msecond        # membrane time constant
Vt = -30 * mvolt          # spike threshold
psp = 0.5 * mvolt         # postsynaptic potential size
a = 0.02/ms
b = 0.2/ms
c = -55 * mvolt          # reset value
# d = ?
tlen = 1000


eqs = ''' 
dV/dt=(0.04/ms/mV)*V**2+(5/ms)*V+140*mV/ms-W+I : volt 
dW/dt=a*(b*V-W) : volt/second 
I : volt/second''' 

group = NeuronGroup(N=1, model=eqs, threshold=Vt, reset=c)

group.I = TimedArray(6*rand(tlen)*mV/ms, dt=1*ms)

M = StateMonitor(group, 'V', record=0)

run(tlen*msecond)

plot(M.times / ms, M[0] / mV)
show()
