import numpy as np
import pylab as pl
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import *
import Image

def gabor(px_filt,px_wind,theta,psi,lamda=3*np.pi/2,gamma=(5./8.)):
    '''
    px_filt: the width of the gabor filter in pixels
    px_wind: the width of the filter window in pixels
    theta: the angle of rotation of the filter
    psi: the phase of the filter; +3pi/2 for sin, 0 for cos
    lamda: the ratio of sinuosoidal frequency to gaussian minor axis width,
           i.e. quantifies the number of cyles to complete within the minor
           axis' 1 std width (approximately)
    gamma: minor axis to major axis ratio
    
    see Hecht-Nielsen, 1989 p 332; Hecht-Nielsen, 2007 p 180; 
    http://en.wikipedia.org/wiki/Gabor_filter
    '''
    sigma = px_filt**.5
    lamda /= sigma
    sigma_x = float(sigma)
    sigma_y = float(sigma)/gamma
    
    # Bounding box
    a = int(px_wind/2.)
    x = np.linspace(-a,a,px_wind)
    X,Y = np.meshgrid(x,x)
    
    # Rotation
    X_theta = X*np.cos(theta)+Y*np.sin(theta)
    Y_theta = -X*np.sin(theta)+Y*np.cos(theta)
    
    # Gabor
    env = np.exp(-((X_theta/sigma_x)**2 + (Y_theta/sigma_y)**2))
    gb = env * np.cos(lamda*X_theta+psi)
    
    return gb, X, Y

def gabor_filterbank(n_ang,px_scales,px_width):
    '''
    n_ang: number of angle orientations in [0,pi/2]
    px_scales: a list of scales in pixels
    px_width: width of filter window in pixels
    
    return numpy array filter bank of size 
    (px_width,px_width,n_ang*len(px_scales)*2)
    '''
    fb = np.zeros((px_width,px_width,n_ang*len(px_scales)*2))
    theta = np.linspace(0,np.pi/2,n_ang)
    phases = [0,3*np.pi/2]
    i=0
    for s in px_scales:
        for w in theta:
            for p in phases:
                fb[:,:,i], _, __ = gabor(s,px_width,w,p)
                i += 1
                
    return fb
    
if __name__ == "__main__":
    '''testing and plotting of filters'''
    
    # filterbank parameters
    n_ang = 8 # number of angles
    px_scales = [2.,3.,5.,9.,15.,20.,35.] # filter width
    px_width = 36 # window width
    theta = np.linspace(0,np.pi,n_ang+1)[0:-1]
    phases = [0.,3*np.pi/2]
       
    # Plot gabor filterbank (generated separately)
    canvas = np.zeros((len(px_scales) * px_width, n_ang * px_width * len(phases)))
    i,j,k = 0,0,0
    for s in px_scales:
        for p in phases:
            for w in theta:
                Z,X,Y = gabor(s,px_width,w,p)
                canvas[i*px_width:i*px_width+px_width,(j+k*n_ang)*px_width:(j+k*n_ang)*px_width+px_width] = Z
                j+=1
            j=0
            k+=1
        k=0
        i+=1
    #fig = pl.figure()
    #ax = Axes3D(fig)
    #ax.plot_wireframe(X,Y,Z)
    fig = pl.figure(0)
    pl.imshow(canvas,cmap=cm.gray)
    pl.title('gabor filter bank')
    
    I = np.asarray(Image.open('/home/bill/python_packages/PIL/Images/lena.ppm'))
    I = np.mean(I,axis=2) # gray scale
    fig = pl.figure(1)
    pl.imshow(I,cmap=cm.gray)
    pl.title('test image, lena')
    
    # test generate fb
    fb = gabor_filterbank(n_ang,px_scales,I.shape[0])
    
    fig = pl.figure(2)
    n = fb.shape[2]
    k = np.ceil(n**.5)
    print k
    for i in range(n):
        pl.subplot(k,k,i)
        I_f = fftconvolve(I,fb[:,:,i],mode='same')
        pl.imshow(I_f,cmap=cm.gray)
    pl.title('filtered by one gabor')
    
    pl.show()