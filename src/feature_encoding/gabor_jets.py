import numpy as np
np.seterr(all='raise')
from feature_encoding import *


class GaborJets(object):
    '''This class generates gabor jets'''
    
    def __init__(self, n_ang = 4, px_scales = [2.,3.,5.,9.,15.,20.,35.],
                 px_width = 36, phases = [0.,3*np.pi/2]):
        
        self.n_ang = n_ang # number of angles gabor filters are oriented
        self.px_scales = px_scales # filter scale (width) in pixels
        self.px_width = px_width # filter window width
        self.phases = phases # phases of gabor filters
        self.theta = np.linspace(0,np.pi,n_ang+1)[0:-1] # angle orientations
        
        self.fb = gabor_filterbank(n_ang,px_scales,px_width)
        
    def image2jets(self, im, n_jets):
        '''
        image 'im' is an 2d array, n_jets is the number of jets to generate
        across an evenly spaced grid
        '''
        return image2features(im,self.fb,n_jets)


if __name__ == "__main__":
    GJ = GaborJets()
    print GJ.fb.shape
    I = np.asarray(Image.open('/home/bill/python_packages/PIL/Images/lena.ppm'))
    I = np.mean(I,axis=2) # gray scale
    print I.shape
    jets = GJ.image2jets(I, 16)
    print jets.shape