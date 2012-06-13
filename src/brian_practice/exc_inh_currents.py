'''
In this problem we will implement excitatory and inhibitory
currents with different time constants to a neuron

The target neuron membrane potential is described by:
tau_m * dV/dt = -V + ge - gi
tau_e * dge/dt = -ge
tau_i * dgi/dt = -gi

where ge and gi are the excitatory and inhibitory "states"
of the target neuron, respectively.  In Brian, a neuron can track
multiple "states" (e.g. exc, inh, metabotropic, etc) and use these
states to govern the overall membrane potential of the neruon.
tau_* are the time constants for the membrane potential, excitatory 
and inhibitory synaptic time constants of the neuron, respectively.
'''
from brian.neurongroup import * # for some reason Eclipse likes this
from brian import *

tau_m, tau_e, tau_i = 20 * ms, 1 * ms, 20 * ms
Vt, Vr = 10 * mV, 0 * mV

eqs = Equations('''
                dV/dt = (-V+ge-gi)/tau_m : volt
                dge/dt = -ge/tau_e       : volt
                dgi/dt = -gi/tau_i       : volt
                ''')

# declare input neuron spike times, format (neuron_number, spike_time)
spike_times = [(0, 1 * ms), (0, 10 * ms), (1, 40 * ms), (0, 50 * ms),
               (0, 55 * ms)]

# Instantiate Neurons
G1 = SpikeGeneratorGroup(2, spike_times)
G2 = NeuronGroup(N=1, model=eqs, threshold=Vt, reset=Vr)

# Create Connections
C1, C2 = Connection(G1, G2, 'ge'), Connection(G1, G2, 'gi')
C1[0,0], C2[1,0] = 3 * mV, 3 * mV

# Setup Monitoring
Mv = StateMonitor(G2, 'V', record=True)
Mge = StateMonitor(G2, 'ge', record=True)
Mgi = StateMonitor(G2, 'gi', record=True)

run(100 * ms)

figure()
subplot(211)
plot(Mv.times, Mv[0])
xlabel('time (ms)')
ylabel('membrane potential (mV)')
subplot(212)
plot(Mge.times, Mge[0])
plot(Mgi.times, Mgi[0])
xlabel('time (ms)')
ylabel('membrane potential (mV)')
show()