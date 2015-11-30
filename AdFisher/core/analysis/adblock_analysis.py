
import os
import sys
import json
from collections import namedtuple

def load_ads_from_json(log_name,session):
    json_file = os.path.splitext(log_name)[0]+"."+session+".json"
    with open(json_file, 'r') as infile:
        raw_ad_lines = json.load(infile)
    
    print("loaded {} lines from session: {}".format(len(raw_ad_lines),session))

    ad_lines =[]
    for line in raw_ad_lines:
        # parse line back into a named tuple, properly encoding to utf-8
        utf8_line  = map(lambda s: s.encode('utf-8') if not isinstance(s, dict) and not isinstance(s,int) else s, line)
        ad_lines.append(Ad(*utf8_line))

    return ad_lines
    
def find_json_logs(log_file):
    json_logs=[]
    with open(log_file,'r') as log:
        for line in log.readlines():
            if "save_data" in line:
                d = line.strip().split(":")[3:]
                json_logs.append(d)
    return json_logs


def simple_print(data):
    
    print("{} Sessions".format(len(data)))
    for session in data:
        unit_id, treatment_id, ad_lines = data[session]
        print("Session/Unit/Treatment: {}/{}/{} : ".format(session,unit_id,treatment_id))
        print("# adlines: {}".format(len(ad_lines)))
        cnt =0
        for ad in ad_lines:
            if ad.link_text !='':
                print("{} : {} : {}".format(ad.url[:30],ad.link_text, ad.on_site))
            else:
                cnt+=1
        print ("and {} ad resources without link text".format(cnt))



Ad = namedtuple('Ad',['url','outerhtml','tag','link_text','link_location','on_site', 'reloads'])

def main(log_file):

    # A dictionary of sessions keyed by session_id
    # Values are [unit_id,treatment_id,[ad_line0,ad_line1,..,ad_lineN]]
    data  = {}


    json_logs = find_json_logs(log_file)
    for log in json_logs:
        unit_id, treatment_id, session_id = log
        print("Session: {} was unit/treatment {}/{}".format(session_id,unit_id,treatment_id))
        ad_lines = load_ads_from_json(log_file,session_id)
        data[session_id] = [unit_id, treatment_id,ad_lines]

    simple_print(data)

if __name__ == "__main__":
    
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("pass in log_file as an argument")
