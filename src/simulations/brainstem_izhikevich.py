from brian import *


##############################################
########### Define Neuron Equations ##########
##############################################

eqs = ''' 
dV/dt=(0.04/ms/mV)*V**2+(5/ms)*V+140*mV/ms-W+I : volt 
dW/dt=a*(b*V-W) : volt/second 
I : volt/second''' 

Vt = -30 * mvolt          # spike threshold
a = 0.02/ms
b = 0.2/ms
Vr = -65 * mvolt          # Vr = c, reset value
# d = ?

N_mVN = 200             # Number of mVN neurons (FTN + non-FTN)
psp = 7 * mV            # Connection strength/postsynaptic potential
tsim = 1000             # time length of simulation in milliseconds
mVN_noise = 5         #random input current noise floor in to populations of neurons
MN_noise = 7

##############################################
######### Create and Connect Nuclei ##########
##############################################

#Vestibular Ganglions/Afferents
vA = PoissonGroup(N_mVN,rates=lambda t:exp(-(((t/msecond)-tsim/2)/(tsim/5))**2)*40*Hz)

#Medial Vestibular Nucleus - FTNs and non-FTNs
mVN = NeuronGroup(N_mVN, eqs, threshold=Vt, reset=Vr)
mVN.v = -60 + 10*(rand(N_mVN)-0.5) 
mVN.I = TimedArray(mVN_noise*rand(tsim,N_mVN)*mV/ms, dt=1*ms)
mVN_FTN = mVN.subgroup(N_mVN/2)
mVN_VN = mVN.subgroup(N_mVN/2)

#Abducens Nucleus- Left and Right
rABD = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
rABD.v = -60 + 10*(rand(N_mVN/2)-0.5)
rABD.I = TimedArray(MN_noise*rand(tsim,N_mVN/2)*mV/ms, dt=1*ms)
lABD = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
lABD.v = -60 + 10*(rand(N_mVN/2)-0.5)
lABD.I = TimedArray(MN_noise*rand(tsim,N_mVN/2)*mV/ms, dt=1*ms)

#Oculomotor Nucleus - Right
rOMN = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
rOMN.v = -60 + 10*(rand(N_mVN/2)-0.5)
rOMN.I = TimedArray(MN_noise*rand(tsim,N_mVN/2)*mV/ms, dt=1*ms)

#Connections are defined by C_source_target
C_vA_mVN = Connection(vA, mVN, 'V')
C_vA_mVN.connect_one_to_one(vA, mVN, weight=10*mV)
C_mVN_FTN_rABD = Connection(mVN_FTN,rABD, 'V', weight=-psp, sparseness=0.1)
C_mVN_VN_lABD = Connection(mVN_VN,lABD, 'V', weight=psp, sparseness=0.05)
C_lABD_rOMN = Connection(lABD, rOMN, 'V', weight=4*mV, sparseness=0.05)


##############################################
############ Running and Plotting ############
##############################################
M_vA = SpikeMonitor(vA)
M_mVN = SpikeMonitor(mVN)
M_rABD = SpikeMonitor(rABD)
M_lABD = SpikeMonitor(lABD)
M_rOMN = SpikeMonitor(rOMN)
run(1*second)
subplot(5,1,1)
raster_plot(M_vA)
title('vA')
subplot(5,1,2)
raster_plot(M_mVN)
title('M_mVN')
subplot(5,1,3)
raster_plot(M_rABD)
title('M_rABD')
subplot(5,1,4)
raster_plot(M_lABD)
title('M_lABD')
subplot(5,1,5)
raster_plot(M_rOMN)
title('M_rOMN')
show()
