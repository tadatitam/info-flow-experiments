
import os
import sys
import json
from collections import namedtuple

def load_ads_from_json(log_name,session):
    # The save file name format is "adb_logfile.session.json
    dirname = os.path.dirname(log_name)
    base=os.path.splitext(os.path.basename(log_name))[0][4:]
    json_name  = base+"."+session+".json" 
    json_file = os.path.join(dirname,json_name)
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

def get_site_reloads(ad_lines):
    '''
    Given a list of ad lines, return a list of the sites that ads where collected on
    '''
    sites = set()
    for ad in ad_lines:
        sites.add((ad.on_site,ad.reloads))
    
    return sorted(list(sites),key=lambda s: s[1])

def get_ad_element(ad_lines,element):
    '''
    Given a list of ad lines, return a list of the sites that ads where collected on
    '''
    sites = set()
    for ad in ad_lines:
        sites.add(getattr(ad, element))
    
    return sorted(list(sites))


def combine_sessions(data):
    '''
    provided the loaded data (dict keyed on session) return all adlines in a list
    '''
    all_data = []
    for session in data:
        unit_id, treatment_id, ad_lines = data[session]
        for ad in ad_lines:
            all_data.append((session,ad))
    return all_data


def group_on_link_text(data):
    '''
    Given the loaded data, group links across session, site and reload by
    link_text. Return a dict, keyed on link_text, with a list of appearances
    '''
    all_data = combine_sessions(data)
    
    ads_by_link={}
    for row in all_data:
        session,ad = row
        lt = ad.link_text
        if lt != '':
            row_data =(session,ad.on_site,ad.reloads)
            if lt in ads_by_link:
                ads_by_link[lt].append(row_data)
            else:
                ads_by_link[lt] = [row_data]
    
    return ads_by_link

def print_link_text_groups(ads_by_link):
    for link_text in ads_by_link:
        print "-"*80
        print("link text: {}".format(link_text[:80]))
        instances = ads_by_link[link_text]
        for ad in instances:
            session,on_site,reloads = ad
            print("\ton: {} : reload: {} : session: {}".format(on_site,reloads,session))

def group_on_url(data):
    '''
    Given the loaded data, group links across session, site and reload by
    url. Return a dict, keyed on url, with a list of appearances
    '''
    all_data = combine_sessions(data)
    
    ads_by_url={}
    for row in all_data:
        session,ad = row
        url = ad.url

        row_data = ad
        if url in ads_by_url:
             ads_by_url[url].append(row_data)
        else:
            ads_by_url[url] = [row_data]
    
    return ads_by_url

def print_url_groups(ads_by_url):
    for url in ads_by_url:
        instances = ads_by_url[url]
        on = get_ad_element(instances,"on_site")
        lt= get_ad_element(instances,"link_text")
        # skip blank ones
        if not (len(lt) ==1 and lt[0] == ''):

            print "-"*80
            print("url: {} on {}".format(url[:40],on))
            for ad in instances:

                print("\tlink_text: {}".format(ad.link_text))

def ads_on_site_reload(ad_lines,site,reloads):
    return [ad for ad in ad_lines if ad.on_site==site and ad.reloads==reloads]

def print_simple_line(ad,level=0):
    if ad.link_text != '':
        print("\t"*level+"url: {} link_text: {}".format(ad.url[:20],ad.link_text[:40]))

def print_by_site_reload(ad_lines):

    sites = get_site_reloads(ad_lines)

    for s in sites:
        site, reloads = s
        ads = ads_on_site_reload(ad_lines,site,reloads)
        print("Site: {} Reload: {}".format(site,reloads))
        cnt =0
        for a in ads:
            print_simple_line(a,1)
        
def print_by_session(data,printer):
    for session in data:
        unit_id, treatment_id, ad_lines = data[session]
        print "-"*80
        print("Session/Treatment/Unit: {}/{}/{} : \n".format(session,treatment_id,unit_id))
        printer(ad_lines)

def simple_print(data):
    
    print("{} Sessions".format(len(data)))
    for session in data:
        unit_id, treatment_id, ad_lines = data[session]
        print "-"*80
        print("\nSession/Treatment/Unit: {}/{}/{} : ".format(session,treatment_id,unit_id))
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
        print("Session: {} was treatment/unit {}/{}".format(session_id,treatment_id,unit_id))
        ad_lines = load_ads_from_json(log_file,session_id)
        data[session_id] = [unit_id, treatment_id,ad_lines]

    print("### Simple Ad Data ###")
    simple_print(data)

    print("\n### Ads grouped by Session ###")
    print_by_session(data,print_by_site_reload)

    print("\n### Ads grouped by link_text ###")
    print_link_text_groups(group_on_link_text(data))

    print("\n### Ads grouped by url ###")
    print_url_groups(group_on_url(data))

    print("\n### Ad Matrix ###")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("pass in log_file as an argument")
