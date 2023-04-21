## Steps to ingest a dataset to NeuPrint

First, these ingest scripts expect a certain schema. Here are the columns for the 3 csv's.

neurons.csv:
| body | name | statusLabel | type | cropped | instance | size |
|---|---|---|---|---|---|---|

synapses.csv:
| body | x | y | z | type | confidence | roi | sub1_roi | sub2_roi | synId |
|---|---|---|---|---|---|---|---|---|---|

connections.csv:
| synId_pre | synId_post |
|---|---|

Additionally, there are 4 json files for ROIs, 1 json file for neuroglancer settings if neuroglancer will be integrated, and 2 yaml files for dataset metadata and neuron metadata. An example for each of these files lies in build_neuprint_example/data and build_neuprint_example/config.

Once these files have been generated for the new dataset, make a copy of `build_neuprint_examples/create_witvliet_dataset1_neuprint.sh` and fill in the appropriate file paths. Then, run the new script. This will convert the input files into a format the neo4j-admin can ingest.

Next, run `sudo ./neo4j_3_5_import.sh <dataset_name>`. This will ingest the dataset as a graph.db, then copy it into its own directory.

Finally, add a new neo4j container to the swarm file. Mount the db to a volume within the new container using `/var/lib/neo4j/data/<dataset_name>:/data:rw`.

