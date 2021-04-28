import sys
import shutil
from datetime import datetime
import os
import math

sat_type = (sys.argv)[1] #
na = int((sys.argv)[2]) #
dirname = str((sys.argv)[3]) #
gain = 33.8
sat_freqs = []
iridium_freqs = [1616716800, 1618150400, 1619584000, 1621017600, 1622451200, 1623884800, 1625318400, 1626752000]
inmarsat_freqs = [1525716800, 1527146880, 1528576960, 1530007040, 1531437120, 1532867200, 1534297280, 1535727360, 1537157440, 1538587520, 1540017600, 1541447680, 1542877760, 1544307840, 1545737920, 1547168000, 1548598080, 1550028160, 1551458240, 1552888320, 1554318400, 1555748480, 1557178560, 1558608640]
gpsl3_freqs = [1375713280, 1377143360, 1378573440, 1380003520, 1381433600, 1382863680, 1384293760, 1385723840]
gpsl2_freqs = [1219143360, 1220573440, 1222003520, 1223433600, 1224863680, 1226293760, 1227723840, 1229153920, 1230584000, 1232014080, 1233444160, 1234874240, 1236304320]
block1_freqs = [1200713280, 1202143360, 1203573440, 1205003520, 1206433600, 1207863680, 1209293760, 1210723840, 1212153920, 1213584000, 1215014080, 1216444160, 1217874240, 1219304320, 1220734400, 1222164480, 1223594560, 1225024640, 1226454720, 1227884800, 1229314880, 1230744960, 1232175040, 1233605120, 1235035200, 1236465280, 1237895360, 1239325440, 1240755520, 1242185600, 1243615680, 1245045760, 1246475840, 1247905920, 1249336000, 1250766080, 1252196160, 1253626240, 1255056320, 1256486400, 1257916480, 1259346560, 1260776640, 1262206720, 1263636800, 1265066880, 1266496960, 1267927040, 1269357120, 1270787200, 1272217280, 1273647360, 1275077440, 1276507520, 1277937600, 1279367680, 1280797760, 1282227840, 1283657920, 1285088000, 1286518080, 1287948160, 1289378240, 1290808320, 1292238400, 1293668480, 1295098560, 1296528640, 1297958720, 1299388800]
block2_freqs = [1302143360, 1303573440, 1305003520, 1306433600, 1307863680, 1309293760, 1310723840, 1312153920, 1313584000, 1315014080, 1316444160, 1317874240, 1319304320, 1320734400, 1322164480, 1323594560, 1325024640, 1326454720, 1327884800, 1329314880, 1330744960, 1332175040, 1333605120, 1335035200, 1336465280, 1337895360, 1339325440, 1340755520, 1342185600, 1343615680, 1345045760, 1346475840, 1347905920, 1349336000, 1350766080, 1352196160, 1353626240, 1355056320, 1356486400, 1357916480, 1359346560, 1360776640, 1362206720, 1363636800, 1365066880, 1366496960, 1367927040, 1369357120, 1370787200, 1372217280, 1373647360, 1375077440, 1376507520, 1377937600, 1379367680, 1380797760, 1382227840, 1383657920, 1385088000, 1386518080, 1387948160, 1389378240, 1390808320, 1392238400, 1393668480, 1395098560, 1396528640, 1397958720, 1399388800]
block3_freqs = [1402143360, 1403573440, 1405003520, 1406433600, 1407863680, 1409293760, 1410723840, 1412153920, 1413584000, 1415014080, 1416444160, 1417874240, 1419304320, 1420734400, 1422164480, 1423594560, 1425024640, 1426454720, 1427884800, 1429314880, 1430744960, 1432175040, 1433605120, 1435035200, 1436465280, 1437895360, 1439325440, 1440755520, 1442185600, 1443615680, 1445045760, 1446475840, 1447905920, 1449336000, 1450766080, 1452196160, 1453626240, 1455056320, 1456486400, 1457916480, 1459346560, 1460776640, 1462206720, 1463636800, 1465066880, 1466496960, 1467927040, 1469357120, 1470787200, 1472217280, 1473647360, 1475077440, 1476507520, 1477937600, 1479367680, 1480797760, 1482227840, 1483657920, 1485088000, 1486518080, 1487948160, 1489378240, 1490808320, 1492238400, 1493668480, 1495098560, 1496528640, 1497958720, 1499388800]

if sat_type == 'iridium':
    for i in iridium_freqs:
        sat_freqs.append(i)
    sat_freqs = iridium_freqs
elif sat_type == 'inmarsat':
    for i in inmarsat_freqs:
        sat_freqs.append(i)
elif sat_type == 'gpsl2':
    for i in gpsl2_freqs:
        sat_freqs.append(i)
elif sat_type == 'gpsl3':
    for i in gpsl3_freqs:
        sat_freqs.append(i)
elif sat_type == 'block1':
    for i in block1_freqs:
        sat_freqs.append(i)
elif sat_type == 'block2':
    for i in block2_freqs:
        sat_freqs.append(i)
elif sat_type == 'block3':
    for i in block3_freqs:
        sat_freqs.append(i)
else:
    print "Invalid sat type"

output_folder = 'survey_data'
output_folder_freq = "freq_domain"
output_folder_time = "time_domain"

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
if (na > 1):
    print("Averaging all powers...")
else:
    print("Relocating .dat files...")
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
    # For multiple acquisitions:
    if na > 1:
        # Rename final averaged .dat to _avg.dat
        cmdln = 'mv ' + file2 + ' ' + dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '_avg.dat'
        os.system(cmdln)
    # For a single acquisition at each center freq:
    else:
        # Rename final .dat
        cmdln = 'mv ' + file1 + ' ' + dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq) + '.dat'
        os.system(cmdln)
    # Remove all the frequency folders
    shutil.rmtree(dirname + '/' + output_folder + '/' + output_folder_freq + '/' + str(freq), ignore_errors=True)
