import sys
import os
import re
import pandas as pd

test_result_dict = {}

csv_cols = ["Log", "Result"]
csv_data = []

def get_cols(log):
    with open(log, encoding='utf-8') as f:
        text = f.read()
        test_name = re.findall(r"\n*.*\n*-> Test (.*) \(", text)

        for name in test_name:
            if name not in csv_cols:
                csv_cols.append(name)

    return csv_cols

def get_results(log):
    result = []
    result.append(log)

    with open(log, encoding='utf-8') as f:
        text = f.read()
        success = re.findall(r"==> Module Test: Success", text)
        if success:
            result.append("Success")
        else:
            result.append("Fail")

        for name in csv_cols[2:]:
            pattern = re.findall(r"\n*.*\n*"+ name + r": (.*) \(", text)
            if pattern:
                result.append(pattern[0])
            else:
                result.append("")

    csv_data.append(result)

def extract_logs(path):
    files = os.listdir(path)

    for name in files:
        log = path + "\\" + name
        if(os.path.isfile(log)):
            res = re.search(r".*_log.*", name)
            if res:
                get_cols(log)
                get_results(log)

        else:
            print(r"\nFolder" , path + "\\" + name)
            extract_logs(path)

    print("{} files processed...".format(len(files)))

def execute(path, csv_path):
    extract_logs(path)

    df = pd.DataFrame(csv_data, columns=csv_cols)
    df.to_csv(csv_path, encoding='utf-8', index=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python mtt_to_csv.py <log_path> <csv_file_name>")
    else:
        execute(sys.argv[1], sys.argv[2])