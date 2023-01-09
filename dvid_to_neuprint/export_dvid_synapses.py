#!/bin/env

import os
import sys
import logging
import json
import requests
from tqdm import tqdm_notebook
tqdm = tqdm_notebook

import numpy as np
import pandas as pd
from neuclease.dvid import find_master, fetch_synapses_in_batches, fetch_labels_batched, fetch_combined_roi_volume
from neuclease.util import extract_labels_from_volume

#example: python export_dvid_synapses.py emdata5-private.janelia.org:8510 52356 synapses segmentation
server = sys.argv[1]
uuid = sys.argv[2]
annotation = sys.argv[3]
segmentation_inst = sys.argv[4]
all_rois_file = sys.argv[5]

rois = []

rois_list = open(all_rois_file,'r')
for line in rois_list:
    roi_name = line.rstrip('\n')
    rois.append(roi_name)

master = (server, uuid)

#box_zyx = [(16000,16000,16000), (17024,17024,17024)]
#box_zyx = [(0,0,0), (11840,8064,12160)]
#box_zyx = [(0,0,0), (11456,9600,13248)]
#box_zyx = [(0,0,0), (18533,10785,22516)]
#box_zyx = [(0,0,0), (64000,76800,96000)]
#box_zyx = [(896,1792,0), (41408,39552,34432)]

# get as pandas dataframe
#synapses_df, partners_df = fetch_synapses_in_batches(*master, annotation, box_zyx, format='pandas')
synapses_df, partners_df = fetch_synapses_in_batches(*master, annotation, format='pandas')
synapses_df.rename(columns={'kind': 'type'}, inplace=True)
partners_df.rename(columns={'pre_id': 'synId_pre', 'post_id': 'synId_post'}, inplace=True)
#partners_df.reset_index(inplace=True)
print(partners_df)

# export partners_df as ftr
partners_ftr = "synapse_partners_" + uuid + ".ftr" 
partners_df.reset_index().to_feather(partners_ftr)

syn_ids = []
syn_count = 0
for index, row in synapses_df.iterrows():
    #syn_count += 1
    #syn_id = 99000000000 + syn_count
    syn_ids.append(int(index))
    #print(index,syn_id)
    
synapses_df['synId'] = syn_ids
#print(synapses_df)
master_seg = (server, uuid, segmentation_inst)

labels = fetch_labels_batched(*master_seg, synapses_df[['z', 'y', 'x']].values, threads=32)
synapses_df['body'] = labels
synapses_df.reset_index(drop=True, inplace=True)

# Map synapses to rois
rois = { roi_name: label for label, roi_name in enumerate(rois, start=1) }
print(rois)
roi_vol, box, overlaps = fetch_combined_roi_volume(*master, rois, box_zyx=[(0,0,0), None])

#from neuclease.dvid import load_synapses_csv
#synapse_csv = sys.argv[3]
#synapses_df = load_synapses_csv(synapse_csv)
#print(f"Loaded {len(synapses_df)} points")
extract_labels_from_volume(synapses_df, roi_vol, vol_scale=5, label_names=rois)

synapses_df.rename(columns={'label_name': 'roi'}, inplace=True)

synapses_df['roi'] = synapses_df['roi'].replace(['<unspecified>'], '')

print(synapses_df)

synapses_ftr = "synapses_" + uuid + ".ftr"
synapses_df.to_feather(synapses_ftr)


