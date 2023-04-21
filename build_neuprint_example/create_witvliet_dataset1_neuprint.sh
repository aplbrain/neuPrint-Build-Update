#!/bin/bash

dataset=witvliet_dataset1
synapses=data/witvliet_dataset1_synapses_lowell.csv
connections=data/witvliet_dataset1_connections_lowell.csv
neurons=data/witvliet_dataset1_neurons_lowell.csv
all_rois=data/witvliet_dataset1_all_ROIs.txt
neurons_yaml=config/witvliet_dataset1_neurons.yaml
meta_yaml=config/witvliet_dataset1_meta.yaml

./create_neuprint.sh $dataset $synapses $connections $neurons $all_rois $neurons_yaml $meta_yaml
