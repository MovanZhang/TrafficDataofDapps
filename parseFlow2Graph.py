'''
@author: MovanZhang
@created： 2019.12.06
@version: Python3.7
@description: 将神经网络进行图结构编码
'''
# encoding: utf8
import csv
dappName = {}

# 抽取下行流量的数据包长度和标志位文本
def extractDownLenandFlagT(readfileName, writefileName):
    readfile = open(readfileName, 'r')
    writefile = open(writefileName, 'w')
    readCSV = csv.reader(readfile)
    writeCSV = csv.writer(writefile)
    # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
    ifFirstAppData = 0
    # 记录流长度
    for row in readCSV:
        if len(row) == 0:
            #writefile.write('\n')
            writeCSV.writerow([])
            ifFirstAppData = 0
        else:
            if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                if row[4].find('TLS') != -1 and ifFirstAppData == 0:
                    #writefile.write(row[5] + ',' + row[6] + '\n')
                    writeCSV.writerow([row[5], row[6]])
                    if row[6].find('Application Data') != -1:
                        ifFirstAppData = 1
    readfile.close()
    writefile.close()


# 抽取下行流量的数据包长度和标志位图结构
def extractDownLenandFlagG(readfileName, writefileName):
    # 获取dapp名称
    dappNameTem = readfileName.split('/')[2].split('-')[0]
    print(dappNameTem)
    if not dappNameTem in dappName:
        mapped = len(dappName)
        dappName[dappNameTem] = mapped
    print(dappName)
    readfile = open(readfileName, 'r')
    readCSV = csv.reader(readfile)
    writeTxt = open(writefileName, 'w')
    # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
    ifFirstAppData = 0
    flowCount = 0  # 流数量
    flowLen = []  # 记录流长度，流里边的数据包
    for row in readCSV:
        if len(row) == 0:
            ifFirstAppData = 0
            #print(flowLen)
            writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
            for i in range(len(flowLen)):
                if i == 0:
                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                elif i == len(flowLen)-1:
                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen)-1-1) + '\n')
                else:
                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i-1) + ' ' + str(i+1) + '\n')
            flowLen = []
            flowCount += 1
        else:
            if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                if row[4].find('TLS') != -1 and ifFirstAppData == 0:
                    #writefile.write(row[5] + ',' + row[6] + '\n')
                    flowLen.append(row[5])
                    if row[6].find('Application Data') != -1:
                        ifFirstAppData = 1
    readfile.close()
    writeTxt.close()
    #最后将流的数量写入第一行
    with open(writefileName, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(flowCount) + '\n' + content)


# 抽取一个文件夹所有流量数据的下行流量的数据包长度和标志位图结构
def extractDownLenandFlagGFlist(readfilepath, writefileName):
    writeTxt = open(writefileName, 'w')
    flowCount = 0  # 流数量
    import os
    fileList = os.listdir(readfilepath)
    for readfileName in fileList:
        # 获取dapp名称
        dappNameTem = readfileName.split('-')[0]
        print(dappNameTem)
        if not dappNameTem in dappName:
            mapped = len(dappName)
            dappName[dappNameTem] = mapped
        print(dappName)
        try:
            readfile = open(readfilepath+readfileName, 'r', encoding='UTF-8')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            ifFirstAppData = 0
            flowLen = []  # 记录流长度，流里边的数据包
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    ifFirstAppData = 0
                    #print(flowLen)
                    if (len(flowLen) > 1 and len(flowLen) < 6):
                        writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                        for i in range(len(flowLen)):
                            if i == 0:
                                writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                            elif i == len(flowLen)-1:
                                writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen)-1-1) + '\n')
                            else:
                                writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i-1) + ' ' + str(i+1) + '\n')
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1 and ifFirstAppData == 0:
                            #writefile.write(row[5] + ',' + row[6] + '\n')
                            flowLen.append(row[5])
                            if row[6].find('Application Data') != -1:
                                ifFirstAppData = 1
            readfile.close()
        except:
            readfile = open(readfilepath + readfileName, 'r')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            ifFirstAppData = 0
            flowLen = []  # 记录流长度，流里边的数据包
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    ifFirstAppData = 0
                    # print(flowLen)
                    if (len(flowLen) > 1 and len(flowLen) < 6):
                        writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                        for i in range(len(flowLen)):
                            if i == 0:
                                writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                            elif i == len(flowLen) - 1:
                                writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                            else:
                                writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1 and ifFirstAppData == 0:
                            # writefile.write(row[5] + ',' + row[6] + '\n')
                            flowLen.append(row[5])
                            if row[6].find('Application Data') != -1:
                                ifFirstAppData = 1
            readfile.close()
    writeTxt.close()
    #最后将流的数量写入第一行
    with open(writefileName, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(flowCount) + '\n' + content)


