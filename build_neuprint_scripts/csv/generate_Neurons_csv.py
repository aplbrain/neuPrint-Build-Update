#!/bin/env
# python generate_Neuprint_Meta_ftr.py mb6_synapse_data_example.ftr meta.yaml > Neuprint_Meta_mb6.csv
# ------------------------- imports -------------------------
import json
import sys
import os
import io
import time
import numpy as np
from tqdm import trange
# from neuclease.dvid import *
# from libdvid import DVIDNodeService, ConnectionMethod
import pandas as pd
import yaml

def parse_config (config_file):
    with open(config_file) as f:
        config_data = yaml.load(f, Loader=yaml.FullLoader)
    return config_data

if __name__ == '__main__':
    bodies_syn_file =  sys.argv[1] #csv file
    neurons_ftr = sys.argv[2]
    config_yaml_file = sys.argv[3]
    config_data = parse_config(config_yaml_file)
    
    dataset = config_data['dataset']

    all_rois_csv = config_data['all_rois_csv']    
    all_rois = []
    allRoisList = open(all_rois_csv,'r')
    for line in allRoisList:
        roi_name = line.rstrip('\n')
        all_rois.append(roi_name)

    downstream_lookup = {}
    downstream_csv = config_data['downstream_csv']    
    allDownStream = open(downstream_csv,'r')
    for line in allDownStream:
        clean_line = line.rstrip('\n')
        downstream_data = clean_line.split(",")
        bodyId = downstream_data[0]
        downstream_count = downstream_data[1]
        downstream_lookup[bodyId] = downstream_count

    downstream_roiInfo_lookup = {}
    downstream_roiInfo = config_data['downstream_roiInfo']
    allDownStreamRoiInfo = open(downstream_roiInfo,'r')
    for line in allDownStreamRoiInfo:
        clean_line = line.rstrip('\n')
        downstream_roiInfo_data = clean_line.split(";")
        bodyId = downstream_roiInfo_data[0]
        dns_roiInfo_str = downstream_roiInfo_data[1]
        dns_roiInfo = json.loads(dns_roiInfo_str)
        downstream_roiInfo_lookup[bodyId] = dns_roiInfo

    #somaFile = "/groups/flyem/home/flyem/bin/identify_soma/soma_bodies_" + dvid_uuid + ".txt"
    #somaList = open(somaFile,'r')
    soma_lookup = {}
    #for line in somaList:
    #    data_str = line.rstrip('\n')
    #    data = data_str.split(",")
    #    soma_bodyID = data[0]
    #    soma_data = data[1].split(" ")
    #    soma_lookup[str(soma_bodyID)] = soma_data

    df = pd.read_csv(neurons_ftr, keep_default_na=False)

    all_values = {}
    for index, row in df.iterrows():
        #body     statusLabel cropped instance    type        size  somaLocation
        neuron_annot = {}
        bodyId = str(row['body'])
        neuron_annot['bodyId'] = row['body']

        status = row['statusLabel']
        if status == None:
            status = ""
        else:
            status = row['statusLabel']
        neuron_annot['status'] = status

        if row['cropped'] == None:
            cropped = ""
        else:
            cropped = str(row['cropped'])
        neuron_annot['cropped'] = cropped

        if row['instance'] == None:
            instance = ""
        else:
            instance = row['instance']
        neuron_annot['instance'] = instance

        if row['type'] == None:
            neuron_type = ""
        else:
            neuron_type = row['type']
        neuron_annot['neuron_type'] = neuron_type

        if row['size'] == None:
            neuron_size = ""
        else:
            neuron_size = row['size']
        neuron_annot['size'] = neuron_size

        if row['name'] == None:
            neuron_name = ""
        else:
            neuron_name = row['name']
        neuron_annot['name'] = neuron_name

        if row['somaX'] == None:
            somaLocationX = ""
        else:
            somaLocationX = row['somaX']
        neuron_annot['somaX'] = somaLocationX

        if row['somaY'] == None:
            somaLocationY = ""
        else:
            somaLocationY = row['somaY']
        neuron_annot['somaY'] = somaLocationY

        if row['somaZ'] == None:
            somaLocationZ = ""
        else:
            somaLocationZ = row['somaZ']
        neuron_annot['somaZ'] = somaLocationZ

        all_values[bodyId] = neuron_annot
        

    bodiesList = open(bodies_syn_file,'r')

    header = '":ID(Body-ID)","bodyId:long","pre:int","post:int","upstream:int","downstream:int","synweight:int","status:string","statusLabel:string","cropped:boolean","instance:string","notes:string","type:string","cellBodyFiber:string","somaLocation:point{srid:9157}","somaRadius:float","size:long","roiInfo:string",":LABEL"'
    for roi in all_rois:
        header = header + ',"' + roi + ':boolean"'

    print (header)

    for line in bodiesList:
        tmp0 = line.rstrip('\n')
        #tmp1 = tmp0.replace("\ufeff","")
        if tmp0[0].isdigit():
            bodyData = tmp0.split(";")
            bodyID = bodyData[0]
            pre_syns = bodyData[1]
            post_syns = bodyData[2]

            upstream = "0"
            if int(post_syns) > 0:
                upstream = str(post_syns)

            downstream = "0"
            if bodyID in downstream_lookup:
                downstream = str(downstream_lookup[bodyID])

            total_synweight = int(upstream) + int(downstream)
            
            roiInfo = bodyData[3]
            if len(roiInfo) > 0:
                roiInfo_str = bodyData[3].replace('"','""')
            else:
                roiInfo = "{}"
                roiInfo_str = "{}"

            if len(roiInfo) > 0:
                downstream_roiInfo = {}
                if bodyID in downstream_roiInfo_lookup:
                    downstream_roiInfo = downstream_roiInfo_lookup[bodyID]
                roiInfo_json = json.loads(roiInfo)
                for roiName in roiInfo_json:
                    roiData = roiInfo_json[roiName]
                    roisynweight = 0
                    if roiName in downstream_roiInfo:
                        dns_data = downstream_roiInfo[roiName]
                        roiData["downstream"] = dns_data["downstream"]
                        roisynweight += dns_data["downstream"]
                    if "post" in roiData:
                        roiData["upstream"] = roiData["post"]
                        roisynweight += roiData["post"]
                    if roisynweight > 0:
                        roiData["synweight"] = roisynweight
                roiInfo_tmp = json.dumps(roiInfo_json)
                roiInfo_str = roiInfo_tmp.replace('"','""')
            else:
                roiInfo = "{}"
                roiInfo_str = "{}"
            
            # somaLocation = ""
            # somaLocationX = ""
            # somaLocationY = ""
            # somaLocationZ = ""
            somaRadius = ""
            bodySize = "0"
            status = ""
            instance = ""
            neuronType = ""
            primaryNeurite = ""
            majorInput = ""
            majorOutput = ""
            neurotransmitter = ""
            clonalUnit = ""
            statusLabel = ""
            cropped = ""
            synonyms = ""
            #isDistinct = ""

            roi_info_dict = {}
            if len(bodyData[3]) > 0:
                roi_info_dict = json.loads(bodyData[3])

            roi_booleans = ""
            for roi_name in all_rois:
                is_roi = ""
                #roi_search = roi_name.replace("|",",")
                if roi_name in roi_info_dict:
                    is_roi = "true"
                roi_booleans = roi_booleans + "," + is_roi

            #if bodyID in size_lookup:
            #    bodySize = size_lookup[bodyID]

            # if bodyID in soma_lookup:
            #     soma_data = soma_lookup[bodyID]
            #     somaLocationX = int(float(soma_data[2]))
            #     somaLocationY = int(float(soma_data[3]))
            #     somaLocationZ = int(float(soma_data[4]))
            #     somaLocation = '"{x:' + str(somaLocationX) + ',y:' + str(somaLocationY) + ',z:' + str(somaLocationZ) + '}"'
            #     somaRadius = soma_data[5]

            # somaLocation = '"{x:' + str(somaLocationX) + ',y:' + str(somaLocationY) + ',z:' + str(somaLocationZ) + '}"'
            
            if bodyID in all_values:
                bodyData = all_values[bodyID]
                if bodyData is None:
                    bodyData = {}
                    #continue
                    
                if 'size' in bodyData:
                    bodySize = str(bodyData['size'])

                if 'cropped' in bodyData:
                    cropped = bodyData["cropped"]
                    
                if 'status' in bodyData:
                    status = bodyData["status"]
                    statusLabel = status
                    if 'Traced' == status:
                        status = "Traced"
                        cropped = "false"
                    if " traced" in status:
                        status = "Traced"
                        cropped = "false"
                    if status == "Leaves":
                        status = "Traced"
                        cropped = "true"
                    if status == "Orphan hotknife":
                        status = "Orphan"
                    if status == "Orphan-artifact":
                        status = "Orphan"
                    if status == "0.5assign":
                        status = "Assign"

                if 'synonym' in bodyData:
                    synonym1 = bodyData["synonym"]
                    synonym2 = synonym1.rstrip('\n')
                    synonyms = '"' + synonym2 + '"'

                if 'name' in bodyData:
                    instance1 = bodyData["name"]
                    instance2 = instance1.rstrip('\n')
                    instance = instance2.replace(',','')

                if 'instance' in bodyData:
                    instance1 = bodyData["instance"]
                    instance2 = instance1.rstrip('\n')
                    instance = instance2.replace(',','')
                
                if 'neuron_type' in bodyData:
                    neuronType1 = bodyData["neuron_type"]
                    neuronType2 = neuronType1.rstrip('\n')
                    neuronType = neuronType2.replace(',','')

                #if 'property' in bodyData:
                #    if bodyData['property'] == "Distinct":
                #        isDistinct = "true"

                if 'primary neurite' in bodyData:
                    primaryNeurite1 = bodyData["primary neurite"]
                    primaryNeurite2 = primaryNeurite1.rstrip('\n')
                    primaryNeurite = primaryNeurite2.replace(',','')
                
                if 'major input' in bodyData:
                    majorInput1 = bodyData["major input"]
                    majorInput2 = majorInput1.rstrip('\n')
                    majorInput = '"' + majorInput2 + '"'

                if 'major output' in bodyData:
                    majorOutput1 = bodyData["major output"]
                    majorOutput2 = majorOutput1.rstrip('\n')
                    majorOutput = '"' + majorOutput2 + '"'

                if 'neurotransmitter' in bodyData:
                    neurotransmitter1 = bodyData["neurotransmitter"]
                    neurotransmitter2 = neurotransmitter1.rstrip('\n')
                    neurotransmitter = neurotransmitter2.replace(',','')

                if 'clonal unit' in bodyData:
                    clonalUnit1 = bodyData["clonal unit"]
                    clonalUnit2 = clonalUnit1.rstrip('\n')
                    clonalUnit = clonalUnit2.replace(',','')
                #clonalUnit = ""

                if 'somaX' in bodyData and 'somaY' in bodyData and 'somaZ' in bodyData:
                    somaLocation = '"{x:' + str(bodyData["somaX"]) + ',y:' + str(bodyData["somaY"]) + ',z:' + str(bodyData["somaZ"]) + '}"'
                else:
                    somaLocation = ""
                
            is_hemibrain_Neuron = ""
            if int(pre_syns) >= 2:
                is_hemibrain_Neuron = ";Neuron;" + dataset + "_Neuron"
            elif int(post_syns) >= 10:
                is_hemibrain_Neuron = ";Neuron;" + dataset + "_Neuron"
            elif len(somaRadius) > 0:
                is_hemibrain_Neuron = ";Neuron;" + dataset + "_Neuron"

            if status == "":
                if int(pre_syns) >= 2:
                    status = "Assign"
                    statusLabel = "0.5assign"
                if int(post_syns) >= 10:
                    status = "Assign"
                    statusLabel = "0.5assign"
                    
            print(bodyID + "," + bodyID + "," + pre_syns + "," + post_syns + "," + upstream + "," + downstream + "," + str(total_synweight) + "," + status + "," + statusLabel + "," + cropped + "," + instance + "," + synonyms + "," + neuronType + "," + primaryNeurite + "," + somaLocation + "," + somaRadius + "," +  bodySize + ",\"" + roiInfo_str +  "\",Segment;" + dataset + "_Segment" + is_hemibrain_Neuron + roi_booleans)
