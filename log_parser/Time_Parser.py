import sys
import os
import re
import matplotlib.pyplot as plt
from functools import reduce

def check_exec_time(path):
    files = os.listdir(path)
    time_results = {}
    time_histo_dict = {0: 0, 100: 0, 200: 0, 300: 0, 400: 0, 500: 0, 600: 0}

    for file_name in files:
        if(os.path.isfile(path + "\\" + file_name)):
            res = re.search(r".*_log.", file_name)
            if res:
                with open(path + "\\" + file_name) as read_file:
                    text = read_file.read()
                    time = re.findall(r"\(Test time: (.*)ms\)", text)
                    if time:
                        time_results[file_name] = int(time[0])

                        if int(time[0]) < 100:
                            time_histo_dict[0] += 1
                        elif int(time[0]) >= 100 and int(time[0]) < 200:
                            time_histo_dict[100] += 1
                        elif int(time[0]) >= 200 and int(time[0]) < 300:
                            time_histo_dict[200] += 1
                        elif int(time[0]) >= 300 and int(time[0]) < 400:
                            time_histo_dict[300] += 1
                        elif int(time[0]) >= 400 and int(time[0]) < 500:
                            time_histo_dict[400] += 1
                        elif int(time[0]) >= 500 and int(time[0]) < 600:
                            time_histo_dict[500] += 1
                        elif int(time[0]) >= 600:
                            time_histo_dict[600] += 1
        else:
            print("Test Folder:", file_name)
            check_exec_time(path + "\\" + file_name)

    if len(time_results) != 0:
        total_time = reduce(lambda x, y : x + y, list(time_results.values()))
        print("Total logs:", time_results)
        print("Average time:", total_time / len(time_results))
        print("Max time:", max(time_results.values()))
        print("Min time:", min(time_results.values()))

        #x = [x for x in range(len(time_results))]
        #y = list(time_results.values())
        # plt.plot(list(x), list(y))
        # plt.show()

        plt.xlabel("Time")
        plt.ylabel("Count")
        plt.plot(list(time_histo_dict.keys()), list(time_histo_dict.values()))
        plt.show()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print ("HELP: python Time_Parser.py <directory>")
    else:
        path = sys.argv[1]
        check_exec_time(path)
