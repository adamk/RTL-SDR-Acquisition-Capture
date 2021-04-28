# Author: Adam Kimbrough
# command line syntax: $ python rsx_survey.py <sat_type> <gain> <na>
#   <gain> RTL-SDR gain parameter, in dB. Must be from list output by rtl_test
#   <na>   Number of acquisitions to do.

# ^^^ Original file this code is based on

# Author: Adam Kimbrough
# Last edited: April 28, 2021
# Program to calculate frequency spacings for L-Band satellite downlinks
# accounting for filter roll-off.

import sys
import shutil
from datetime import datetime
import os
import math

# get input parameters
#freq = int((sys.argv)[1]) # string understandable by rtl_sdr
sat_type = (sys.argv)[1]  # Choose between Iridium or Inmarsat
gain = (sys.argv)[2]  # in dB, from list of valid gains
duration = (sys.argv)[3] # in seconds
na = int((sys.argv)[4]) #

import sys
import math
iridium_start = 1616.0e6 # end freq: 1626.5 MHz
inmarsat_start = 1525.0e6 # end freq: 1559.0 MHz
gpsl2_start = 1217.0e6 # end freq: 1237.0 MHz
gpsl3_start = 1375.0e6 # end freq: 1386.0 MHz
block1_start = 1200.0e6 # end freq: 1300.0 MHz
block2_start = 1300.0e6 # end freq: 1400.0 MHz
block3_start = 1400.0e6 # end freq: 1500.0 MHz
list_irdm = []
list_inmar = []
list_gpsl2 = []
list_gpsl3 = []
list_block1 = []
list_block2 = []
list_block3 = []
list_irdm_MHZ = []
i = 0
init = 0


if sat_type == 'iridium':
    start_freq = iridium_start + 1.024e6 - 0.3072e6
    list_irdm.append(math.trunc(start_freq))
    while i < 7:
        next_freq = start_freq + 0.7168e6 + 1.024e6 - 0.3072e6
        list_irdm.append(math.trunc(next_freq))
        start_freq = next_freq
        i = i + 1;
    for i in list_irdm:
        adj_freq = i / 1e6
        list_irdm_MHZ.append(adj_freq)
    print(list_irdm_MHZ)
    sat_freqs = list_irdm

elif sat_type == 'inmarsat':
    start_freq = inmarsat_start + 1.024e6 - 0.3072e6
    list_inmar.append(math.trunc(start_freq))
    while i < 23:
        next_freq = start_freq + 0.7168e6 + 1.024e6 - 0.31072e6
        list_inmar.append(math.trunc(next_freq))
        start_freq = next_freq
        i = i + 1;
    print(list_inmar)
    sat_freqs = list_inmar

elif sat_type == 'gpsl2':
    start_freq = gpsl2_start + 1.024e6 - 0.31072e6
    list_gpsl2.append(math.trunc(start_freq))
    while i < 13:
        next_freq = start_freq + 0.7168e6 + 1.024e6 - 0.31072e6
        list_gpsl2.append(math.trunc(next_freq))
        start_freq = next_freq
        i = i + 1;
    print(list_gpsl2)
    sat_freqs = list_gpsl2

elif sat_type == 'gpsl3':
    start_freq = gpsl3_start + 1.024e6 - 0.31072e6
    list_gpsl3.append(math.trunc(start_freq))
    while i < 7:
        next_freq = start_freq + 0.7168e6 + 1.024e6 - 0.31072e6
        list_gpsl3.append(math.trunc(next_freq))
        start_freq = next_freq
        i = i + 1;
    print(list_gpsl3)
    sat_freqs = list_gpsl3

elif sat_type == 'block1':
    start_freq = block1_start + 1.024e6 - 0.31072e6
    list_block1.append(math.trunc(start_freq))
    while i < 69:
        next_freq = start_freq + 0.7168e6 + 1.024e6 - 0.31072e6
        list_block1.append(math.trunc(next_freq))
        start_freq = next_freq
        i = i + 1;
    print(list_block1)
    sat_freqs = list_block1


elif sat_type == 'block2':
    start_freq = block2_start + 1.024e6 - 0.31072e6
    list_block1.append(math.trunc(start_freq))
    while i < 69:
        next_freq = start_freq + 0.7168e6 + 1.024e6 - 0.31072e6
        list_block2.append(math.trunc(next_freq))
        start_freq = next_freq
        i = i + 1;
    print(list_block2)
    sat_freqs = list_block2

