# -*- coding: utf-8 -*-
"""
Created on Mon Feb 20 14:45:04 2012
Script for generating adjacency matrices using the brainwaver package for R.
The input is a timeseries file.
@author: - tr332@medschl.cam.ac.uk
"""

import csv,os,glob,shutil,operator
import numpy as np
import rpy2
from rpy2.robjects.packages import importr
import matplotlib as mp
from matplotlib import pyplot
import rpy2.robjects.numpy2ri
from nitime import viz
from pylab import *
from operator import itemgetter

rpy2.robjects.numpy2ri.activate()
brainwaver = importr("brainwaver")
base = importr("base")
utils = importr("utils")

cdict = {'red': ((0.0, 1.0, 1.0),
                 (0.5, 1.0, 1.0),
                 (1.0, 1.0, 1.0)),
         'green': ((0.0, 1.0, 1.0),
                   (0.7, 0.5, 0.5),
                   (1.0, 0.0, 0.0)),
         'blue': ((0.0, 1.0, 1.0),
                  (0.5, 0.2, 0.2),
                  (1.0, 0.0, 0.0))}
my_cmap = mp.colors.LinearSegmentedColormap('my_colormap',cdict,256)

class individual:
    def __init__ (self, filename, diag=None):
        if diag:
            self.diag = diag
        else:
            self.diag = None
                        
        self.dir = os.path.split(filename)[0]
        
        self.timeseries = filename
	
    def waveletDecomp(self, headerBool=False, Rtimeseries=None, removeNAlines=True):
        """
        Calculates and draw adjacency matrices
        """
        if not Rtimeseries:
            self.Rtimeseries = self.timeseries
        else:
            self.Rtimeseries = Rtimeseries
                
        # get dimensions        
        f = open(self.Rtimeseries)
        lines = f.readlines()
        lines = [v for v in lines]
        rows = len(lines)
        cols = len(lines[0].split())
        print ' '.join([str(rows),str(cols)])
        f.close()
        
        self.fileNameBase= "d_"+str(cols)
        
        ts = np.genfromtxt(self.timeseries, missing_values="NA", filling_values=999.)

        missing = np.where(ts[1,:] == 999.)
        print "Missing columns: "+' '.join([str(v) for v in missing[0]])
        
        if removeNAlines:
            self.adjmats = brainwaver.const_cor_list(base.as_matrix(ts),export_data=False)  # construct correlation matrices using wavelet decomposition
            
            for n,mat in enumerate(self.adjmats):
                mat = np.array(mat)
                
                for m in missing[0]:
                    mat[m,:] = np.nan
                    mat[:,m] = np.nan
                    
                if n < 4:
                    outfile='_'.join(["wave_cor_mat_level", str(n+1) + self.fileNameBase + '.txt'])
                elif n < 8:
                    outfile='_'.join(["wave_cor_lower_mat_level", str(n-3) + self.fileNameBase + '.txt'])
                else:
                    outfile='_'.join(["wave_cor_upper_mat_level", str(n-7) + self.fileNameBase + '.txt'])
                
                print "Saving "+outfile
                np.savetxt(outfile, mat, fmt='%0.6f')
	             


        
        else:
            self.adjmats = brainwaver.const_cor_list(base.as_matrix(ts),export_data=True)  # construct correlation matrices using wavelet decomposition

            for i in range(1,5):
                for wavedecomp in glob.glob(os.path.join(self.dir,'wave_cor_*'+str(i)+'.txt')):
                    end = self.fileNameBase+'.txt'

                    newfile = os.path.join(self.dir,wavedecomp[:-4]+end)
                    try:
                        shutil.move(wavedecomp,newfile)
                    except:
                        shutil.move(newfile,newfile+".old")
                        shutil.move(wavedecomp,newfile)
                        print "moved "+newfile+" to "+newfile+".old"
    

