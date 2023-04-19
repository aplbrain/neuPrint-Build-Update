#!/bin/env
# ------------------------- imports -------------------------
import json
import sys
import os
import io
import time
import numpy as np
import pandas as pd

if __name__ == '__main__':
    synapses_ftr = sys.argv[1]
    synapse_partners_ftr = sys.argv[2]
    
    synapse_body_lookup = {}
    synapse_confidence = {}
    synapse_roi = {}
    synapse_coords = {}
    #synapse_ids = {}

    syn_df = pd.read_feather(synapses_ftr)
    for index, row in syn_df.iterrows():
        #synId     x     y      z     type  confidence     roi     body
        #print(row['synId'],row['body'])
        x = row["x"]
        y = row["y"]
        z = row["z"]
        confidence = row["confidence"]
        roi = row["roi"]
        bodyID = row["body"]
        synapse_coord = str(x) + "," + str(y) + "," + str(z)
        synID = row["synId"]
        synapse_body_lookup[synID] = bodyID
        synapse_confidence[synID] = confidence
        synapse_roi[synID] = roi
        synapse_coords[synID] = synapse_coord
        #synapse_sub1_roi[synapse_key] = sub1_roi
        #synapse_sub2_roi[synapse_key] = sub2_roi
        #synapse_sub3_roi[synapse_key] = sub3_roi
            
    print("from_synId,from_x,from_y,from_z,from_conf,from_super_roi,from_sub1_roi,from_sub2_roi,from_sub3_roi,from_bodyId,connection,to_synId,to_x,to_y,to_z,to_conf,to_super_roi,to_sub1_roi,to_sub2_roi,to_sub3_roi,to_bodyId")

    rel_df = pd.read_feather(synapse_partners_ftr)
    
    
    for index, row in rel_df.iterrows():        
        #pre_id,z_pre,y_pre,x_pre,kind_pre,conf_pre,user_pre,post_id,z_post,y_post,x_post,kind_post,conf_post,user_post
        from_bodyId = "0"
        from_super_roi = ""
        from_sub1_roi = ""
        from_sub2_roi = ""
        from_sub3_roi = ""
        from_conf = ""
        kind = "PreSynTo"
        from_synId = row["synId_pre"]
        if from_synId in synapse_confidence:
            from_conf = str(synapse_confidence[from_synId])
        from_coord = synapse_coords[from_synId]
        coord_data1 = from_coord.split(',')        
        from_x = coord_data1[0]
        from_y = coord_data1[1]
        from_z = coord_data1[2]
        if from_synId in synapse_body_lookup:
            from_bodyId = str(synapse_body_lookup[from_synId])
        if from_synId in synapse_roi:
            from_super_roi = synapse_roi[from_synId]    
            if from_super_roi is None:
                from_super_roi = ""
            
        to_bodyId = "0"
        to_super_roi = ""
        to_sub1_roi = ""
        to_sub2_roi = ""
        to_sub3_roi = ""
        to_conf = ""
        to_synId = row["synId_post"]
        if to_synId in synapse_confidence:
            to_conf = str(synapse_confidence[to_synId])
        to_coord = synapse_coords[to_synId]
        coord_data2 = to_coord.split(',')
        to_x = coord_data2[0]
        to_y = coord_data2[1]
        to_z = coord_data2[2]
        if to_synId in synapse_body_lookup:
            to_bodyId = str(synapse_body_lookup[to_synId])
        if to_synId in synapse_roi:
            to_super_roi = synapse_roi[to_synId]        
            if to_super_roi is None:
                to_super_roi = ""
                
        connection = "PreSynTo"
        #print(from_super_roi + ",")
        #print(str(from_synId) + "," + from_x + "," + from_y + "," + from_z + ","  + from_conf + "," + from_super_roi + "," + from_sub1_roi + "," + from_sub2_roi + "," + from_sub3_roi + "," + from_bodyId + "," + connection)
        print(str(from_synId) + "," + from_x + "," + from_y + "," + from_z + ","  + from_conf + "," + from_super_roi + "," + from_sub1_roi + "," + from_sub2_roi + "," + from_sub3_roi + "," + from_bodyId + "," + connection + "," + str(to_synId) + "," + to_x + "," + to_y + "," + to_z + "," + to_conf + "," + to_super_roi + "," + to_sub1_roi + "," + to_sub2_roi + "," + to_sub3_roi + "," + to_bodyId)
            