elif sat_type == 'block3':
    start_freq = block3_start + 1.024e6 - 0.31072e6
    list_block1.append(math.trunc(start_freq))
    while i < 69:
        next_freq = start_freq + 0.7168e6 + 1.024e6 - 0.31072e6
        list_block3.append(math.trunc(next_freq))
        start_freq = next_freq
        i = i + 1;
    print(list_block3)
    sat_freqs = list_block3

else:
    print 'No valid satellite type selected.'

# these are the current RTL-SDR valid gain parameters, in dB:
gain_list = [ 0.9, 1.4, 2.7, 3.7, 7.7, 8.7, 12.5, 14.4, 15.7, 16.6, 19.7, 20.7, 22.9, 25.4, 28.0, 29.7, 32.8, 33.8, 36.4, 37.2, 38.6, 40.2, 42.1, 43.4, 43.9, 44.5, 48.0, 49.6 ]

hydrogen_freq = 1420.0e6
# error-checking gain value
if not (gain in str(gain_list)):
  sys.exit("gain setting '"+gain+"' valid not valid. Crashing out...")


# create a subdirectory for output
now = datetime.now()
if sat_type == 'iridium':
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_iridium_survey")
elif sat_type == 'inmarsat':
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_inmarsat_survey")
elif sat_type == 'gpsl2':
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_gpsl2_survey")
elif sat_type == 'gpsl3':
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_gpsl3_survey")
elif sat_type == 'block1':
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_1200-1300_survey")
elif sat_type == 'block2':
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_1300-1400_survey")
elif sat_type == 'block3':
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_1400-1500_survey")
else:
    dirname = now.strftime(str(duration) + "-sec-" + str(na) + "-na-" + "%y%m%d_%H%M%S_rsx_survey")

#print dirname
os.system('mkdir '+dirname)
f = open(dirname+'/log.dat','w')


# create a subdirectory for output
output_folder = 'survey_data'
output_folder_freq = "freq_domain"
output_folder_time = "time_domain"
os.system('mkdir ' + dirname + '/' + output_folder)
os.system('mkdir ' + dirname + '/' + output_folder + '/' + output_folder_freq)
os.system('mkdir ' + dirname + '/' + output_folder + '/' + output_folder_time)
na1 = na

for freq in sat_freqs:
    os.system('mkdir ' + dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq))
    os.system('mkdir ' + dirname + '/' + output_folder + '/' + output_folder_time + '/' + str(freq))
    acquisition_count = 1
    while (na1 > 0):
        f.write(str(freq)+' <-- center freq [Hz]\n')
        f.write(gain     +' <-- gain [dB] (string parameter to rtl_sdr)\n')
        f.write(duration  +' <-- # iterations (0=forever)\n')

         # construct filename for this capture
        now = datetime.now()
        rootname = str(freq)

        # capture data from RTL-SDR

        cmdln = 'rtl_sdr -f '+ str(freq) +' -s 2048000 -g '+ str(gain) +' -n '+ str(int(duration)*2048000+2048) + ' ' +dirname+'/'+rootname+'.out'
        print cmdln
        f.write(cmdln+'\n')
        os.system(cmdln)
        na1 = na1 - 1
        acquisition_count += 1
    na1 = na
f.close()

cont_analysis = input("Press (1) to analyze or (2) to abort: ")

