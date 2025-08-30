# Ersilia Model Template

This document contains the instructions to incorporate a model. Please follow along to bring your model into the [Ersilia Model Hub](https://github.com/ersilia-os/ersilia). After successful incorporation of the model, this README file will be **automatically updated** to reflect model specific details.

Further information about model incorporation can be found in our [Documentation](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/).

## Template Structure

The model template is organized in two parts, namely the (a) model code and parameters, and (b) the metadata and installation instructions

### The Model Folder

Generally, two important pieces make up a model that goes into the Ersilia Model Hub: (a) the model checkpoints and (b) the code to load those checkpoints and make predictions with that model (framework). With that in mind, the model folder is organised as follows:

```
└── model
    ├── checkpoints
    │   └── .gitkeep
    └── framework
        ├── code
        │   └── main.py
        ├── examples
        │   ├── run_input.csv
        │   └── run_output.csv
        ├── columns
            └── run_columns.csv
        └── run.sh
```
- `model/checkpoints` contains checkpoint files required by the model. This directory is optional.
- `model/framework` contains the driver code to load the model and run inferences from it. There are two files of interest here: `code/main.py`, and `run.sh`. The `code/main.py` file will contain the primary code to load model checkpoints and run the model, and can obviously refer to other files and packages contained within the `code` directory. The `run.sh` serves two purposes, it runs the code in the `main.py` file and also tells Ersilia that this model server will have a `run` API. The `run.sh` file is mandatory while the `code/main.py` is optional.
- `model/framework/examples` contains an example input file (should have three smiles under the header smiles, this file can be generated with the `ersilia example` command) and the output of running the `run.sh` on the example inputs. Both `run_input.csv` and `run_output.csv` are mandatory.
- `model/framework/columns` contains a template of the expected output columns, indicating their name, type (float, integer or string), direction (high, low, or empty) and a short one-sentence description. For more rules on how to fill in this file, check our [documentation](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/model-template). The `run_columns.csv` file is mandatory.

### Metadata, Installation, and Other Templated Files

In addition to adding the model checkpoints, the code for running them and the example and columns file, you'll need to edit the following:

#### Model Dependencies

Use the `install.yml` file to specify all the necessary dependencies required by the model to successfully run. This dependency configuration file has two top level keys:

- The `python` field expects a string value denoting a python version (e.g. `"3.12"`)
- The `commands` field expects a list of values, each of which is a list on its own, denoting the dependencies required by the model. Currently, `pip` and `conda` dependencies are supported using this syntax. 
    - `pip` dependencies are expected to be one of the following lists:
        -  Versioned dependency: three element lists in the format `["pip", "library", "version"]`
        - Versioned dependency with additional flags: five element lists in the format `["pip", "library", "version", "--index-url", "URL"]`
        - VCS-based dependency: four element lists in the format `['pip', 'URL']`. E.g `["pip", "git+https://github.com/bp-kelley/descriptastorus.git@9a190343bcd3cfd35142d378d952613bcac40797"]`.
    - `conda` dependencies are expected to be four element lists in the format `["conda", "library", "version", "channel"]`, where channel is the conda channel to install the required library.
    - For other `bash` commands, simply specify them as a oneliner string.

The installation parser will raise an exception if dependencies are not specified in the aforementioned format.

#### Model Metadata

Model metadata should be specified within `metadata.yml`. A detailed explanation of what the metadata fields correspond to can be found [here](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/incorporate-models/model-template). Note that some fields will be automatically updated upon model incorporation in Ersilia.

#### Other Relevant Files

* The `.dockerignore` file can be used to specify which files and folders should not be included in the eventual Docker image. By default, the `.git` folder is ignored. Other files to be ignored could include training data of the model, which will be available in GitHub and S3 but is not needed to run the model image. This is devised to reduce the final size of the images.

* Consider adding a `.gitattributes` file if your model contains large files. In this file, you can specify which files should be handled with [Git LFS](https://git-lfs.com/).

* As you work with the model, use the `.gitignore` file appropriately to ensure that only relevant files are included in the model repository.

* As mentioned above, the `README.md` file **should not be modified**. It will automatically be updated when the model is incorporated in the Ersilia Model Hub.
