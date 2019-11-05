### Objective:
Perform a read-resample-roll-std pipeline using less than 1MB over a large amount of (time series) data.

# Solution use:
main.py [DATA_FOLDER] [True|False]  
arg0: Absolute path of folder containted (uncompressed) plain text files with sorted time series data.   
arg1: (default: False) Delete temporal files created during execution in /tmp folder.  

* Time series line required format:  
time in epoch millis,decimal number


