import numpy as np
import matplotlib.pyplot as plt

def image_grid(im_size,filt_size,n_pts):
    '''
    given an image 'im' in numpy array format, return the coordinates of
    n_pts (must be a square number) evenly spaced across the image with enough
    room left on edges for the filter
    
    returns a list of tuples of grid pts, i.e. [(i,j),...]
    '''
    a,b = np.ceil(filt_size[0]/2.), np.ceil(filt_size[1]/2.)
    m,n = im_size
    
    i = int(n_pts ** .5)
    if i**2 != n_pts:
        raise Exception('n_pts must be a square number')
    
    x = np.linspace(a,m-a,i)
    y = np.linspace(b,n-b,i)
    grid_pts = []
    for i in x:
        for j in y:
            grid_pts.append((int(i),int(j)))
    return grid_pts

def feature_vector(im,grid_pt,fb):
    '''
    generate a feature vector (aka "jet") at pt 'grid_pt' (a tuple) by
    taking the dot product of the image surrounding that point with each filter
    in the filter bank 'fb'.  the filters are along the third axis
    '''
    m,n,p = fb.shape
    a,b = np.ceil(m/2.), np.ceil(n/2.)
    i,j = grid_pt
    return ((im[i-a:i+a,j-b:j+b,None]*fb).sum(axis=0).sum(axis=0))**.5

def image2features(im,fb,n_features):
    '''
    im: image (np array)
    fb: filter bank (np array)
    n_features: number of feature vectors to extract (must be a square number)
    
    return feature vectors of an image at regularly spaced points on a
    grid over the image
    '''
    if int(n_features ** .5)**2 != n_features:
        raise Exception('n_features must be a square number')
    a,b,c = fb.shape
    feat_vecs = {}
    for pt in image_grid(im.shape,(a,b),n_features):
        feat_vecs[pt] = feature_vector(im,pt,fb)
    return feat_vecs    
    
    
if __name__ == "__main__":
    im = np.zeros((128,128))   
    fb = np.zeros((32,32,16))
    fs = image2features(im,fb,16)
    print fs
