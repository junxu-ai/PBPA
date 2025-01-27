import os
from numpy import *
from matplotlib.pylab import *
# from statistics import mode
from scipy.stats import *
from scipy import *
import dill  
import pickle
import inspect
from scipy.io import loadmat
 
from PBPA.sub_basic_info import sub_basic_info
from PBPA.sub_queue_depth import sub_queue_depth
from PBPA.sub_busy_time import sub_busy_time
from PBPA.sub_iops import sub_iops
from PBPA.sub_size_dist import sub_size_dist
from PBPA.sub_lba_dist import sub_lba_dist
from PBPA.sub_sequence_analysis import sub_sequence_analysis
from PBPA.sub_stack_wow import sub_stack_wow
from PBPA.sub_stack_row import sub_stack_row
from PBPA.sub_freq_wow import sub_freq_wow
from PBPA.sub_seek_dist import sub_seek_dist
from PBPA.sub_time_wow import sub_time_wow
from PBPA.sub_idle_queue import sub_idle_queue
from PBPA.report_plugins import options_class


#lists_action=lists_action[:,0:2]

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
options.export_report = 0

if 'name' in locals():
    options.report_name = name+'_raw.ppt'
else:
    options.report_name = 'trace_analysis_raw.ppt'

options.export_report = 1
options.plot_fontsize = 10
options.time_interval = 5
options.plot_figure = 1
#options.offset_time=lists_action(1,1); # some trace is not started from zone. in this case. need to find the starting time of first event.
options.offset_time = 0

idx=argsort(lists_action[:,0])

lists_cmd=lists_cmd[ix_(list(idx),[0,1,2])]
lists_cmd=lists_cmd.astype(int64)
lists_action=lists_action[ix_(list(idx),[0,1])]

basic_info=sub_basic_info(lists_action,lists_cmd,options)
### call individual sub-functions
#1 average queue depth for completion and arrival
options.time_interval=5
queue_record=sub_queue_depth(lists_action,lists_cmd,options)

#2 calculate the device busy time;
time_record=sub_busy_time(lists_action,options)

#3 average IOPS/throughput/request
options.time_interval = 1
average_record=sub_iops(lists_action,lists_cmd,options)
options.time_interval = 6
average_record=sub_iops(lists_action,lists_cmd,options)

#4 calcuate the size distribution
req_size_record=sub_size_dist(lists_action,lists_cmd,options)

#5 calcuate the LBA/size distribution
options.lba_size_set = 50
lba_stat_array=sub_lba_dist(lists_action,lists_cmd,options)


#6 sequential analysis (stream/commands/size/queue length)
options.near_sequence = 0
options.S2_threshold = 32
options.S2_threshold2 = 64
options.max_stream_length = 1024
options.seq_size_threshold = 1024

sequence_stat0=sub_sequence_analysis(lists_action,lists_cmd,options)

options.near_sequence = 1
options.S2_threshold = (32)
options.S2_threshold2 = (64)
options.max_stream_length = (1024)
options.seq_size_threshold = (1024)

sequence_stat1=sub_sequence_analysis(lists_action,lists_cmd,options)

#7
## sub_sequence_queue(lists_cmd,options)

#8 stack distance analysis - WOW
# options.spec_stack=[10,20,30];  # for very large dataset ; otherwise specify some small numbers
stack_wow_record=sub_stack_wow(lists_cmd,options)

#9 stack distance analysis - ROW
stack_row_record=sub_stack_row(lists_cmd,options)

#10 frequented write update ratio - WOW
options.access_type = (0)
freq_wow_record=sub_freq_wow(lists_cmd,options)

#11 timed/ordered update ratio - WOW
options.access_type = (0)
time_wow_record=sub_time_wow(lists_cmd,options)

#12 seek distance calcuation
seek_dist_record=sub_seek_dist(lists_cmd,options)

#13 queue length and idle time
idle_queue_record=sub_idle_queue(lists_action,options)


## save all variables into file for future use
filename= 'result.pkl'
f=open( filename, "wb" ) 
pickle.dump([lists_cmd, lists_action, options],f)
for var_i in dir():
    if isinstance(var_i,type(var_i)):
        pickle.dump(var_i,f)
f.close()

mid_dict = {'basic_info':basic_info,
            'seek_dist_record':seek_dist_record,
            'time_wow_record':time_wow_record,
            'idle_queue_record':idle_queue_record,
            'lists_action':lists_action,
            'req_size_record':req_size_record,
            'freq_wow_record':freq_wow_record,
            'stack_wow_record':stack_wow_record
}

analysis_result_file = _get_module_path('analysis.pkl')

with open(analysis_result_file, 'wb') as data_f:
    pickle.dump(mid_dict, data_f)

#
#dill.dump_session(filename)