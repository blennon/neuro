from brian import *
eqs = '''
dv/dt = (ge+gi-(v+49*mV))/(20*ms) : volt
dge/dt = -ge/(5*ms) : volt
dgi/dt = -gi/(10*ms) : volt
'''
P = NeuronGroup(400, eqs, threshold=-50*mV, reset=-60*mV)
P.v = -60 + 100*rand(4000)
Pe = P.subgroup(320)
Pi = P.subgroup(80)
Ce = Connection(Pe, P, 'ge', weight=1.62*mV, sparseness=0.01)
Ci = Connection(Pi, P, 'gi', weight=-9*mV, sparseness=0.04)
M = SpikeMonitor(P)
run(1*second)
raster_plot(M)
show()