# 抽取一个文件夹所有流量数据的下行流量的数据包长度和标志位图结构
def extractDownLenandFlagNF(readfilepath, writefileName):
    packetUse = 18
    writeTxt = open(writefileName, 'w')
    flowCount = 0  # 流数量
    import os
    fileList = os.listdir(readfilepath)
    for readfileName in fileList:
        # 获取dapp名称
        dappNameTem = readfileName.split('-')[0]
        print(dappNameTem)
        if not dappNameTem in dappName:
            mapped = len(dappName)
            dappName[dappNameTem] = mapped
        print(dappName)
        # 将dappName写入文件
        import json
        json_str = json.dumps(dappName)
        with open('name_label.json', 'w') as json_file:
            json_file.write(json_str)

        try:
            readfile = open(readfilepath+readfileName, 'r', encoding='UTF-8')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 1:
                        if len(flowLen) <= packetUse:
                            writeTxt.write(
                                str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == len(flowLen)-1:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen)-1-1) + '\n')
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i-1) + ' ' + str(i+1) + '\n')
                        else:
                            writeTxt.write(
                                str(packetUse) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(packetUse):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == packetUse-1:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse-1-1) + '\n')
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i-1) + ' ' + str(i+1) + '\n')
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1 :
                            flowLen.append(row[5])
            readfile.close()
        except:
            readfile = open(readfilepath + readfileName, 'r')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 1:
                        if len(flowLen) <= packetUse:
                            writeTxt.write(
                                str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == len(flowLen) - 1:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                else:
                                    writeTxt.write(
                                        flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        else:
                            writeTxt.write(str(packetUse) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(packetUse):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == packetUse-1:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse - 1 - 1) + '\n')
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1:
                            # writefile.write(row[5] + ',' + row[6] + '\n')
                            flowLen.append(row[5])
            readfile.close()
    writeTxt.close()
    #最后将流的数量写入第一行
    with open(writefileName, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(flowCount) + '\n' + content)


# 抽取一个文件夹所有流量数据的双向流量的数据包长度和标志位图结构-图结构风筝头-风筝头圆形（环状）
def extractDownLenandFlagBi(readfilepath, writefileName):
    packetUse = 20
    writeTxt = open(writefileName, 'w')
    flowCount = 0  # 流数量
    import os
    fileList = os.listdir(readfilepath)
    for readfileName in fileList:
        # 获取dapp名称
        dappNameTem = readfileName.split('-')[0]
        print(dappNameTem)
        if not dappNameTem in dappName:
            mapped = len(dappName)
            dappName[dappNameTem] = mapped
        print(dappName)
        # 将dappName写入文件
        import json
        json_str = json.dumps(dappName)
        with open('name_label.json', 'w') as json_file:
            json_file.write(json_str)

        try:
            readfile = open(readfilepath+readfileName, 'r', encoding='UTF-8')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            firstAppIndex = None # 第一个下行ApplicationData数据包位置
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 5:
                        #print(flowLen)
                        if len(flowLen) <= packetUse:
                            writeTxt.write(
                                str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == len(flowLen)-1:
                                    if firstAppIndex != None and i == firstAppIndex:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(len(flowLen) - 1 - 1) + ' 0\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                elif firstAppIndex != None and i == firstAppIndex:
                                    writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' 0'+'\n')
                                    #print()
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i-1) + ' ' + str(i+1) + '\n')
                        else:
                            writeTxt.write(
                                str(packetUse) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(packetUse):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == packetUse-1:
                                    if firstAppIndex != None and i == firstAppIndex:
                                        writeTxt.write(
                                            flowLen[i] + ' ' + '2' + ' ' + str(packetUse - 1 - 1) + ' 0\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse - 1 - 1) + '\n')
                                    #writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse-1-1) + '\n')
                                elif firstAppIndex != None and i == firstAppIndex:
                                    writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' 0'+'\n')
                                    #print()
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i-1) + ' ' + str(i+1) + '\n')
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1:
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex==None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if row[4].find('TLS') != -1:
                            #print(row[5])
                            flowLen.append(str(int(row[5]) * -1))
            readfile.close()
        except:
            readfile = open(readfilepath + readfileName, 'r')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            firstAppIndex = None
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 5:
                        if len(flowLen) <= packetUse:
                            writeTxt.write(
                                str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == len(flowLen) - 1:
                                    if firstAppIndex != None and i == firstAppIndex:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(len(flowLen) - 1 - 1) + ' 0\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                elif firstAppIndex != None and i == firstAppIndex:
                                    writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' 0'+'\n')
                                    #print()
                                else:
                                    writeTxt.write(
                                        flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        else:
                            writeTxt.write(str(packetUse) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(packetUse):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == packetUse-1:
                                    if firstAppIndex != None and i == firstAppIndex:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(packetUse - 1 - 1) + ' 0\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse - 1 - 1) + '\n')
                                elif firstAppIndex != None and i == firstAppIndex:
                                    writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' 0'+'\n')
                                    #print()
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1:
                            # writefile.write(row[5] + ',' + row[6] + '\n')
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex==None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if row[4].find('TLS') != -1:
                            flowLen.append(str(int(row[5]) * -1))
            readfile.close()
    writeTxt.close()
    #最后将流的数量写入第一行
    with open(writefileName, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(flowCount) + '\n' + content)


# 抽取一个文件夹所有流量数据的双向流量的数据包长度和标志位图结构-图结构风筝头-风筝头圆形（环里边有网）
def extractDownLenandFlagBiDuo(readfilepath, writefileName):
    packetUse = 20
    writeTxt = open(writefileName, 'w')
    flowCount = 0  # 流数量
    import os
    fileList = os.listdir(readfilepath)
    for readfileName in fileList:
        print(readfileName)
        # 获取dapp名称
        dappNameTem = readfileName.split('-')[0]
        print(dappNameTem)
        if not dappNameTem in dappName:
            mapped = len(dappName)
            dappName[dappNameTem] = mapped
        print(dappName)
        # 将dappName写入文件
        import json
        json_str = json.dumps(dappName)
        with open('name_label.json', 'w') as json_file:
            json_file.write(json_str)

        try:
            readfile = open(readfilepath+readfileName, 'r', encoding='UTF-8')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            firstAppIndex = None # 第一个下行ApplicationData数据包位置
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 5:  # 四个数据包以上才作为一条流
                        #print(flowLen)
                        if len(flowLen) <= packetUse:  # 实际数据包数量不大于用到的数据包数量
                            writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if firstAppIndex != None and firstAppIndex >= 1 and firstAppIndex <= packetUse-1:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + '1 ' + str(firstAppIndex) + '\n')
                                    elif i < firstAppIndex:
                                        writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' ' + str(firstAppIndex) + '\n')
                                    elif i == firstAppIndex:
                                        if i == len(flowLen) - 1:
                                            writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' 0' + '\n')
                                        else:
                                            writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' 0' + '\n')
                                    elif i == len(flowLen) - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                                else:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                    elif i == len(flowLen) - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        else:
                            writeTxt.write(
                                str(packetUse) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(packetUse):
                                if firstAppIndex != None and firstAppIndex <= packetUse-1:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '2 1 ' + str(firstAppIndex) + '\n')
                                    elif i < firstAppIndex:
                                        writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' ' + str(firstAppIndex) + '\n')
                                    elif i == firstAppIndex:
                                        if i == packetUse - 1:
                                            writeTxt.write(flowLen[i] + ' ' + '2 ' + str(i - 1) + ' 0' + '\n')
                                        else:
                                            writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' 0' + '\n')
                                    elif i == packetUse - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                                else:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                    elif i == packetUse - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        firstAppIndex = None
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1:
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex==None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if row[4].find('TLS') != -1:
                            #print(row[5])
                            flowLen.append(str(int(row[5]) * -1))
            readfile.close()
        except:
            readfile = open(readfilepath + readfileName, 'r')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            firstAppIndex = None
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 5:  # 四个数据包以上才作为一条流
                        if len(flowLen) <= packetUse:
                            writeTxt.write(
                                str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if firstAppIndex != None and firstAppIndex >= 1 and firstAppIndex <= packetUse-1:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + '1 ' + str(firstAppIndex) + '\n')
                                    elif i < firstAppIndex:
                                        writeTxt.write(
                                            flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' ' + str(
                                                firstAppIndex) + '\n')
                                    elif i == firstAppIndex:
                                        if i == len(flowLen) - 1:
                                            writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' 0' + '\n')
                                        else:
                                            writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(
                                                i + 1) + ' 0' + '\n')
                                    elif i == len(flowLen) - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(
                                            flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                                else:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                    elif i == len(flowLen) - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(
                                            flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        else:
                            writeTxt.write(
                                str(packetUse) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(packetUse):
                                if firstAppIndex != None and firstAppIndex <= packetUse-1:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '2 1 ' + str(firstAppIndex) + '\n')
                                    elif i < firstAppIndex:
                                        writeTxt.write(
                                            flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' ' + str(
                                                firstAppIndex) + '\n')
                                    elif i == firstAppIndex:
                                        if i == packetUse - 1:
                                            writeTxt.write(flowLen[i] + ' ' + '2 ' + str(i - 1) + ' 0' + '\n')
                                        else:
                                            writeTxt.write(flowLen[i] + ' ' + '3' + ' ' + str(i - 1) + ' ' + str(i + 1) + ' 0' + '\n')
                                    elif i == packetUse - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                                else:
                                    if i == 0:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                    elif i == packetUse - 1:
                                        writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(packetUse - 1 - 1) + '\n')
                                    else:
                                        writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                        firstAppIndex = None
                        flowLen = []
                        flowCount += 1
                    else:
                        flowLen = []
                else:
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1:
                            # writefile.write(row[5] + ',' + row[6] + '\n')
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex==None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if row[4].find('TLS') != -1:
                            flowLen.append(str(int(row[5]) * -1))
            readfile.close()
    writeTxt.close()
    #最后将流的数量写入第一行
    with open(writefileName, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(flowCount) + '\n' + content)


# 抽取一个文件夹所有流量数据的双向流量的数据包长度图结构-图结构梯形风筝结构
def extractDownLenandFlagBiTixing(readfilepath, writefileName):
    packetUse = 25
    writeTxt = open(writefileName, 'w')
    flowCount = 0  # 流数量
    import os
    fileList = os.listdir(readfilepath)
    for readfileName in fileList:
        print(readfileName)
        # 获取dapp名称
        dappNameTem = readfileName.split('-')[0]
        print(dappNameTem)
        if not dappNameTem in dappName:
            mapped = len(dappName)
            dappName[dappNameTem] = mapped
        print(dappName)
        # 将dappName写入文件
        import json
        json_str = json.dumps(dappName)
        with open('name_label.json', 'w') as json_file:
            json_file.write(json_str)

        try:
            readfile = open(readfilepath+readfileName, 'r', encoding='UTF-8')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            firstAppIndex = None # 第一个下行ApplicationData数据包位置
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 5 :  # 四个数据包以上才作为一条流
                        if len(flowLen) > packetUse:
                            flowLen = flowLen[:packetUse]
                        #print(flowLen)
                        graphItems = genTixingGaphitems(flowLen)
                        count = 0
                        if len(graphItems) == 1:  # 一条流中只有单向流量
                            #print(flowLen)
                            print('Hello')
                            '''
                            writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == len(flowLen) - 1:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                            flowCount += 1
                            '''
                        else:
                            writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for level in range(len(graphItems)):
                                if level == 0: # 第一层
                                    if len(graphItems[level]) == 1:
                                        if len(graphItems[level+1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 1 ' + str(count + 1) + '\n')
                                            count += 1
                                        else:
                                            writeTxt.write(graphItems[level][0] + ' 2 ' + str(count + 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                            count += 1
                                    else:
                                        for i in range(len(graphItems[level])):
                                            if i == 0:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count + 1) + ' ' + str(len(graphItems[level])) + '\n')
                                                count += 1
                                            elif i == len(graphItems[level]) - 1:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                                count += 1
                                            else:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                count += 1
                                elif level == len(graphItems) - 1:  # 最后一层
                                    if len(graphItems[level]) == 1:
                                        if len(graphItems[level-1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 1 ' + str(count - 1) + '\n')
                                            count += 1
                                        else:
                                            writeTxt.write(graphItems[level][0] + ' 2 ' + str(count - len(graphItems[level-1])) + ' ' + str(count - 1) + '\n')
                                    else:
                                        for i in range(len(graphItems[level])):
                                            if i == 0:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - len(graphItems[level-1])) + ' ' + str(count + 1) + '\n')
                                                count += 1
                                            elif i == len(graphItems[level]) - 1:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count - len(graphItems[level])) + '\n')
                                                count += 1
                                            else:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                count += 1
                                else: # 中间层
                                    if len(graphItems[level]) == 1: # 中间层节点数为1
                                        if len(graphItems[level-1]) == 1 and len(graphItems[level+1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                            count += 1
                                        elif len(graphItems[level-1]) == 1 and len(graphItems[level+1]) != 1:
                                            writeTxt.write(graphItems[level][0] + ' 3 ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                            count += 1
                                        elif len(graphItems[level-1]) != 1 and len(graphItems[level+1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 3 ' + str(count - len(graphItems[level-1])) + ' ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                            count += 1
                                        else:
                                            writeTxt.write(graphItems[level][0] + ' 4 ' + str(count - len(graphItems[level-1])) + ' ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                            count += 1
                                    else:  # 中间层节点数不为1
                                        if len(graphItems[level - 1]) == 1 and len(graphItems[level + 1]) == 1:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level])) + ' ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                        elif len(graphItems[level - 1]) == 1 and len(graphItems[level + 1]) != 1:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - 1) + ' ' + str(count - len(graphItems[level])) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                        elif len(graphItems[level-1]) != 1 and len(graphItems[level+1]) == 1:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level-1])) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level])) + ' ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                        else:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level-1])) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level])) + ' ' + str(count - 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                            #print(graphItems)
                            flowCount += 1
                        firstAppIndex = None
                        flowLen = []

                    else:
                        flowLen = []
                else:
                    #if row[3].find('172.217') != -1:
                    #    firstIP = '31.'
                    #else:
                    firstIP = row[3][:4]
                    if firstIP.find('172.') != -1 or firstIP.find('10.') != -1 or firstIP.find('192.') != -1:
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex == None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if int(row[5]) != 66 and int(row[5])!= 54 and int(row[5])!= 60:
                            flowLen.append(str(int(row[5]) * -1))
                        '''
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            # print(row[5])
                            flowLen.append(str(int(row[5]) * -1))
                        '''
                    #print(row[3][:4])
                    '''
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex==None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            #print(row[5])
                            flowLen.append(str(int(row[5]) * -1))
                    '''
            readfile.close()
        except:
            readfile = open(readfilepath + readfileName, 'r')
            readCSV = csv.reader(readfile)
            # row = ['13576', '423.009129', '172.18.94.45', '104.24.3.10', 'TCP', '54', '53712 → 443 [ACK] Seq=1429 Ack=783934 Win=253952 Len=0']
            flowLen = []  # 记录流长度，流里边的数据包
            firstAppIndex = None
            for row in readCSV:
                #print(row)
                if len(row) == 0:
                    if len(flowLen) > 5:  # 四个数据包以上才作为一条流
                        if len(flowLen) > packetUse:
                            flowLen = flowLen[:packetUse]
                        #print(flowLen)
                        graphItems = genTixingGaphitems(flowLen)
                        count = 0
                        if len(graphItems) == 1:
                            #print(flowLen)
                            print('Hello')
                            '''
                            writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for i in range(len(flowLen)):
                                if i == 0:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + '1' + '\n')
                                elif i == len(flowLen) - 1:
                                    writeTxt.write(flowLen[i] + ' ' + '1' + ' ' + str(len(flowLen) - 1 - 1) + '\n')
                                else:
                                    writeTxt.write(flowLen[i] + ' ' + '2' + ' ' + str(i - 1) + ' ' + str(i + 1) + '\n')
                            flowCount += 1
                            '''
                        else:
                            writeTxt.write(str(len(flowLen)) + ' ' + str(dappName[dappNameTem]) + '\n')  # 写入数据流种数据包个数和类别
                            for level in range(len(graphItems)):
                                if level == 0: # 第一层
                                    if len(graphItems[level]) == 1:
                                        if len(graphItems[level+1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 1 ' + str(count + 1) + '\n')
                                            count += 1
                                        else:
                                            writeTxt.write(graphItems[level][0] + ' 2 ' + str(count + 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                            count += 1
                                    else:
                                        for i in range(len(graphItems[level])):
                                            if i == 0:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count + 1) + ' ' + str(len(graphItems[level])) + '\n')
                                                count += 1
                                            elif i == len(graphItems[level]) - 1:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                                count += 1
                                            else:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                count += 1
                                elif level == len(graphItems) - 1:  # 最后一层
                                    if len(graphItems[level]) == 1:
                                        if len(graphItems[level-1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 1 ' + str(count - 1) + '\n')
                                            count += 1
                                        else:
                                            writeTxt.write(graphItems[level][0] + ' 2 ' + str(count - len(graphItems[level-1])) + ' ' + str(count - 1) + '\n')
                                    else:
                                        for i in range(len(graphItems[level])):
                                            if i == 0:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - len(graphItems[level-1])) + ' ' + str(count + 1) + '\n')
                                                count += 1
                                            elif i == len(graphItems[level]) - 1:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count - len(graphItems[level])) + '\n')
                                                count += 1
                                            else:
                                                writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                count += 1
                                else: # 中间层
                                    if len(graphItems[level]) == 1: # 中间层节点数为1
                                        if len(graphItems[level-1]) == 1 and len(graphItems[level+1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                            count += 1
                                        elif len(graphItems[level-1]) == 1 and len(graphItems[level+1]) != 1:
                                            writeTxt.write(graphItems[level][0] + ' 3 ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                            count += 1
                                        elif len(graphItems[level-1]) != 1 and len(graphItems[level+1]) == 1:
                                            writeTxt.write(graphItems[level][0] + ' 3 ' + str(count - len(graphItems[level-1])) + ' ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                            count += 1
                                        else:
                                            writeTxt.write(graphItems[level][0] + ' 4 ' + str(count - len(graphItems[level-1])) + ' ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                            count += 1
                                    else:  # 中间层节点数不为1
                                        if len(graphItems[level - 1]) == 1 and len(graphItems[level + 1]) == 1:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level])) + ' ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                        elif len(graphItems[level - 1]) == 1 and len(graphItems[level + 1]) != 1:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - 1) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - 1) + ' ' + str(count - len(graphItems[level])) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                        elif len(graphItems[level-1]) != 1 and len(graphItems[level+1]) == 1:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level-1])) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level])) + ' ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                                        else:
                                            for i in range(len(graphItems[level])):
                                                if i == 0:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level-1])) + ' ' + str(count + 1) + ' ' + str(count + len(graphItems[level])) +'\n')
                                                    count += 1
                                                elif i == len(graphItems[level]) - 1:
                                                    writeTxt.write(graphItems[level][i] + ' 3 ' + str(count - len(graphItems[level])) + ' ' + str(count - 1) + ' ' + str(count + len(graphItems[level+1])) + '\n')
                                                    count += 1
                                                else:
                                                    writeTxt.write(graphItems[level][i] + ' 2 ' + str(count - 1) + ' ' + str(count + 1) + '\n')
                                                    count += 1
                            #print(graphItems)
                            flowCount += 1
                        firstAppIndex = None
                        flowLen = []
                    else:
                        flowLen = []
                else:
                    #if row[3].find('172.217') != -1:
                    #    firstIP = '31.'
                    #else:
                    firstIP = row[3][:4]
                    if firstIP.find('172.') != -1 or firstIP.find('10.') != -1 or firstIP.find('192.') != -1:
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex == None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if int(row[5]) != 66 and int(row[5])!= 54 and int(row[5])!= 60:
                            flowLen.append(str(int(row[5]) * -1))
                        '''
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            # print(row[5])
                            flowLen.append(str(int(row[5]) * -1))
                        '''
                    '''
                    if row[3].find('172.') != -1 or row[3].find('10.') != -1 or row[3].find('192.') != -1:
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            # writefile.write(row[5] + ',' + row[6] + '\n')
                            flowLen.append(row[5])
                        if row[6].find('Application Data') != -1 and firstAppIndex==None:
                            firstAppIndex = len(flowLen) - 1
                    else:
                        if row[4].find('TLS') != -1 or row[4].find('SSL') != -1:
                            flowLen.append(str(int(row[5]) * -1))
                    '''
            readfile.close()
    writeTxt.close()
    #最后将流的数量写入第一行
    with open(writefileName, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(str(flowCount) + '\n' + content)


def genTixingGaphitems(flowLen):
    graphItems = []
    graphItemst = []
    for i in range(len(flowLen)):
        if i == 0:
            graphItemst.append(flowLen[i])
        elif int(flowLen[i]) > 0 and int(flowLen[i - 1]) > 0:
            graphItemst.append(flowLen[i])
        elif int(flowLen[i]) < 0 and int(flowLen[i - 1]) < 0:
            graphItemst.append(flowLen[i])
        else:
            graphItems.append(graphItemst)
            graphItemst = []
            graphItemst.append(flowLen[i])
    if len(graphItemst) != 0:
        graphItems.append(graphItemst)
    return graphItems


def main():
    #extractDownLenandFlagNF('data/ALL/', 'feature/DAPP.txt')
    extractDownLenandFlagBiTixing('data/ALL/', 'feature/DAPPBI.txt')
    #extractDownLenandFlagBi('data/ALL/', 'feature/DAPPBI.txt')
    #extractDownLenandFlagBi('data/FFFC/', 'feature/DAPPBIF.txt')
    #extractDownLenandFlagBiDuo('data/ALL/', 'feature/DAPPBI.txt')
    #extractDownLenandFlagBiDuo('data/TTTT/', 'feature/DAPPBI.txt')
    #extractDownLenandFlagGFlist('data/TTTT/', 'feature/DAPP.txt')


if __name__=='__main__':
    main()
