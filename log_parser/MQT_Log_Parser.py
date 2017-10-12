import sys
import os
import re
import matplotlib.pyplot as plt
from functools import reduce

def check_ofilm_snr_results(path):
    files = os.listdir(path)
    snr_results = {}

    html_count = 0
    snr_histo_file_name = {0:[], 8:[], 9:[], 10:[], 11:[], 12:[], 13:[], 14:[], 15:[], 16:[], 17:[], 18:[]}
    snr_histo_dict = {0: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0}

    for file_name in files:
        if(os.path.isfile(path + "\\" + file_name)):
            res = re.search(r".*_log.", file_name)
            if res:
                html_count += 1
                with open(path + "\\" + file_name, encoding='utf8') as read_file:
                    text = read_file.read()
                    snr = re.findall(r"snr: (.*) \(", text)
                    if snr:
                        snr_results[file_name] = float(snr[0])

                        if float(snr[0]) < 8:
                            snr_histo_file_name[0].append(file_name)
                            snr_histo_dict[0] += 1
                        elif float(snr[0]) >= 8 and float(snr[0]) < 9:
                            snr_histo_file_name[8].append(file_name)
                            snr_histo_dict[8] += 1
                        elif float(snr[0]) >= 9 and float(snr[0]) < 10:
                            snr_histo_file_name[9].append(file_name)
                            snr_histo_dict[9] += 1
                        elif float(snr[0]) >= 10 and float(snr[0]) < 11:
                            snr_histo_file_name[10].append(file_name)
                            snr_histo_dict[10] += 1
                        elif float(snr[0]) >= 11 and float(snr[0]) < 12:
                            snr_histo_file_name[11].append(file_name)
                            snr_histo_dict[11] += 1
                        elif float(snr[0]) >= 12 and float(snr[0]) < 13:
                            snr_histo_file_name[12].append(file_name)
                            snr_histo_dict[12] += 1
                        elif float(snr[0]) >= 13 and float(snr[0]) < 14:
                            snr_histo_file_name[13].append(file_name)
                            snr_histo_dict[13] += 1
                        elif float(snr[0]) >= 14 and float(snr[0]) < 15:
                            snr_histo_file_name[14].append(file_name)
                            snr_histo_dict[14] += 1
                        elif float(snr[0]) >= 15 and float(snr[0]) < 16:
                            snr_histo_file_name[15].append(file_name)
                            snr_histo_dict[15] += 1
                        elif float(snr[0]) >= 16 and float(snr[0]) < 17:
                            snr_histo_file_name[16].append(file_name)
                            snr_histo_dict[16] += 1
                        elif float(snr[0]) >= 17 and float(snr[0]) < 18:
                            snr_histo_file_name[17].append(file_name)
                            snr_histo_dict[17] += 1
                        elif float(snr[0]) >= 18:
                            snr_histo_file_name[18].append(file_name)
                            snr_histo_dict[18] += 1
                    #else:
                    #    print(file_name)
        else:
            print("Test Folder:", file_name)
            check_ofilm_snr_results(path + "\\" + file_name)

    if len(snr_results) != 0:
        total_snr = reduce(lambda x, y : x + y, list(snr_results.values()))
        print("Total logs:", html_count)
        print("MQT with SNR count:", len(snr_results))
        print("Average SNR:", total_snr / len(snr_results))
        print("Max SNR:", max(snr_results.values()))
        print("Min SNR:", min(snr_results.values()))

        #x = [x for x in range(len(snr_results))]
        #y = list(snr_results.values())

        plt.xlabel("SNR Value")
        plt.ylabel("Count")
        plt.plot(list(snr_histo_dict.keys()), list(snr_histo_dict.values()))
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ("HELP: python MQT_Log_Parser.py <directory>")
    else:
        path = sys.argv[1]
        check_ofilm_snr_results(path)
