'''
This will model and plot a set of Izhikevich neuron models
'''
from brian.library.IF import *
from brian.neurongroup import *
from brian import *
from utils import IzhikevichReset
        
def plot_Izhikevich(name,a,b,c,d):
    a,b,c,d = a/ms, b/ms, c*mV, d*mV/ms
    threshold = 30*mV
    

    eqs = Equations('''
                    dv/dt = (0.04/ms/mV)*v**2+(5/ms)*v+140*mV/ms-u+I/nF  : volt
                    du/dt = a*(b*v-u)                                    : volt/second
                    I                                                    : amp
                    ''')
    reset = '''
            v = c
            u += d
            '''

       
    G = NeuronGroup(1,eqs,threshold=threshold,reset=IzhikevichReset(c,d))
    
    G.v = -80*mV
    G.u = 0
    
    # Setup Monitoring
    Mv = StateMonitor(G, 'v', record=0)
    Mu = StateMonitor(G, 'u', record=0)
    MI = StateMonitor(G, 'I', record=0)
    p = SpikeMonitor(G)
    
    # Run
    stim = zeros(500)
    stim[100:400] = 10
    G.I = TimedArray(stim*nA, dt=1*ms)
    run(500*ms)
    
    # Plotting
    plot(Mv.times/ms, Mv[0]/mV, 'b', MI.times/ms,MI[0]/nA - 95,'r')
    xlabel('time (ms)')
    ylabel('v (mV), I (nA)')
    title(name)


if __name__ == '__main__':
    # Neuron Parameters
    neurons = {'regular spiking':(0.02,0.2,-65,8),
               'intrinsically bursting':(0.02,0.2,-55,4),
               'chattering':(0.02,0.2,-50,2),
               'fast spiking':(0.1,0.2,-65,8),
               'low-threshold spiking':(0.02,0.25,-65,8)}

    figure()
    i = 1
    for n,tup in neurons.iteritems():
        a,b,c,d = tup
        subplot(5,1,i)
        plot_Izhikevich(n, a, b, c, d)
        reinit()
        i += 1
    subplots_adjust(hspace=0.5)
    show()