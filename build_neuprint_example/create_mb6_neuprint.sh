#!/bin/bash

# Create synapses and bodie relationship file
python ../build_neuprint_scripts/generate_Synapse_Connections_All_ftr.py data/mb6_synapse_data_example.ftr data/mb6_synapse_connections_example.ftr > All_Neuprint_Synapse_Connections_mb6.csv

# Generate Neuron downstream counts
python ../build_neuprint_scripts/detect_downstream_synapses.py All_Neuprint_Synapse_Connections_mb6.csv > downstream_synapses.csv

# Generate Neuron downstream ROIs
python ../build_neuprint_scripts/detect_downstream_roiInfo.py All_Neuprint_Synapse_Connections_mb6.csv > downstream_synapses_roiInfo.csv

# Create Synapse csv
python ../build_neuprint_scripts/generate_Neuprint_Synapses_ftr.py data/mb6_synapse_data_example.ftr mushroombody data/all_ROIs.txt > Neuprint_Synapses_mb6.csv

# Create Synapse Connections csv
python ../build_neuprint_scripts/generate_Synapse_Connections.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_Synapse_Connections_mb6.csv

# Generate Neurons connections file
python ../build_neuprint_scripts/generate_Neuron_connections.py All_Neuprint_Synapse_Connections_mb6.csv 0.5 0.5 > Neuprint_Neuron_Connections_mb6.csv

# Generate Synapse Set file
python ../build_neuprint_scripts/generate_SynapseSet_to_SynapseSet.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_SynapseSet_to_Synapses_mb6.csv

# Generate Synapse Set collection
python ../build_neuprint_scripts/generate_SynapseSets.py All_Neuprint_Synapse_Connections_mb6.csv mushroombody > Neuprint_SynapseSet_mb6.csv

# Generate Neuron to Synapse Set
python ../build_neuprint_scripts/generate_Neuron_to_SynapseSet.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_Neuron_to_SynapseSet_mb6.csv

# Generate Synapse Set to Synapse Set
python ../build_neuprint_scripts/generate_SynapseSet_to_SynapseSet.py All_Neuprint_Synapse_Connections_mb6.csv > Neuprint_SynapseSet_to_SynapseSet_mb6.csv

# Generate roiInfo, pre, post counts
python ../build_neuprint_scripts/generate_Neurons_roiInfo_ftr.py data/mb6_synapse_data_example.ftr > synapse_bodies_mb6.csv

# Generate Neurons
python ../build_neuprint_scripts/generate_Neurons_ftr.py synapse_bodies_mb6.csv data/mb6_neuron_data_example.ftr config/neurons.yaml > Neuprint_Neurons_mb6.csv

# Generate Neuprint Meta
python ../build_neuprint_scripts/generate_Neuprint_Meta_ftr.py data/mb6_synapse_data_example.ftr config/meta.yaml > Neuprint_Meta_mb6.csv
