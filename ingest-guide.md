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

Additionally, there are 4 json files for ROIs, 1 json file for neuroglancer settings if neuroglancer will be integrated, and 2 yaml files for dataset metadata and neuron metadata. An example for each of these files lies in `build_neuprint_example/data` and `build_neuprint_example/config`.

_Witvliet note:_
In the witvliet folder, `python witvliet_ingest_script.py -n dataset_no` can generate these files in a new directory with the dataset's title, using a number of files that have been compiled for the witvliet datasets. Note that there are a few metadata parameters which must be changed in the script before running.
(This script has been committed to [user-scratch](https://github.com/aplmicrons/user-scratch/blob/master/neuprint/witvliet/witvliet_ingest_script.py) to keep this repo fairly dataset agnostic.)

Run `./create_neuprint.sh <dataset_name>`. This will convert the input files into a format the neo4j-admin can ingest.

Next, run `sudo ./neo4j_3_5_import.sh <dataset_name>`. This will ingest the dataset as a graph.db, then copy it into its own directory.

Finally, edit the production configuration file. First, add a new neo4j container to neuprint-swarm.yaml. Mount the db to a volume within the new container using `/var/lib/neo4j/data/<dataset_name>:/data:rw`. Second, add a new alternative database to config/config.json.

To update prod with the new dataset, run the following commands:

`docker stack deploy -c neuprint-swarm.yml neuprint`

`docker service scale neuprint_neuprinthttp=0`

`docker service scale neuprint_neuprinthttp=1`
