# Ersilia Model Template

This README contains the instructions to incorporate a model. Please follow along to bring your model into the Ersilia Model Hub. After successful incorporation of the model, this README will be automatically updated to reflect model specific details.
Further information can be found in our [Documentation](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/).

## Folder Structure

Generally, two important pieces make up a model that goes into the hub: the model checkpoints and the code to load and make predictions with that model. With that in mind, the model folder is organised as follows:

```
└── model
    ├── checkpoints
    │   └── README.md
    └── framework
        ├── README.md
        ├── code
        │   └── main.py
        ├── examples
        │   ├── run_input.csv
        │   └── run_output.csv
        ├── columns
            └── run_columns.csv
        └── run.sh
```
- `model/checkpoints` contains checkpoint files required by the model
- `model/framework` contains the driver code to load the model and run inferences from it. There are two files of interest here: `main.py`, and `run.sh`. The `main.py` file will contain the driver code to load model checkpoints and call its prediction API, while `run.sh` serves two purposes, it runs the code in the `main.py` file and also tells Ersilia that this model server will have a `run` API.
- `model/framework/examples` contains an example input file (should have three smiles under the header smiles, this file can be generated with the `ersilia example` command) and the output of running the `run.sh` on the example inputs.
- `model/framework/columns` contains a template of the expected output columns, indicating their name, type (float, integer or string), direction (high,low) and a short one-sentence description. For more rules on how to fill in this file, check our [Documentation](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/model-template).

## Changes to templated files

In addition to adding the model checkpoints, the code for running them and the example and columns file, you'll need to edit the following:

### Dependencies

To specify dependencies for this model, use the `install.yml` file to populate all the necessary dependencies required by the model to successfully run. This dependency configuration file has two top level keys:

- `python` which expects a string value denoting a python version (eg `"3.12"`)
- `commands` which expects a list of values, each of which is a list on its own, denoting the dependencies required by the model. Currently, `pip` and `conda` dependencies are supported. 
- `pip` dependencies are expected to be one of the following lists:
    -  Versioned dependency: three element lists in the format `["pip", "library", "version"]`
    - Versioned dependency with additional flags: five element lists in the format `["pip", "library", "version", "--index-url", "URL"]`
    - VCS-based dependency: four element lists in the format `['pip', 'git', 'URL', 'commit_sha']`
- `conda` dependencies are expected to be four element lists in the format `["conda", "library", "version", "channel"]`, where channel is the conda channel to install the required library.

The installation parser will raise an exception if dependencies are not specified in the aforementioned format.


### Model Metadata

Model metadata should be specified within metadata.yml. A detailed explanation of what the metadata fields correspond to can be found [here](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/incorporate-models/model-template). Note that some fields will be automatically updated upon model incorporation in Ersilia.

### Dockerignore
This file will mark the files not needed in the Docker image of the model. By definition, the .git folder is ignored. Other files to be ignored could include training data of the model (which will be available in GitHub and S3 but is not needed to run the model image). This is devised to reduce the final size of the images.

### README file
Please do not make any changes to this README file. It will automatically be updated when the model is incorporated in the Ersilia Model Hub.
