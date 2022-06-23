# avalon

# Overview 
Avalon fingertips is a substructure fingerprint for similarity search based on 16 features of a molecule graph.
- **Input**: SMILES (what input does the model take?)
- **Output**: 1024-bit vector (what is the unit of the output?)
- **Output explanation**: Bitvector representation of a molecule (what does the output describe or mean?)
- **Threshold**: None (is there a point or range that the predict output should be guarded by?)
- **Training data**: 143,000 molecules (how many compounds or molecules, or what databases were used to train the model?)
- **Experimental validation**: No (was the model tested experimentally?)

# Source Code 
This model is published by Peter Gedeck, Bernhard Rohde, and Christian Bartels. QSAR − How Good Is It in Practice? Comparison of Descriptor Sets on an Unbiased Cross Section of Corporate Data Sets. Journal of Chemical Information and Modeling 2006 46 (5), 1924-1936 DOI: 10.1021/ci050413p
(Cite the scientific publication that explains the model)

Code: https://github.com/rdkit/rdkit/tree/master/External/AvalonTools
(Link the source code of the model)

# Specifications 
- Model is ready (what is the status of the model? Is it ready or in progress?)
- Model type is regression (does the model predict discrete output (classification) or continuous output (regression)?
- Model is pretrained (is the model based on another model (pretrained)? Or the model was trained from scratch with updated training data (retrained)?
- Model tags: fingerprint, ML, substructure

# History
- Model was downloaded on September 13, 2021 (when was the model downloaded into Ersilia?)
- Model was incorporated on September 13, 2021 (when was the model included in Ersilia?)

# License and copyright notice 
The GPL-v3 license applies to all parts of the repository that are not externally maintained libraries. This repository uses the externally maintained library "Avalon", located at /model and licensed under the BSDv3 License.
(State the original licence (if need be) and the GPLv3 licence or maintain the original licence if the licence is a copyleft licence)
