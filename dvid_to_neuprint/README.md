DVID to neuPrint
=====
Scripts used to export synapse, neurons, neuron connections

## Prerequisite Python Libraries
To run these scripts you will need to install the following python packages:

* [neuclease](https://github.com/stuarteberg/neuclease)
* [libdvid-cpp](https://github.com/janelia-flyem/libdvid-cpp)
* [pandas](https://pandas.pydata.org/)
* [numpy](https://numpy.org/)
* [tqdm](https://github.com/tqdm/tqdm)

## Examples
How to create synapses and synapse partners feather files (synapses.ftr and synapse_partners.ftr) from DVID source.
```
python export_dvid_synapses.py emdata5-private.janelia.org:8510 45d61 synapses segmentation all_ROIs.txt
```

How to create neurons feather files (neurons.ftr) from DVID source.
```
python export_dvid_neurons.py emdata5-private.janelia.org:8510 45d61 segmentation segmentation_annotations synapses_45d61.ftr
```




