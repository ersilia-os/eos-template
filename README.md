# avalon

# Overview 
Avalon fingertips is a substructure fingerprint for similarity search based on 16 features of a molecule graph.
- **Input**: SMILES
- **Output**: 1024-bit vector
- **Output explanation**: Bitvector representation of a molecule 
- **Threshold**: None
- **Training data**: 143,000 molecules 
- **Experimental validation**: No

# Source Code 
This model is published by Peter Gedeck, Bernhard Rohde, and Christian Bartels. QSAR − How Good Is It in Practice? Comparison of Descriptor Sets on an Unbiased Cross Section of Corporate Data Sets. Journal of Chemical Information and Modeling 2006 46 (5), 1924-1936 DOI: 10.1021/ci050413p

Code: https://github.com/rdkit/rdkit/tree/master/External/AvalonTools

# Specifications 
- Model is ready
- Model type is regression
- Model is pretrained
- Model tags: fingerprint, ML, substructure

# History
- Model was downloaded on September 13, 2021
- Model was incorporated on September 13, 2021

# License and copyright notice 
The GPL-v3 license applies to all parts of the repository that are not externally maintained libraries. This repository uses the externally maintained library "Avalon", located at /model and licensed under the BSDv3 License.
