#!/bin/bash

# Create synapses and bodie relationship file
echo 'Building connections csv'
python3 ../build_neuprint_scripts/csv/generate_Synapse_Connections_All_csv.py data/mb6_synapse_data_example.csv data/mb6_synapse_connections_example.csv > All_Neuprint_Synapse_Connections_mb6.csv

# Generate Neuron downstream counts
echo 'Building downstream synapses'
python3 ../build_neuprint_scripts/csv/detect_downstream_synapses.py All_Neuprint_Synapse_Connections_mb6.csv > downstream_synapses.csv

# Generate Neuron downstream ROIs
echo 'Building downstream synapse rois'
python3 ../build_neuprint_scripts/csv/detect_downstream_roiInfo.py All_Neuprint_Synapse_Connections_mb6.csv > downstream_synapses_roiInfo.csv

# Create Synapse csv
echo 'Building synapses csv'
python3 ../build_neuprint_scripts/csv/generate_Neuprint_Synapses_csv.py data/mb6_synapse_data_example.csv mushroombody data/all_ROIs.txt > Neuprint_Synapses_mb6.csv

# Create Synapse Connections csv
echo 'Building synapse connections'
python3 ../build_neuprint_scripts/csv/generate_Synapse_Connections.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_Synapse_Connections_mb6.csv

# Generate Neurons connections file
echo 'Building neuron connections'
python3 ../build_neuprint_scripts/csv/generate_Neuron_connections.py All_Neuprint_Synapse_Connections_mb6.csv 0.5 0.5 > Neuprint_Neuron_Connections_mb6.csv

# Generate Synapse Set file
echo 'Building synapse sets on synapses'
python3 ../build_neuprint_scripts/csv/generate_SynapseSet_to_SynapseSet.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_SynapseSet_to_Synapses_mb6.csv

# Generate Synapse Set collection
echo 'Building synapse sets'
python3 ../build_neuprint_scripts/csv/generate_SynapseSets.py All_Neuprint_Synapse_Connections_mb6.csv mushroombody > Neuprint_SynapseSet_mb6.csv

# Generate Neuron to Synapse Set
echo 'Building neuron to synapsesets'
python3 ../build_neuprint_scripts/csv/generate_Neuron_to_SynapseSet.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_Neuron_to_SynapseSet_mb6.csv

# Generate Synapse Set to Synapse Set
echo 'Building synapsesets to synapsesets'
python3 ../build_neuprint_scripts/csv/generate_SynapseSet_to_SynapseSet.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_SynapseSet_to_SynapseSet_mb6.csv

# Generate roiInfo, pre, post counts
echo 'Building roi info'
python3 ../build_neuprint_scripts/csv/generate_Neurons_roiInfo_csv.py data/mb6_synapse_data_example.csv > synapse_bodies_mb6.csv

# Generate Neurons
echo 'Building neuron csv'
python3 ../build_neuprint_scripts/csv/generate_Neurons_csv.py synapse_bodies_mb6.csv data/mb6_neuron_data_example.csv config/neurons.yaml > Neuprint_Neurons_mb6.csv

# Generate Neuprint Meta
echo 'Building metadata csv'
python3 ../build_neuprint_scripts/csv/generate_Neuprint_Meta_csv.py data/mb6_synapse_data_example.csv config/meta.yaml > Neuprint_Meta_mb6.csv
