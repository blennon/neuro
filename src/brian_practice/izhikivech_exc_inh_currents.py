'''
In this problem we will implement excitatory and inhibitory
currents with different time constants to an Izhikevich neuron
'''
from brian.neurongroup import * # for some reason Eclipse likes this
from brian import *
from brian_utils import IzhikevichReset

########################################################################
# Network Parameters
########################################################################
taue, taui = 2 * ms, 5 * ms
Vt = 30 * mV
a = 0.02/ms
b = 0.2/ms
c = -65*mV
d = 8*mV/ms

eqs = Equations('''
                dv/dt=(0.04/ms/mV)*v**2+(5/ms)*v+140*mV/ms-u+(ge-gi)/ms : volt 
                du/dt=a*(b*v-u) : volt/second 
                dge/dt = -ge/taue            : volt
                dgi/dt = -gi/taui            : volt
                ''')

reset = '''
        v = c
        u = u + d
        '''


########################################################################
# Neurons
######################################################################## 
# declare input neuron spike times, format (neuron_number, spike_time)
spike_times = [(0, 205 * ms), (0, 210 * ms), (1, 238 * ms), (0, 250 * ms),
               (0, 255 * ms)]

# Instantiate Neurons
G1 = SpikeGeneratorGroup(2, spike_times)
G2 = NeuronGroup(1,eqs,threshold=Vt,reset=IzhikevichReset(c,d),freeze=False)


########################################################################    
# Connections
########################################################################
C1, C2 = Connection(G1, G2, 'ge'), Connection(G1, G2, 'gi')
C1[0,0], C2[1,0] = 10 * mV, 1 * mV


########################################################################
# Monitor
########################################################################
Mv = StateMonitor(G2, 'v', record=True)
Mge = StateMonitor(G2, 'ge', record=True)
Mgi = StateMonitor(G2, 'gi', record=True)


########################################################################
# Run simulation
########################################################################
run(400 * ms)


########################################################################
# Plotting
########################################################################
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