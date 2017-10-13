import sys
import os
import re

global test_result_dict
test_result_dict = {}

def connected_product(text):
    product = re.search(r"\n*.*\n*(:: Sensor: )FPC(.*) Touch Sensor", text)
    return product

def check_case_result(text):
    tests = re.findall(r"\n*.*\n*-> Test (.*) \(", text)

    test_results = {}
    for test in tests:
        pattern = r"\n*.*\n*" + test + r": (.*) \("
        res = re.search(pattern, text)
        if res:
            test_results[test] = res.group(1)

            if res.group(1) == "Success":
                if test in test_result_dict:
                    test_result_dict[test] += 1
                else:
                    test_result_dict[test] = 1

    return test_results

def check_file_result(path, file_name):
    log_pass = False
    read_file = open(path + "\\" + file_name)
    text = read_file.read()

    match_success = re.search(r".*Module Test: Success", text)

    if match_success:
        log_pass = True
    else:
        print(file_name, "Failed")

    product = connected_product(text)
    if product:

        test_results = check_case_result(text)
        for test in test_results:
            log = mtt_log(file_name, product.group(2), test, test_results[test])            #logs.append(log)
            if log.test_result == "Fail" or log.test_result == "Exception":
                print(str(log))

    else:
        print("Connect error")

    return log_pass

def check_logs(path):
    files = os.listdir(path)

    pass_number = 0
    fail_number = 0
    for name in files:
        if(os.path.isfile( path + "\\" + name)):
            res = re.search(r".*_log.txt", name)
            if res:
                if check_file_result(path, name):
                    pass_number += 1
                else:
                    fail_number += 1
        else:
            #print(r"\nFolder" , path + "\\" + name)
            (p, f) = check_logs(path + "\\" + name)
            pass_number += p
            fail_number += f

    return pass_number, fail_number

def main(path):
    p, f = check_logs(path)
    log_num = p + f
    print("Total log number:", log_num)
    print("Pass number: ", p)
    if log_num != 0:
        pass_rate = p / log_num
        print("Pass rate: ", pass_rate)

    print(test_result_dict)
    for test in test_result_dict:
        print(test, "pass rate: ", test_result_dict[test] / log_num)

class mtt_log(object):
    def __init__(self, log_name, product, test_name, test_result):
        self.log_name = log_name
        self.product = product
        self.test_name = test_name
        self.test_result = test_result

    def __str__(self):
        log_str = self.product + " " +\
                  self.log_name + ": " + \
                  self.test_name + " " + \
                  self.test_result

        return log_str


if __name__ == "__main__":
    main(r"D:\Temp\MKML0RQ\MKML0RQ")