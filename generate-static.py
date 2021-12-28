import json
import logging
from datetime import datetime
import requests
import csv
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# from smc import session
# from smc.elements.network import Host, Network, AddressRange, IPList
import os
from pprint import *
# import functions as f
import base64


### Input variables
IPAM_LOGIN = os.environ.get('IPAM_LOGIN')
IPAM_PASSWORD = os.environ.get('IPAM_PASSWORD')
IPAM_HOSTNAME = os.environ.get('IPAM_HOSTNAME')
OUTPUT_PATH = str(os.environ.get('OUTPUT_PATH'))

DEFAULT_THRESHOLD_MIN_IPAM = int(os.environ.get('DEFAULT_THRESHOLD_MIN_IPAM'))
# MAX_ADDRESS_TO_SEND = int(os.environ.get('MAX_ADDRESS_TO_SEND'))

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# import urllib3
# urllib3.disable_warnings() # suppression des warning du insecure https


### CONSTANT
# IPAM_HOSTNAME = "ipam.fr.corp.leroymerlin.com"
# DASHNET_HOSTNAME = "api.dashnet.fr.corp.leroymerlin.com"
print( IPAM_LOGIN )
print( IPAM_HOSTNAME)
IPAM_CREDENTIAL = f"{IPAM_LOGIN}:{IPAM_PASSWORD}"
dictionnaryOfUsagesWithTheirRanges = {}

if OUTPUT_PATH == "None" :
    outputPath = "./temp/"
else:
    outputPath = OUTPUT_PATH

def getAllRangesFromIpam(ipamHostname, ipamCredential):
    start = datetime.now()
    # r = requests.get(f"https://{ipamCredential}@{ipamHostname}/wapi/v2.4/range?_return_fields=extattrs,start_addr,end_addr&_return_type=json&_max_results=-100000", verify=False)
    r = requests.get(f"https://{ipamCredential}@{ipamHostname}/wapi/v2.4/range?_return_fields=extattrs,start_addr,end_addr&_return_type=json&_max_results=100", verify=False)
    data = json.loads(r.text)
    stop = datetime.now()
    temps_requete = (stop - start)
    return data


listRangesAsIpamJson = getAllRangesFromIpam(IPAM_HOSTNAME, IPAM_CREDENTIAL)

print(listRangesAsIpamJson)
print()


# A modifier -> Un CSV avec addr debut, fin, site id et vlan
for currentRange in listRangesAsIpamJson:
    end_addr = currentRange['end_addr']
    start_addr = currentRange['start_addr']
    range = f"{start_addr}-{end_addr}"
    # currentRange['vlan'] = currentRange['extattrs']['VLAN']['value']
    
    if 'site_id' in currentRange['extattrs']:
        currentRange['siteId'] = currentRange['extattrs']['site_id']['value']
        site_id = f"{currentRange['siteId']}"
    else:
        site_id = f"NoSiteID"
    
    if 'usage'  in currentRange['extattrs']:
        currentRange['usage'] = currentRange['extattrs']['usage']['value'].lower()
    
    if 'VLAN' in currentRange['extattrs']:
        currentRange['vlan'] = currentRange['extattrs']['VLAN']['value']
        vlan = f"{currentRange['vlan']}"
    else:
        vlan = f"NoVlan"
    
    print(currentRange)
    
    if currentRange['usage'] in dictionnaryOfUsagesWithTheirRanges:
        dictionnaryOfUsagesWithTheirRanges[currentRange['usage']].append(range)
    else:
        dictionnaryOfUsagesWithTheirRanges[currentRange['usage']] = [site_id][vlan][range]
        pprint(dictionnaryOfUsagesWithTheirRanges[currentRange['usage']])

'''
for currentUsage in dictionnaryOfUsagesWithTheirRanges:
    currentUsageRangeList = dictionnaryOfUsagesWithTheirRanges[currentUsage]
    print(currentUsage)
    # print(dictionnaryOfUsages[currentUsage])    
    contenuDuFichier = "\n".join(currentUsageRangeList)
    outputFilename = f"{outputPath}/range-{currentUsage}.txt"
    print(f"output file is {outputFilename}")
    f = open(outputFilename, "w")
    f.write(contenuDuFichier)
    f.close()
'''


for currentUsage in dictionnaryOfUsagesWithTheirRanges:
    outputFilename = f"{outputPath}/range-{currentUsage}.csv"
    with open(outputFilename, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        currentUsageRangeList = dictionnaryOfUsagesWithTheirRanges[currentUsage]
        print(currentUsage)
        # print(dictionnaryOfUsages[currentUsage])
        contenuDuFichier = "\n".join(currentUsageRangeList)
        spamwriter.writerow([currentUsageRangeList[0], currentUsageRangeList[1], currentUsageRangeList[2],
                             currentUsageRangeList[3]])
        print(f"output file is {outputFilename}")
exit()


