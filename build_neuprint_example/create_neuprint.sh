#!/bin/bash

dataset=$1
synapses=$2
connections=$3
neurons=$4
all_rois=$5
neurons_yaml=$6
meta_yaml=$7

# Create synapses and bodie relationship file
echo 'Building connections csv'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Synapse_Connections_All_csv.py $synapses $connections > import/All_Neuprint_Synapse_Connections_$dataset.csv

# Generate Neuron downstream counts
echo 'Building downstream synapses'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/detect_downstream_synapses.py import/All_Neuprint_Synapse_Connections_$dataset.csv > import/downstream_synapses.csv

# Generate Neuron downstream ROIs
echo 'Building downstream synapse rois'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/detect_downstream_roiInfo.py import/All_Neuprint_Synapse_Connections_$dataset.csv > import/downstream_synapses_roiInfo.csv

# Create Synapse csv
echo 'Building synapses csv'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Neuprint_Synapses_csv.py $synapses $dataset $all_rois > import/Neuprint_Synapses_$dataset.csv

# Create Synapse Connections csv
echo 'Building synapse connections'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Synapse_Connections.py import/All_Neuprint_Synapse_Connections_$dataset.csv > import/Neuprint_Synapse_Connections_$dataset.csv

# Generate Neurons connections file
echo 'Building neuron connections'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Neuron_connections.py import/All_Neuprint_Synapse_Connections_$dataset.csv 0.5 0.5 > import/Neuprint_Neuron_Connections_$dataset.csv

# Generate Synapse Set file
echo 'Building synapse sets on synapses'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_SynapseSet_to_SynapseSet.py import/All_Neuprint_Synapse_Connections_$dataset.csv > import/Neuprint_SynapseSet_to_Synapses_$dataset.csv

# Generate Synapse Set collection
echo 'Building synapse sets'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_SynapseSets.py import/All_Neuprint_Synapse_Connections_$dataset.csv $dataset > import/Neuprint_SynapseSet_$dataset.csv

# Generate Neuron to Synapse Set
echo 'Building neuron to synapsesets'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Neuron_to_SynapseSet.py import/All_Neuprint_Synapse_Connections_$dataset.csv > import/Neuprint_Neuron_to_SynapseSet_$dataset.csv

# Generate Synapse Set to Synapse Set
echo 'Building synapsesets to synapsesets'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_SynapseSet_to_SynapseSet.py import/All_Neuprint_Synapse_Connections_$dataset.csv > import/Neuprint_SynapseSet_to_SynapseSet_$dataset.csv

# Generate roiInfo, pre, post counts
echo 'Building roi info'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Neurons_roiInfo_csv.py $synapses > import/synapse_bodies_$dataset.csv

# Generate Neurons
echo 'Building neuron csv'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Neurons_csv.py import/synapse_bodies_$dataset.csv $neurons $neurons_yaml > import/Neuprint_Neurons_$dataset.csv

# Generate Neuprint Meta
echo 'Building metadata csv'
python3 /home/ubuntu/neuPrint-Build-Update/build_neuprint_scripts/csv/generate_Neuprint_Meta_csv.py $synapses $meta_yaml > import/Neuprint_Meta_$dataset.csv
