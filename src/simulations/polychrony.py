'''
This experiment attempts to reproduce the results from
Izhikevich - 2006 - Polychronization: Computation with Spikes

author: bill lennon
date: 18 June 2012
'''
from brian.library.IF import *
from brian.neurongroup import *
from brian import *
from scipy.sparse import rand as sprand
from cortex import *
from utils import *
import time
import matplotlib.pyplot as plt

defaultclock.dt = .5*ms
print 'building network...'
start = time.time()

########################################################################
# Network Parameters
########################################################################
Ne, Ni = 800, 200   # number of excitatory/inhibitory neurons
N = Ne + Ni
sm = 10 * mV        # max synapse strength


########################################################################
# Neurons
########################################################################        
Ge = IzhikevichGroup(Ne, 0.02/ms, 0.2/ms, -65*mV, 8*mV/ms, 1*ms, 1*ms)
Gi = IzhikevichGroup(Ni, 0.1/ms, 0.2/ms, -65*mV, 2*mV/ms, 1*ms, 1*ms)


########################################################################    
# Connections
########################################################################
# Ge -> Ge
w,d = random_weights_delays(Ne,Ne,.1,max_weight=2.0*mV,max_delay=20*ms)
Cee = DelayConnection(Ge,Ge,'ge', delay=d)
Cee.connect(Ge,Ge,w)

# Ge -> Gi
w,d = random_weights_delays(Ne,Ni,.1,max_weight=2.0*mV,max_delay=20*ms)
Cei = DelayConnection(Ge,Gi,'ge', delay=d)
Cei.connect(Ge,Gi,w)

# Gi -> Ge
w,d = random_weights_delays(Ni,Ne,.1,max_weight=-5.0*mV,max_delay=1*ms)
Cie = DelayConnection(Gi,Ge,'gi', delay=d)
Cie.connect(Gi,Ge,w)


########################################################################
# Input
########################################################################
@network_operation
def thalamic_input():
    Ge.I = 6*np.random.rand(Ne)*nA
    Gi.I = 2*np.random.rand(Ni)*nA


########################################################################
# Monitor
########################################################################
Mse = SpikeMonitor(Ge)
Mve = StateMonitor(Ge, 'v', record=[0,Ne-1])
MIe = StateMonitor(Ge, 'I', record=[0,Ne-1])
Msi = SpikeMonitor(Gi)
Mvi = StateMonitor(Gi, 'v', record=[0,Ni-1])
MIi = StateMonitor(Gi, 'I', record=[0,Ni-1])
M = [Mse,Mve,MIe,Msi,Mvi,MIi]


########################################################################
# Plotting
########################################################################
ion()
figure(0,figsize=(20,10))
plot_args = dict(refresh=500*ms, showlast=500*ms)
subplot(221)
raster_plot(Mse, title='Exc Neurons - Firing Times', newfigure=False, **plot_args)
xlabel('time (ms)')
subplot(222)
Mve.plot(**plot_args)
title('Excitatory Neurons trace')
xlabel('time (s)')
ylabel('membrane potential (V)')
subplot(223)
raster_plot(Msi, title='Inh Neurons - Firing Times', newfigure=False, **plot_args)
xlabel('time (ms)')
subplot(224)
Mvi.plot(**plot_args)
title('Inhibitory Neurons trace')
xlabel('time (s)')
ylabel('membrane potential (V)')
subplots_adjust(hspace=0.25)


########################################################################
# Run simulation
########################################################################
net = Network(Ge,Gi,Cee,Cei,Cie,M,thalamic_input)
print 'network built. took %s seconds' % (time.time()-start)
print 'running...'
start = time.time()
net.run(3000 * ms)
print 'done. took %s seconds' % (time.time()-start)
ioff()
show()
