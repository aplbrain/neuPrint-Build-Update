#!/bin/env

import os
import sys
import logging
import json
import requests
from tqdm import trange
#from tqdm import tqdm_notebook
#tqdm = tqdm_notebook

import numpy as np
import pandas as pd
from neuclease.util import compute_parallel, read_csv_col
from neuclease.dvid import find_master, fetch_sizes, fetch_keys, fetch_keyvalues

server = sys.argv[1]
uuid = sys.argv[2]
segmentation = sys.argv[3]
neuron_dvid = sys.argv[4]
synapses_ftr = sys.argv[5]

master = (server, uuid)

syn_df = pd.read_feather(synapses_ftr)
#synId     x     y      z     type  confidence     roi     body
body_list = syn_df['body'].tolist()
#print(len(body_list))
uniq_body_list = list(set(body_list))
#print(len(uniq_body_list))

# get sizes for all the bodies

master_seg = (server, uuid, segmentation)
body_groups = []
body_count = 0
group_list = []
for bodyid in uniq_body_list:
    group_list.append(bodyid)
    body_count += 1
    if body_count == 1000:
        body_groups.append(group_list)
        group_list = []
        body_count = 0

if len(group_list) > 0:
    body_groups.append(group_list)

PROCESSES = 15
def get_sizes(label_ids):
    try:
        sizes_pd = fetch_sizes(*master_seg, label_ids, supervoxels=False)
    except HTTPError:
        s_empty_pd = pd.Series(index=label_ids, data=-1, dtype=int)
        s_empty_pd.name = 'size'
        s_empty_pd.index.name = 'body'
        return(s_empty_pd)
    else:
        return(sizes_pd)

body_sizes_df_list = compute_parallel(get_sizes, body_groups, chunksize=100, processes=PROCESSES, ordered=False)

body_sizes_pd = pd.concat(body_sizes_df_list)

body_sizes_dict = body_sizes_pd.to_dict()

#print(body_sizes_dict)

# get all body annotations as dict

node = (server, uuid)

all_keys = fetch_keys(*node, neuron_dvid)

all_values = {}
for start in trange(0,100_000,100_000): # head
    values = fetch_keyvalues(*node, neuron_dvid, all_keys[start:start+100_000], as_json=True)
    all_values.update(values)

count = 0
all_neurons = {}
for bodyid in body_sizes_dict:
    size = body_sizes_dict[bodyid]
    neuron_type = None
    instance = None
    cropped = None
    status = None

    if str(bodyid) in all_values:
        body_annot = all_values[str(bodyid)]
        #print(bodyid, body_annot, size)
        if 'class' in body_annot:
            neuron_type = body_annot['class']
        if 'type' in body_annot:
            neuron_type = body_annot['type']
        if 'status' in body_annot:
            status = body_annot['status']
            if status == 'Leaves':
                cropped = "true"
        if 'name' in body_annot:
            instance = body_annot['name']
        if 'instance' in body_annot:
            instance = body_annot['instance']
    body_annot = {}
    body_annot['body'] = bodyid
    body_annot['statusLabel'] = status
    body_annot['cropped'] = cropped
    body_annot['instance'] =instance
    body_annot['type'] = neuron_type
    body_annot['size'] = size
    all_neurons[count] = body_annot
    #print(bodyid, status, neuron_type, instance, cropped,  size)
    count += 1

#print(all_neurons)
neurons_df = pd.DataFrame(all_neurons).transpose()

print(neurons_df)

neurons_ftr = "neurons_" + uuid + ".ftr"
neurons_df.to_feather(neurons_ftr)
