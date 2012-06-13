'''
This will reproduce the simple network of excitatory
and inhibitory cortical neurons driven by thalamic
stimulation from:
Izhikevich - 2003 - Simple Model of Spiking Neurons
'''
from brian.library.IF import *
from brian.neurongroup import *
from brian import *
from brian_utils import IzhikevichReset
import time

defaultclock.dt = .5*ms

########################################################################
# Network Parameters
########################################################################
Ne, Ni = 800, 200
N = Ne + Ni
a,b,c,d = (0.02+0.08*rand(N))/ms, (0.25-0.05*rand(N))/ms, (-65+15*rand(N)**2)*mV, (8-6*rand(N)**2)*mV/ms
threshold = 30*mV
sim_len = 1000

eqs = Equations('''
                dv/dt = (0.04/ms/mV)*v**2+(5/ms)*v+140*mV/ms-u+thal/nF : volt
                du/dt = a*(b*v-u) : volt/second
                thal : amp
                ''')

reset = '''
        v = c
        u = u + d
        '''


########################################################################
# Neurons
########################################################################        
G = NeuronGroup(N,eqs,threshold=threshold,reset=IzhikevichReset(c,d),freeze=False)
Ge = G.subgroup(Ne)
Gi = G.subgroup(Ni)
G.v = (-80 + randn(N))* mV
G.u = randn(N) * mV/ms

# random thalamic input
Ge.thal = TimedArray(5*randn(sim_len,Ne)*nA,dt=1*ms)
Gi.thal = TimedArray(3*randn(sim_len,Ni)*nA,dt=1*ms)


########################################################################    
# Connections
########################################################################
C = Connection(G,G,'v')
C.connect(Ge,G,.4*rand(Ne,Ni+Ne)*mV)
C.connect(Gi,G,-1*rand(Ni,Ne+Ni)*mV)


########################################################################
# Monitor
########################################################################
M = SpikeMonitor(G)
Mv = StateMonitor(G, 'v', record=[0,999])


########################################################################
# Run simulation
########################################################################
print 'running...'
start = time.time()
run(sim_len * ms)
print 'done. took %s seconds' % (time.time()-start)


########################################################################
# Plotting
########################################################################
figure()
subplot(311)
raster_plot(M, title='Cortical Neurons - Firing Times', newfigure=False)
xlabel('time (ms)')
subplot(312)
plot(Mv.times/ms, Mv[0]/mV)
title('Excitatory Neuron trace')
xlabel('time (ms)')
ylabel('membrane potential (mV)')
subplot(313)
plot(Mv.times/ms, Mv[999]/mV)
xlabel('time (ms)')
title('Inhibitory Neuron trace')
ylabel('membrane potential (mV)')
subplots_adjust(hspace=0.25)
show()