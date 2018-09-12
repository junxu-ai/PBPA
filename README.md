# PBPA
A Python-based Block-trace Analyser. It comes with a book on "block trace analysis and storage system optimization". Besides, a Matlab version is also provided.

Author: Jun Xu (jun.xu@wdc.com)

# Background

IO event trace analysis is one of the most common techniques for storage system performance analysis. In particular, block-level trace analysis is essential for storage system optimization and design, as most underlying storage devices are in block-level, even the upper-level system to users are in object- or file-level. However, there are very few tools dedicated to this topic. This tool intends to fill this gap and provide a self-inclusive contents for block-level trace analysis techniques, as well as trace parsing and result reporting techniques, based on MATLAB platform.

# Installation [Python 3.5+]

sudo apt-get install python3-tk
pip install pandas python-pptx dill scipy matplotlib DateTime
cd PBPA
python setup.py install 

# structure

"Trace Analysis": the main functions to analysing the trace with given format. tens of properties are presented.
  [Input data]
  lists_cmd: Nx3 matrix; the first column is starting LBA, the second column is the request size, and the third column is access type (0/write, 1/read)
  lists_action: Nx2 matrix with the first column as arrival time, and the second coloumn as completion time
  [Output classes]
  Over ten classes for various basic and advanced metrics. see the commentrs inside functions

"Report generator": powerpoint report generator with using the lib python-pptx


# Howto

1. load the data file to get the trace matrices "lists_cmd" and "Blktrace Parser" (any traces with the pre-defined matrix format; see the book for the details)
2. run the corresponding trace analysis functions based your need; by default, all workload metrices will be analyzed
3. run report generator to create a powerpoint slide; 

batch_analysis.py & batch_generate_ppt.py provide a demo.
for more information, please refer to manual


# TD list
1. add more functions on locality analysis
2. add flexiablity in report generator
