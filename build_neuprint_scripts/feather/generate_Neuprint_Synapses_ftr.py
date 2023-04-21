#!/bin/env

# python generate_Neuprint_Synapses_csv.py synIDs_synapses-6f2cb-rois-bodyIDs.csv hemibrain > Neuprint_Synapses_6f2cb.csv
# ------------------------- imports -------------------------
import json
import sys
import os
import io
import time
import pandas as pd

if __name__ == '__main__':
    synapses_ftr = sys.argv[1]
    dataset = sys.argv[2]    
    all_rois_csv = sys.argv[3]
    
    all_rois = []
    allRoisList = open(all_rois_csv,'r')
    for line in allRoisList:
        roi_name = line.rstrip('\n')
        #print(roi_name)
        all_rois.append(roi_name)

    header = '":ID(Syn-ID)","type:string","confidence:float","location:point{srid:9157}",":Label"'

    for roi in all_rois:
        header = header + ',"' + roi + ':boolean"'

    print(header)

    syn_df = pd.read_feather(synapses_ftr)
    for index, row in syn_df.iterrows():
        #synId     x     y      z     type  confidence     roi     body
        syn_id = row["synId"]
        x = row["x"]
        y = row["y"]
        z = row["z"]
        syn_type_dvid = row["type"]
        isPre_bool = "false"
        isPost_bool = "false"
        if syn_type_dvid == "PostSyn":
            isPost_bool = "true"
            syn_type = "post"
        elif syn_type_dvid == "PreSyn":
            isPre_bool = "true"
            syn_type = "pre"

        confidence = row["confidence"]
        super_roi = str(row["roi"])
        #sub1_roi = synData[7]
        #sub2_roi = synData[8].replace("|",",")
        #sub3_roi = synData[9]
            
        location = "\"{x:" + str(x) + ", y:" + str(y) + ", z:" + str(z) + "}\""
        syn_line = str(syn_id) + "," + syn_type + "," + str(confidence) + "," + location + ",Synapse;" + dataset + "_Synapse"
        for roi_name in all_rois:
            is_roi = ""
            if roi_name == super_roi:
                is_roi = "true"
        #    if roi_name == sub1_roi:
        #        is_roi = "true"
        #    if roi_name == sub2_roi:
        #        is_roi = "true"
        #    if roi_name == sub3_roi:
        #        is_roi = "true"
            syn_line = syn_line + "," + is_roi

        print(syn_line)
