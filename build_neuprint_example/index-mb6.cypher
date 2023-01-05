CREATE INDEX  ON :mushroombody_Segment(`alpha1`);
CREATE INDEX  ON :mushroombody_Segment(`alpha2`);
CREATE INDEX  ON :mushroombody_Segment(`alpha3`);
CREATE INDEX  ON :mushroombody_Segment(`cropped`);
CREATE INDEX  ON :mushroombody_Segment(`instance`);
CREATE INDEX  ON :mushroombody_Segment(`name`);
CREATE INDEX  ON :mushroombody_Segment(`notes`);
CREATE INDEX  ON :mushroombody_Segment(`post`);
CREATE INDEX  ON :mushroombody_Segment(`pre`);
CREATE INDEX  ON :mushroombody_Segment(`somaLocation`);
CREATE INDEX  ON :mushroombody_Segment(`status`);
CREATE INDEX  ON :mushroombody_Segment(`statusLabel`);
CREATE INDEX  ON :mushroombody_Segment(`type`);


CREATE INDEX  ON :mushroombody_Neuron(`alpha1`);
CREATE INDEX  ON :mushroombody_Neuron(`alpha2`);
CREATE INDEX  ON :mushroombody_Neuron(`alpha3`);
CREATE INDEX  ON :mushroombody_Neuron(`cropped`);
CREATE INDEX  ON :mushroombody_Neuron(`instance`);
CREATE INDEX  ON :mushroombody_Neuron(`name`);
CREATE INDEX  ON :mushroombody_Neuron(`notes`);
CREATE INDEX  ON :mushroombody_Neuron(`post`);
CREATE INDEX  ON :mushroombody_Neuron(`pre`);
CREATE INDEX  ON :mushroombody_Neuron(`somaLocation`);
CREATE INDEX  ON :mushroombody_Neuron(`status`);
CREATE INDEX  ON :mushroombody_Neuron(`statusLabel`);
CREATE INDEX  ON :mushroombody_Neuron(`type`);

CREATE INDEX  ON :mushroombody_Cell(`alpha1`);
CREATE INDEX  ON :mushroombody_Cell(`alpha2`);
CREATE INDEX  ON :mushroombody_Cell(`alpha3`);
CREATE INDEX  ON :mushroombody_Cell(`cropped`);
CREATE INDEX  ON :mushroombody_Cell(`instance`);
CREATE INDEX  ON :mushroombody_Cell(`name`);
CREATE INDEX  ON :mushroombody_Cell(`notes`);
CREATE INDEX  ON :mushroombody_Cell(`post`);
CREATE INDEX  ON :mushroombody_Cell(`pre`);
CREATE INDEX  ON :mushroombody_Cell(`somaLocation`);
CREATE INDEX  ON :mushroombody_Cell(`status`);
CREATE INDEX  ON :mushroombody_Cell(`statusLabel`);
CREATE INDEX  ON :mushroombody_Cell(`type`);

CREATE INDEX  ON :mushroombody_Synapse(`location`);
CREATE INDEX  ON :mushroombody_Element(`location`);

CREATE INDEX  ON :Segment(`type`);
CREATE INDEX  ON :Neuron(`type`);
CREATE INDEX  ON :Cell(`type`);
CREATE INDEX  ON :Synapse(`type`);
CREATE INDEX  ON :Element(`type`);

CREATE CONSTRAINT ON ( datamodel:DataModel ) ASSERT datamodel.dataModelVersion IS UNIQUE;
CREATE CONSTRAINT ON ( mushroombodysegment:mushroombody_Segment ) ASSERT mushroombodysegment.bodyId IS UNIQUE;
CREATE CONSTRAINT ON ( mushroombodyneuron:mushroombody_Neuron ) ASSERT mushroombodyneuron.bodyId IS UNIQUE;
CREATE CONSTRAINT ON ( mushroombodycell:mushroombody_Cell ) ASSERT mushroombodycell.bodyId IS UNIQUE;
CREATE CONSTRAINT ON ( mushroombodysegment:mushroombody_Segment ) ASSERT mushroombodysegment.mutationUuidAndId IS UNIQUE;
CREATE CONSTRAINT ON ( mushroombodysynapse:Synapse ) ASSERT mushroombodysynapse.location IS UNIQUE;
