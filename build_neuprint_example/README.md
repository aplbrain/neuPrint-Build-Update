Create neuPrint from flat files (feather) using mushroombody (MB6) as an example
=====
An example of the data and format you data needs to be in to import your connectome data into a neuprint neo4j database

## Prerequisite Python Libraries
To run these scripts you will need to install the following python packages and Python 3.7 or greater::
* [pandas](https://pandas.pydata.org/)

## Example feather (ftr) files for mushroombody (MB6)
* mb6_synapse_data_example.ftr - synapses data which includes unique synapse ID (synId), synapse coordinate location (x,y,z), synapse type (type), synapse confidence (confidence), segmentation/body mapping (body)
```
              synId     x     y      z     type  confidence     roi     body
0       99000000001  3966  6940   1341  PostSyn         1.0  alpha3  6716266
1       99000000002  3987  6935   1341   PreSyn         1.0  alpha3   113556
2       99000000003  3989  6962   1341  PostSyn         1.0  alpha3        2
3       99000000004  4058  7063   1301   PreSyn         1.0  alpha3    75040
4       99000000005  4053  7083   1301  PostSyn         1.0  alpha3   352987
...             ...   ...   ...    ...      ...         ...     ...      ...
317981  99000317982  4148  4334  13195  PostSyn         1.0  alpha1        0
317982  99000317983  4143  4322  13189  PostSyn         1.0  alpha1        0
317983  99000317984  4158  4349  13190  PostSyn         1.0  alpha1        0
317984  99000317985  4147  4322  13203   PreSyn         1.0  alpha1        0
317985  99000317986  4144  4355  13185   PreSyn         1.0  alpha1        0
```

* mb6_synapse_connections_example.ftr - defines all synapse relationship from pre (synId_pre) to post (synId_post)
```
          synId_pre   synId_post
0       99000000002  99000000001
1       99000000002  99000000003
2       99000000002  99000000058
3       99000000004  99000000008
4       99000000004  99000000005
...             ...          ...
226547  99000317985  99000317983
226548  99000317985  99000317979
226549  99000317985  99000317984
226550  99000317986  99000317981
226551  99000317986  99000317982
```

* mb6_neuron_data_example.ftr - neuron annotation/properties data. unique neuron ID (body), neuron annotation status (statusLabel), is neuron truncated (cropped), neuron name (instance), neuron class or type (type), neuron size ex. voxels (size)
```
          body     statusLabel cropped instance    type        size
0      6716266  Roughly traced    None     KC-s    KC-s    18996810
1       113556  Roughly traced    None     KC-s    KC-s    26334586
2            2  Roughly traced    None   MB-APL  MB-APL  1060865319
3        75040  Roughly traced    None     KC-s    KC-s    28280828
4       352987  Roughly traced    None     KC-s    KC-s    23431792
...        ...             ...     ...      ...     ...         ...
7759  17144796            None    None     None    None       13103
7760  17145055            None    None     None    None         733
7761  17143968            None    None     None    None        5019
7762  17143713            None    None     None    None        2015
7763  17144961            None    None     None    None      219314
```

## Create csv neuprint files



## Build neo4j database
Run either of these shell scripts that will generate the neo4j-admin command line that defines the nodes and relationships for neuprint and build the database.
```
# use this if using neo4j 3.5 or greater
./neo4j_3_5_import.sh mb6
```

```
# use this shell script if using neo4j 4.4 or greater
./neo4j_4_4_import.sh mb6
```

After building the neo4j neuprint database, launch the database in neo4j. Next you will need to build the indices and warmup the page cache by running these commands with the supplied cypher.
```
cat index-mb6.cypher | ./bin/cypher-shell -u neo4j  --format plain
cat warmup-cache.cypher | ./bin/cypher-shell -u neo4j  --format plain
```