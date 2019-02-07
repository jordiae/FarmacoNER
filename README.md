# FarmacoNER

FarmacoNER is a Neural Named Entity Recognition program based on NeuroNER (https://github.com/Franck-Dernoncourt/NeuroNER). The project was developed during my research internship at the Text Mining group of the Barcelona Supercomputing Center.

The following features have been added to NeuroNER:
- POS tags.
- Gazetteer features.

In order to adapt NeuroNER to the domain of Spanish medical texts, the following steps have been applied:
- Applying the SPACC POS Tagger to the text files.
- Building a gazetteer based on a pharmaceutical nomenclator maintained by the Spanish government.
- Trying 8 different token embeddings, both generic and domain-specific.

In order to adapt NeuroNER to the particular task of detecting PROTEINAS, NORMALIZABLES, NO-NORMALIZABLES and UNCLEAR entities the following steps have been applied:
- Since the original dataset was small, data augmentation with datasets from UMLS and Mantra corpus has been applied.
- Since the original dataset was heavily imbalanced, stratified splitting and oversampling have been applied.

In order to adapt NeuroNER to HPC, it had to be installed to the BSC HPC clusters with a virtual environment. Both GPU and CPU based computing was tried. The performance with CPUs was much higher because of the batch size of NeuroNER. The most efficient number of cores was investigated.

Different experiments have been conducted. The results will be published.