if (cont_analysis == 1):
    f = open(dirname + '/' + output_folder+'/survey.dat','w')
    na2 = na
    for freq in sat_freqs:
        acquisition_count = 1
        while (na2 > 0):
          ## analyze this block of data
            cmdln = './rsx_analyze ' + dirname + '/' + str(freq) +'.out' + ' 2048'
            cmdout = os.popen(cmdln).read() # this way, stdout is captured to the variable "cmdout"
            print cmdout

          # strip out min and max I values
            line = (cmdout.splitlines())[5] # line reading something like this: "-12 +3.714e-01  +13 <-- I min, mean, max"
            imin = int( (line.split())[0] ) # in case of above example, gives -12 (min I value)
            imax = int( (line.split())[2] ) # in case of above example, gives +13 (max I value)

          # strip out min and max Q values
            line = (cmdout.splitlines())[6] # line reading something like this: " -13 +3.678e-01  +14 <-- Q min, mean, max"
            qmin = int( (line.split())[0] ) # in case of above example, gives -13 (min Q value)
            qmax = int( (line.split())[2] ) # in case of above example, gives +14 (max Q value)

          # strip out rms
            line = (cmdout.splitlines())[8] # line reading something like this: "+1.520e+02 <-- RMS sample magnitude"
            rms = (line.split())[0]         # in case of above example, gives '+1.520e+02'

            iqave = (abs(imin)+abs(imax)+abs(qmin)+abs(qmax))/4.0 # average of extreme I and Q values
            print str(imin)+' '+str(imax)+' '+str(qmin)+' '+str(qmax)+' mean: '+str(iqave)
            f.write(str(gain)+' '+str(iqave)+' '+rms+' '+str(20.0*math.log10(float(rms)))+'\n')

          # rename rsx_analyze_f.dat so that it is not overwritten and can be recognized later
            cmdln = 'mv rsx_analyze_f.dat ' + dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '/' + "acquisition" + str(acquisition_count).zfill(4)+'.dat'
            os.system(cmdln)

            cmdln = 'mv rsx_analyze_t.dat ' + dirname + '/' + output_folder + '/' + output_folder_time + '/' + str(freq) + '/' + "acquisition" + str(acquisition_count).zfill(4)+'.dat'
            os.system(cmdln)
            na2 = na2 - 1
            acquisition_count += 1
        na2 = na

    f.close()

    # Combine all .out files for each frequency and remove folders
    print("Combining .out acquisitions...")
    cmdln = 'zip ' + dirname + '/' + sat_type + '.zip ' + dirname + '/*.out'
    os.system(cmdln)

    for freq in sat_freqs:
        cmdln = 'rm ' + dirname + '/' + str(freq) + '.out'
        os.system(cmdln)

    # Remove filter roll-off on each .dat file
    na3 = na
    print("Removing filter roll-offs...")
    for freq in sat_freqs:
        for file in os.listdir(dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq)):
            acquisition_count = 1
            while(na3 > 0):
                output_file = dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '/' + "acquisition" + str(acquisition_count).zfill(4)+'.dat'
                dat_file = open(output_file, "r")
                lines = dat_file.readlines()
                dat_file.close()
                new_dat_file = open(output_file, "w+")
                for line in lines:
                    freq_line = float( (line.split())[0] )
                    if (freq_line >= -0.35010) & (freq_line <= 0.35010):
                        new_dat_file.write(line)
                new_dat_file.close()
                na3 = na3 - 1
                acquisition_count += 1
            na3 = na

    # Average power of all collected acquisitions per duration at each frequency (works for even numbers only)
    na4 = na # Set number of acquistions = # of files present
    print("Averaging all powers...")
    for freq in sat_freqs:
        data1 = []
        data2 = []
        data3 = []
        acquisition_count = 1
        acquisition_count2 = acquisition_count + 1
        file1 = dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '/' + "acquisition" + str(acquisition_count).zfill(4)+'.dat'
        while((na4/2) > 0):
            file1 = dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '/' + "acquisition" + str(acquisition_count).zfill(4)+'.dat'
            file2 = dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '/' + "acquisition" + str(acquisition_count2).zfill(4)+'.dat'

            # Put every value from third column of file1 into list
            f1 = open(file1, "r")
            for line in f1.readlines():
                power = float( (line.split())[1] ) # Value in 2nd column of file
                data1.append(power)

            f1.close()
            # Put every value from third column of file2 into list
            f2 = open(file2, "r")
            for line in f2.readlines():
                power = float( (line.split())[1] ) # Entry in 2nd column of file
                data2.append(power)
            f2.close()

            # Add the powers, divide by 2, convert to dB
            data3 = [10*math.log10((x + y)/2) for x, y in zip(data1, data2)]

            with open(file2, "r") as f:
                lines = f.readlines()
                lines = [line.split() for line in lines]

            count3 = 0
            for line in lines:
                # Replace column #3 (aka index 2) with average power in dB
                line[2] = str(data3[count3])
                count3 += 1

            with open(file2, "w") as f:
                f.write("\n".join(" ".join(line) for line in lines))

            na4 = na4 - 1
            acquisition_count += 1
            acquisition_count2 += 1
        na4 = na
        # For a single acuisition
        if na > 1:
            # Rename final averaged .dat to _avg.dat
            cmdln = 'mv ' + file2 + ' ' + dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '_avg.dat'
            os.system(cmdln)
        # For multiple acquisitions
        else:
            # Rename final .dat
            cmdln = 'mv ' + file1 + ' ' + dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '.dat'
            os.system(cmdln)
        # Remove all the frequency folders
        shutil.rmtree(dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq), ignore_errors=True)

elif (cont_analysis == 2):
    print "Data acquisition finished."

else:
    "Invalid input"
