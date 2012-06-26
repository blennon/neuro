'''
Created on Jun 25, 2012

@author: bill
'''
from cortex.neuron_groups import IzhikevichGroup
from brian.neurongroup import *
from brian import *

class GranuleGolgi(IzhikevichGroup):
    '''
    Input layer to cerebellar cortex featuring granule cells
    and inhibitory Golgi cells
    
    Contains parameters defining the behavior of each cell type.
    
    ===========================================================
    TO DO:
        1 neuron parameters: a,b,c,d to match physiology
        2 model AMPA, NMDA and GABA channels with different
          time constants (conductances)
        4 model topology with connection set algebra using 
          python-csa
    ===========================================================
    
    Buonomano and Mauk (1994) anatomical parameters:
    - 10000 GC, 900 GG, 500 MF, 1 PC
    - 100 GC, 20 MF -> 1 GG
    
    Biological parameters:
    - GC/GG ~= 1000/1 (numbers of neurons)
    - 4 GG -> 1 GC; 1 GC -> 5-10 GG [Eccles 1973; Palkovits et al 1971]
    - GG receives ~4800 inputs from PFs, 230 inputs from MF
      [Pelionisz and Szentagothai, 1973]
    - each GG synapses onto up to ~5700 GCs [cat; Palkovits et al 1971]
    - 1 MF -> 400-500 GCs; 4-5 MF -> 1 GC [Ito, 2012]
    - 1 mm^3 contains ~1000 GG [cat; Palkovits et al 1971]
    
    Deriving probability of connection:
    - C: NxM matrix (source,target) neurons
    - p = nnz(C)/(N*M)
    - define: divergence - the number of target neurons contacted by a
                           single source neuron
    - define: convergence - the number of source neurons contacting a
                            a single target neuron
    - ==> N*div = M*conv = nnz(C) ==> p = N*div/(N*M) = M*conv/(N*M)
    - ==> p = conv/N = div/M (by substitution)
    
    Derived parameters:
      => MF -> GC sparsity: 500/1000000 ~= 5/N_mf
          => N_mf = 5*1000000/500 = 100000
      => GG -> GC sparsity 5700/1000000, 4/1000
      => GC -> GG sparsity 10/1000, 4800/1000000
      => MF -> GG sparsity 230/100000
    '''
    
    # Physiology (Izhikevich neuron parameters)
    a_gc, b_gc, c_gc, d_gc = 0.02/ms, 0.2/ms, -65*mV, 8*mV/ms
    a_gg, b_gg, c_gg, d_gg = 0.02/ms, 0.2/ms, -65*mV, 8*mV/ms
    taue_gc, taui_gc, taue_gg, taui_gg = 1*ms, 1*ms, 1*ms, 1*ms
    
    def __init__(self, N_gc, gc_gg_ratio = 1000):
        '''
        N_gc: number of granule cells
        '''
        self.N_gc, self.N_gg = N_gc, int(N_gc/gc_gg_ratio)
        super(GranuleGolgi, self).__init__(N_gc+self.N_gg,'a','b','c','d',
                                           'taue','taui')
            
        # Anatomical parameters
        N_gg_hyp = 1000                        # number of Gg neurons in 1 mm^3
        N_gc_hyp = 1000*N_gg_hyp               # number of GC based on ratios
        self.p_mf2gc = 500./N_gc_hyp           # MF -> GC connection probability
        self.p_gg2gc = 5700./N_gc_hyp          # GG -> GC connection probability
        self.p_gc2gg = 10./N_gg_hyp            # GC -> GG connection probability
        self.p_mf2gg = 230./(5.*N_gc_hyp/500.) # MF -> GG connection probability
        
        # Synaptic weights
        self.w_gc2gg = .1*mV
        self.w_gg2gc = .1*mV
        self.w_mf2gc = .1*mV
        self.w_mf2gg = .1*mV
        
        self.GC = self.subgroup(N_gc)
        self.GG = self.subgroup(self.N_gg)
        self.setup()
        
    def setup(self):
        '''set the neuron parameters connections'''
        self.GC.a, self.GC.b = self.a_gc, self.b_gc
        self.GC.c, self.GC.d = self.c_gc, self.d_gc
        self.GC.taue, self.GC.taui = self.taue_gc, self.taui_gc
        self.GC.a, self.GC.b = self.a_gc, self.b_gc
        self.GC.c, self.GC.d = self.c_gc, self.d_gc
        self.GC.taue, self.GC.taui = self.taue_gc, self.taui_gc
        self.connect_gc_gg()

    def connect_gc_gg(self):
        '''reciprocally connect the granule cells and golgi cells'''
        self.C_gc_gg = Connection(self, self, 'ge')
        self.C_gc_gg.connect_random(self.GC, self.GG, sparseness=self.p_gc2gg,
                                    weight=self.w_gc2gg)
        self.C_gc_gg.connect_random(self.GG, self.GC, sparseness=self.p_gg2gc,
                                    weight=self.w_gg2gc)
    
    def connect_mf(self, ng):
        '''Connect neuron group 'ng' to GC and GG acting as mossy fiber'''
        print 'Warning: connect_mf() only supports one neuron group as input for now'
        self.C_input = Connection(ng,self,'ge')
        self.C_input.connect_random(ng,self.GC, sparseness=self.p_mf2gc,
                                    weight=self.w_mf2gc)
        self.C_input.connect_random(ng, self.GC, sparseness=self.p_mf2GG,
                                    weight=self.w_mf2gg)
        print 'Connected %s to granule-golgi cell layer' % (ng)

if __name__ == "__main__":
    G = GranuleGolgi(1000,100)
    print G
