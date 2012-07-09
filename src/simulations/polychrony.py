'''
This experiment attempts to reproduce the results from
Izhikevich - 2006 - Polychronization: Computation with Spikes

author: bill lennon
date: 18 June 2012

TO DO:
    - Get STDP working properly.  Nearest spike learning only.
    - Monitor synaptic weight changes
    - Find/track polychronous groups
'''
from brian.library.IF import *
from brian.neurongroup import *
from brian import *
from brian.experimental.realtime_monitor import RealtimeConnectionMonitor
from scipy.sparse import rand as sprand
from cortex import *
from utils import *
import time
import matplotlib.pyplot as plt

set_global_preferences(useweave=True)
print 'building network...'
start = time.time()

########################################################################
# Network Parameters
########################################################################
sim_clock = Clock(dt=0.5*ms)    # simulation clock
input_clock = Clock(dt=1*ms)    # input current change clock
mon_clock = Clock(dt=1*ms)      # monitor clock
report_clock = Clock(dt=1000*ms)
Ne, Ni = 800, 200   # number of excitatory/inhibitory neurons
N = Ne + Ni
smax = 10 * mV        # max synapse strength
tau_pre = 20*ms
tau_post = 20*ms
Ap = .1
Am = -.1
plot_on = True


########################################################################
# Neurons
########################################################################
G = IzhikevichGroup(N, 'a', 0.2/ms, -65*mV, 'd', 1*ms, 1*ms, clock=sim_clock)        
Ge = G.subgroup(Ne)
Gi = G.subgroup(Ni)
Ge.a,Ge.d = 0.02/ms, 8*mV/ms
Gi.a,Gi.d = 0.1/ms, 2*mV/ms


########################################################################    
# Connections
########################################################################
# Ge -> G
Ce = DelayConnection(Ge,G,max_delay=20*ms)
Ce.connect_random(Ge,G,.05,weight=6.0*mV,delay=(0*ms,20*ms))

Ci = DelayConnection(Gi,Ge,max_delay=1*ms)
Ci.connect_random(Gi,Ge,.05,weight=-5.0*mV,delay=1*ms)
'''
w,d = random_weights_delays(Ne,N,.05,max_weight=6.0*mV,max_delay=20*ms)
Ce = DelayConnection(Ge,G,'ge', delay=d)
Ce.connect(Ge,G,w)

# Gi -> Ge
w,d = random_weights_delays(Ni,Ne,.05,max_weight=-5.0*mV,max_delay=1*ms)
Ci = DelayConnection(Gi,Ge,'gi', delay=d)
Ci.connect(Gi,Ge,w)
'''
stdp = ExponentialSTDP(Ce, tau_pre, tau_post, Ap, Am, wmax=smax,
                       clock=sim_clock, interactions='nearest')


########################################################################
# Input
########################################################################
@network_operation(input_clock)
def thalamic_input():
    stim = np.zeros_like(G.I)
    stim[np.random.randint(stim.shape[0])] = 20 * nA
    G.I = stim


########################################################################
# Monitor
########################################################################
Mse = SpikeMonitor(Ge)
Mve = StateMonitor(Ge, 'v', record=[0,Ne-1], clock=mon_clock)
MIe = StateMonitor(Ge, 'I', record=[0,Ne-1], clock=mon_clock)
Msi = SpikeMonitor(Gi)
Mvi = StateMonitor(Gi, 'v', record=[0,Ni-1], clock=mon_clock)
MIi = StateMonitor(Gi, 'I', record=[0,Ni-1], clock=mon_clock)
M = [Mse,Mve,MIe,Msi,Mvi,MIi]

RT = RealtimeConnectionMonitor(Ce)

########################################################################
# Plotting
########################################################################
if plot_on:
    ion()
    figure(0,figsize=(18,10))
    plot_args = dict(refresh=1000*ms, showlast=1000*ms)
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

@network_operation(report_clock)
def report_weights():
    print 'Total excitatory synaptic value: ', np.sum(Ce.W.alldata)

########################################################################
# Run simulation
########################################################################
net = Network(G,M,Ce,Ci,stdp,thalamic_input,report_weights,RT)
print 'network built. took %s seconds' % (time.time()-start)
print 'running...'
start = time.time()
net.run(20000*ms, report='text')
print 'done. took %s seconds' % (time.time()-start)
ioff()
show()
