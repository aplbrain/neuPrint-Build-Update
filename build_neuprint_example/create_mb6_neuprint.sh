#!/bin/bash

dataset=mb6
synapses=data/mb6_synapse_data_example.csv
connections=data/mb6_synapse_connections_example.csv
neurons=data/mb6_neuron_data_example.csv
all_rois=data/all_ROIs.txt
neurons_yaml=data/neurons.yaml
meta_yaml=data/meta.yaml

./create_neuprint.sh $dataset $synapses $connections $neurons $all_rois $neurons_yaml $meta_yaml
