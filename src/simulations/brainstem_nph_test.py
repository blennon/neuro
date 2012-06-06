from brian import *


############################################################################################
########### Define Neuron Equations ########################################################
############################################################################################

eqs = ''' 
dV/dt=(0.04/ms/mV)*V**2+(5/ms)*V+140*mV/ms-W+I : volt 
dW/dt=a*(b*V-W) : volt/second 
I : volt/second''' 

Vt = -30 * mvolt        # spike threshold
a = 0.02/ms
b = 0.2/ms
Vr = -65 * mvolt        # Vr = c, reset value
# d = ?

N_mVN = 200             # Number of mVN neurons (FTN + non-FTN)
N_NPH = N_mVN           # Number of NPH neurons
psp1 = 10 * mV          # Connection strength/postsynaptic potential
psp2 = 5 * mV
tsim = 1000             # time length of simulation in milliseconds
mVN_noise = 5           # random input current noise floor in to populations of neurons
NPH_noise = 1
MN_noise = 7
NPH_sparse = 0.065
NPH_delay = 1 * msecond
OMN_delay = 3 * msecond

############################################################################################
############### Create Nuclei ##############################################################
############################################################################################

# Vestibular Ganglions/Afferents
vA = PoissonGroup(N_mVN,rates=lambda t:exp(-(((t/msecond)-tsim/2)/(tsim/5))**2)*40*Hz)

# Medial Vestibular Nucleus - FTNs and non-FTNs
mVN = NeuronGroup(N_mVN, eqs, threshold=Vt, reset=Vr)
mVN.v = -60 + 10*(rand(N_mVN)-0.5) 
mVN.I = TimedArray(mVN_noise*rand(tsim,N_mVN)*mV/ms, dt=1*ms)
mVN_FTN = mVN.subgroup(N_mVN/2)
mVN_VN = mVN.subgroup(N_mVN/2)

# NPH - separate channels for FTNs and non-FTNs (Buttner-Ennever 2006)
NPH = NeuronGroup(N_NPH, eqs, threshold=Vt, reset=Vr)
NPH.v = -60 + 10*(rand(N_NPH)-0.5) 
NPH.I = TimedArray(NPH_noise*rand(tsim,N_NPH)*mV/ms, dt=1*ms)
NPH_FTN = NPH.subgroup(N_NPH/2)
NPH_VN = NPH.subgroup(N_NPH/2)

# Abducens Nucleus- Left and Right
rABD = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
rABD.v = -60 + 10*(rand(N_mVN/2)-0.5)
rABD.I = TimedArray(MN_noise*rand(tsim,N_mVN/2)*mV/ms, dt=1*ms)
lABD = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
lABD.v = -60 + 10*(rand(N_mVN/2)-0.5)
lABD.I = TimedArray(MN_noise*rand(tsim,N_mVN/2)*mV/ms, dt=1*ms)

# Oculomotor Nucleus - Right
rOMN = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
rOMN.v = -60 + 10*(rand(N_mVN/2)-0.5)
rOMN.I = TimedArray(MN_noise*rand(tsim,N_mVN/2)*mV/ms, dt=1*ms)

############################################################################################
############## Connect Nuclei ##############################################################
############################################################################################

# vA to mVN
C_vA_mVN = Connection(vA, mVN, 'V')
C_vA_mVN.connect_one_to_one(vA, mVN, weight=10*mV)

# mVN to NPH
C_mVN_FTN_NPH_FTN = Connection(mVN_FTN,NPH_FTN, 'V', weight=lambda:psp1*rand(), sparseness=0.06, delay = NPH_delay) #separate channels
C_mVN_VN_NPH_VN = Connection(mVN_VN,NPH_VN, 'V', weight=lambda:psp1*rand(), sparseness=0.06, delay = NPH_delay)

# NPH to MVN
C_NPH_FTN_mVN_FTN = Connection(NPH_FTN,mVN_FTN, 'V', weight=lambda:psp2*rand(), sparseness=0.05, delay = NPH_delay)
C_NPH_VN_mVN_VN = Connection(NPH_VN,mVN_VN, 'V', weight=lambda:psp2*rand(), sparseness=0.05, delay = NPH_delay)
NPH_FTN_stp = STP(C_NPH_FTN_mVN_FTN,taud=10*ms,tauf=1*ms,U=.9)
NPH_VN_stp = STP(C_NPH_VN_mVN_VN,taud=10*ms,tauf=1*ms,U=.9)

# NPH to NPH recurrent synapses
C_NPH_FTN_NPH_FTN = Connection(NPH_FTN,NPH_FTN, 'V', weight=lambda:psp1*rand(), sparseness=0.07, delay = NPH_delay)
C_NPH_VN_NP_VN = Connection(NPH_VN,NPH_VN, 'V', weight=lambda:psp1*rand(), sparseness=0.07, delay = NPH_delay)

# mVN FTNs to rABD
C_mVN_FTN_rABD = Connection(mVN_FTN,rABD, 'V', weight=lambda:-psp1*rand(), sparseness=0.1, delay = OMN_delay)

# mVN non-FTNs to lABD
C_mVN_VN_lABD = Connection(mVN_VN,lABD, 'V', weight=lambda:psp1*rand(), sparseness=0.05, delay = OMN_delay)

# lABD to rOMN
C_lABD_rOMN = Connection(lABD, rOMN, 'V', weight=lambda:psp1*rand(), sparseness=0.05, delay = OMN_delay)

############################################################################################
############ Running and Plotting ##########################################################
############################################################################################

M_vA = SpikeMonitor(vA)
M_mVN_FTN = SpikeMonitor(mVN_FTN)
M_mVN_VN = SpikeMonitor(mVN_VN)
M_NPH_FTN = SpikeMonitor(NPH_FTN)
M_NPH_VN = SpikeMonitor(NPH_VN)
M_rABD = SpikeMonitor(rABD)
M_lABD = SpikeMonitor(lABD)
M_rOMN = SpikeMonitor(rOMN)
R_rOMN = PopulationRateMonitor(rOMN)
R_rABD = PopulationRateMonitor(rABD)
run(tsim * ms)
subplot(7,1,1)
raster_plot(M_vA)
title('M_vA')
subplot(7,1,2)
raster_plot(M_mVN_FTN)
title('M_mVN_FTN')
subplot(7,1,3)
raster_plot(M_mVN_VN)
title('M_mVN_VN')
subplot(7,1,4)
raster_plot(M_NPH_FTN)
title('M_NPH_FTN')
subplot(7,1,5)
raster_plot(M_NPH_VN)
title('M_NPH_VN')
subplot(7,1,6)
raster_plot(M_rABD)
title('M_rABD')
subplot(7,1,7)
raster_plot(M_rOMN)
title('M_rOMN')
show()

