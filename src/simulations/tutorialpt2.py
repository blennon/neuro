from brian import *

#Neuron parameters
tau_a = 1 * ms        # neuron state a time constant
tau_b = 10 * ms       # neuron state b time constant
Vt = 10 * mV
Vr = 0 * mV

eqs = Equations('''
dVa/dt = -Va/tau_a : volt
dVb/dt = -Vb/tau_b : volt
''')

spiketimes = [(0, 1 * ms), (0, 4 * ms), (1, 2 * ms), (1, 3 * ms)]   # (i,t): neuron i spikes at time t

G1 = SpikeGeneratorGroup(2,spiketimes)

G2 = NeuronGroup(N=1, model=eqs, threshold=Vt, reset=Vr)

C1 = Connection(G1,G2, 'Va')
C2 = Connection(G1,G2, 'Vb')

C1[0,0] = 6 * mV
C2[1,0] = 3 * mV

Ma = StateMonitor(G2, 'Va', record=True)
Mb = StateMonitor(G2, 'Vb', record=True)

run(10 * ms)

plot(Ma.times, Ma[0])
plot(Mb.times, Mb[0])
show()
