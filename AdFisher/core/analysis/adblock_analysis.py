
import os
import sys
import json
from collections import namedtuple

def load_ads_from_json(log_name,session):
    json_file = os.path.splitext(log_name)[0]+"."+session+".json"
    with open(json_file, 'r') as infile:
        ad_lines = json.load(infile)
    
    print "loaded {} lines from session: {}".format(len(ad_lines),session)
    return ad_lines
    
def find_json_logs(log_file):
    json_logs=[]
    with open(log_file,'r') as log:
        for line in log.readlines():
            if "save_data" in line:
                print line.strip()
                d = line.strip().split(":")[3:]
                json_logs.append(d)
    return json_logs

def main(log_file):

    # A dictionary of sessions keyed by session_id
    # Values are [unit_id,treatment_id,[ad_line0,ad_line1,..,ad_lineN]]
    data  = {}

    ad_line = namedtuple('Ad',['url','outerhtml','tag','link_text','link_location','on_site', 'reloads'])

    json_logs = find_json_logs(log_file)
    for log in json_logs:
        unit_id, treatment_id, session_id = log
        print("Session: {} was unit/treatment {}/{}".format(session_id,unit_id,treatment_id))
        ad_lines = load_ads_from_json(log_file,session_id)
        data[session_id] = [unit_id, treatment_id,ad_lines]


if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "pass in log_file as an argument"
