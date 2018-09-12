# -*- coding: utf-8 -*-
"""
load the data for analysis and reporting
"""
import os
import scipy
import numpy as np
from scipy.io import loadmat
from PBPA.report_plugins import options_class
    
filename='.\\Data\\RAID.mat'
_get_module_path = lambda path: os.path.normpath(os.path.join(os.getcwd(),os.path.dirname(__file__), path))
DEFAULT_MAT = _get_module_path(filename)

mat_dict={}
mat_dict.update(loadmat(DEFAULT_MAT))
lists_action=mat_dict['lists_action']  
if lists_action.shape[1]==7:
    lists_action=lists_action[:,5:7]
lists_cmd=mat_dict['lists_cmd']

options=options_class()
options.access_type=0
traces=lists_cmd

## generate trace analysis result
#os.system("python batch_analysis.py")
#
## create powerpoint report
#os.system("python batch_generate_ppt.py")
