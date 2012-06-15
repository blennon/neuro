'''
Created on Jun 5, 2012

@author: bill
'''
import numpy as np
import pylab as pl

class RealToSpikes(object):
    '''
    This class is to encode real valued vectors into
    spike time data for each presentation
    
    Methodology:
    - Each position in the vector maps to an array
    of receptive fields.  These receptive fields are
    spread across the range of the values that this position
    in the vector takes on.  For now this array of receptive
    fields is static.
    - Receptive fields are modeled of RFs.  Arrays of these
    have been shown to have useful properties for feature
    encoding (Baldi and Heiligenberg, 1988)
    - Thus values of the elements of the RF array will take
    on values in [0,1] in a distributed fashion.  Many will
    be near zero.
    - Spike time encoding then takes place by assigning early
    spike times to array elements with high values and later
    spike times (or none at all) to elements with lower values.
    This method is used successfully in Bohte et al 2002.
    - An alternative to this, to be tested, will be to use these
    RF values as current input to target neurons.  Then a series
    of real valued vectors can be fed into this encoder.
    - The result is a sparse distributed spiking representation
    of a real valued vector.
    
    '''

    def __init__(self, data, num_RFs=10):
        '''
        Given the input data or large enough sample of it, set up
        the encoder.
        
        Parameters:
        data - a numpy array, size (num_features, num_samples)
        num_RFs - number of receptive fields for each position
        in the array.  essentially the population size for each
        position in the array.
        '''
        self.num_RFs = num_RFs
        self.RFs = ReceptiveFields(data, num_RFs)
        self.n,self.m = data.shape
        
    def spikes(self, v, t, min_exc=.2):
        '''
        v is a 1-d numpy array -- a real-valued input vector
        describing sensory input to a system to be converted into
        neuron spikes spread across a time window 't'.
        
        t is the time window length to produce spikes across,
        lower receptive field values spike later, or not at all.
        
        min_exc in [0,1] is the minimum excitation/activation
        of a receptive field in order to register a spike.
        
        returns [(neuron_number,spike_time),...]
        '''
        r = self.RFs.response(v)
        spike_times = self.linear_spike_times(r, t, min_exc)

        return spike_times
    
    def linear_spike_times(self, rf, t, min_exc):
        '''
        take a numpy array of size (n,self.num_RFs) (n is the len of the
        real valued input vector to be converted to spike times) of RF
        response values and return an array of spike times.
        
        These spike times are spread out linearly across t, the high
        RF values spike first, the lower ones later.  In order to spike
        these neurons must meet a minimum excitation (i.e. firing rate)
        threshold.
        '''
        m = float(t)/(min_exc - 1.0)
        b = t - m * min_exc
        spike_times = m * rf + b
        
        s = spike_times.flatten()
        n = np.nonzero(s<=t)[0] # neuron numbers of spikes before t
        t = s[n] # times of spikes for neurons in n

        return zip(n,t)
    
    def spike_raster(self, times):
        '''raster plot of spike times'''
        pl.figure()
        for neuron,time in times:
            pl.plot(time,neuron,'o',color='b')
        pl.ylim([0,self.n*self.num_RFs])
        pl.xlabel('Time')
        pl.ylabel('Neuron Number')
        pl.title('Spike times - Raster plot')


class ReceptiveFields(object):
    '''
    This class will create receptive fields for real-valued data 
    and produce a response for a particular input
    '''
    
    def __init__(self, num_RFs, data=None, online=False):
        '''
        num_RFs -- number of receptive fields to encode data in
        
        data -- a numpy 2-d array of the data or significant sample,
        size (num_features,num-samples)
        
        If data is None, assumes that the receptive field locations will
        be determined in an online manner, i.e. every time a new input is
        received, the RF array will be adjust to spread out maximally over all
        of the data that's been seen so far.
        '''
        self.num_RFs = num_RFs
        if data is not None:
            self.min,self.max = np.min(data,axis=1), np.max(data,axis=1)
            self.spread_RFs()
            self.online = online
        else:
            self.online = True
            self.init = False
            print 'Waiting for first two inputs to initialize Receptive Fields...'
    
    def get_parameters(self):
        return self.C, self.w
    
    def new_max_min(self, input):
        '''calculate the new min,max values of the data seen so far'''
        if not self.init:
            self.min, self.max = input, input.copy()
            self.init = True
            return
        self.max[self.max<input] = input[self.max<input]
        self.min[input<self.min] = input[input<self.min]
        
    def response(self, input):
        '''
        input is an (n,) array to be converted into receptive field
        response values
        '''
        if self.online:
            self.new_max_min(input)
            self.spread_RFs()
            
        return self.gaussian_field(input[...,None], self.C, self.w)
    
    def gaussian_field(self, x, C, w):
        '''
        x is an (n,) array
        C is (n,self.num_RFs) array
        w is (n,) array
        
        returns a (n,self.num_RFs) array
        '''
        if np.array_equal(w, np.zeros_like(w)):
            return np.zeros_like(C)
        
        return np.exp( -((x - C).T / w ) ** 2.0).T
    
    def spread_RFs(self, beta=1.0):
        '''
        beta -- an overlap parameter.  somewhere in [1.0,2.0]
        supposedly works well
        
        set parameter vectors for the 'self.num_RFs' number
        of receptive fields as two arrays.
        
        this spreads the RFs evenly over the range [min,max]
        '''
        N = self.num_RFs
        C = np.array([self.min + (2*(i+1)-3)/2. * (self.max-self.min)/(N-2.) for i in range(N)]).T
        w = 1/beta * (self.max-self.min)/(N-2.)
        self.C, self.w = C, w

    def plot_rfs(self, row=0, num_pts=1000):
        '''
        remember to run pl.show()
        '''
        pl.figure()
        C,w = self.C[row,:], self.w[row]
        min,max = np.min(C)-2*w, np.max(C)+2*w
        x = np.arange(min,max,(max-min)/num_pts)
        R = self.gaussian_field(x,C[...,None],w)
        for i in range(R.shape[0]):
            pl.plot(x, R[i,:])
        pl.title('Receptive fields for row %s of input vector' % row)
        pl.ylabel('Receptive Field Value')
        pl.xlabel('Input Value')


if __name__ == '__main__':
    RF = ReceptiveFields(7)
    print RF.response(np.array([1,2,1]))
    RF.response(np.array([2,1,3]))
    RF.plot_rfs()
    pl.show()


    '''
    R = RealToSpikes(10*np.random.rand(2,1000),7)
    R.RFs.plot_rfs()
    input = np.array([9,2])
    print input
    spikes = R.spikes(input,5.0)
    print spikes
    R.spike_raster(spikes)
    pl.show()
    '''
