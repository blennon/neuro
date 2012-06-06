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
        
    def spikes(self, v, t):
        '''
        v is a 1-d numpy array
        t is the time window length to produce spikes
        
        return spikes a sparse array of size (an n*num_RFs, t)
        '''
        r = self.RFs.response(v)
        pass


class ReceptiveFields(object):
    '''
    This class will produce receptive fields
    '''
    
    def __init__(self, data, num_RFs):
        '''
        data -- a numpy 2-d array of the data or significant sample,
        size (num_features,num-samples)
        num_RFs -- number of receptive fields to encode data in
        '''
        self.num_RFs = num_RFs
        self.C, self.w = self.spread(data)
    
    def parameters(self):
        return self.C, self.w
           
    def response(self, x):
        '''
        x is an (n,) array
        '''
        return self.gaussian_field(x[...,None], self.C, self.w)
    
    def gaussian_field(self, x, C, w):
        '''
        x is an (n,) array
        C is (n,self.num_RFs) array
        w is (n,) array
        
        returns a (n,self.num_RFs) array
        '''
        return np.exp( -((x - C).T / w ) ** 2).T
    
    def spread(self, data, beta=1.5):
        '''
        beta -- an overlap parameter.  somewhere in [1.0,2.0]
        supposedly works well
        
        return parameter vectors for the 'self.num_RFs' number
        of receptive fields as two arrays.
        
        this spreads the RFs evenly over the range [min,max]
        '''
        N = self.num_RFs
        min,max = np.min(data,axis=1), np.max(data,axis=1)
        C = np.array([min + (2*(i+1)-3)/2. * (max-min)/(N-2.) for i in range(N)]).T
        w = 1/beta * (max-min)/(N-2.)
        
        return C, w

    def plot_rfs(self, row=0, num_pts=1000):
        '''
        remember to run pl.show()
        '''
        C,w = self.C[row,:], self.w[row]
        min,max = np.min(C)-2*w, np.max(C)+2*w
        x = np.arange(min,max,(max-min)/num_pts)
        print min,max
        R = self.response(x,C[...,None],w)
        for i in range(R.shape[0]):
            pl.plot(x, R[i,:])


if __name__ == '__main__':
    data = np.array([100*np.random.rand(1000), 10*np.random.rand(1000)])
    
    RF = ReceptiveFields(data,7)

    print RF.response(np.array([1,2])).shape

