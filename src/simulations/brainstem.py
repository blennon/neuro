from brian import *


##############################################
########### Define Neuron Equations ##########
##############################################
eqs = '''
dv/dt = (I+ge+gi-(v+49*mV))/(30*ms) : volt
dge/dt = -ge/(5*ms) : volt
dgi/dt = -gi/(10*ms) : volt
I : volt
'''



Vt = -50 * mV          # threshold potential
Vr = -60 * mV          # reset value
N_mVN = 200            # Number of mVN neurons (FTN + non-FTN)
psp = 0* mV            # Connection strength/postsynaptic potential

##############################################
######### Create and Connect Nuclei ##########
##############################################

#Vestibular Ganglions/Afferents
vA = PoissonGroup(N_mVN,rates=lambda t: t*40*Hz)

#Medial Vestibular Nucleus - FTNs and non-FTNs
mVN = NeuronGroup(N_mVN, eqs, threshold=Vt, reset=Vr)
mVN.v = -60 + 30*(rand(N_mVN)-0.5) #randomly initialize the state of these neurons
mVN_FTN = mVN.subgroup(N_mVN/2)
mVN_VN = mVN.subgroup(N_mVN/2)

#Abducens Nucleus- Left and Right
rABD = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
rABD.v = -60 + 30*(rand(N_mVN/2)-0.5)
lABD = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
lABD.v = -60 + 30*(rand(N_mVN/2)-0.5)

#Oculomotor Nucleus - Right
rOMN = NeuronGroup(N_mVN/2, eqs, threshold=Vt, reset=Vr)
rOMN.v = -60 + 30*(rand(N_mVN/2)-0.5)

#Connections are defined by C_source_target
C_vA_mVN = Connection(vA, mVN, 'ge')
C_vA_mVN.connect_one_to_one(vA, mVN, weight=psp)
C_mVN_FTN_rABD = Connection(mVN_FTN,rABD, 'gi', weight=psp, sparseness=0.2)
C_mVN_VN_lABD = Connection(mVN_VN,lABD, 'ge', weight=psp, sparseness=0.2)
C_lABD_rOMN = Connection(lABD, rOMN, 'ge', weight=psp, sparseness=0.2)


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
