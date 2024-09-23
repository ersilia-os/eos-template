# Ersilia Model Contribution

This README contains the instructions to incorporate a model. Please follow along to bring your model into the Ersilia Model Hub. After successful incorporation of the model, this README will be automatically updated to reflect model specific details.

## Folder Structure

Generally, two important pieces make up a model that goes into the hub: the model checkpoints, and the code to load and make predictions with that model. With that in mind, the model folder is organised as follows:

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
        └── run.sh
```

- `model/checkpoints` contains checkpoint files required by the model
- `model/framework` contains the driver code to load the model and run inferences from it. There are two files of interest here: `main.py`, and `run.sh`. The `main.py` file will contain the driver code to load model checkpoints and call its prediction API, while `run.sh` serves two purposes, it runs the code in the `main.py` file and also tells Ersilia that this model server will have a `run` API.

## Specifying Dependencies

To specify dependencies for this model, use the `install.yml` file to populate all the necessary dependencies required by the model to successfully run. This dependency configuration file has two top level keys:

- `python` which expects a string value denoting a python version (eg `"3.10"`)
- `commands` which expects a list of values, each of which is a list on its own, denoting the dependencies required by the model. Currently, dependencies `pip` and `conda` are supported. 
- `pip` dependencies are expected to be three element lists in the format `["pip", "library", "version"]`
- `conda` dependencies are expected to be four element lists in the format `["conda", "library", "version", "channel"]`, where channel is the conda channel to install the required library.

The installation parser will raise an exception if dependencies are not specified in the aforementioned format.

**Note**: Please note that we realise that this form of dependency specification is restrictive. We are [working](https://github.com/ersilia-os/ersilia-pack/issues/21) on extending how Ersilia Pack handles dependency specification, for example, to handle VCS and URL based dependencies. 


## Specifying Model Metadata

Model metadata should be specified within metadata.yml. An explanation of what these metadata fields correspond to can be found [here.](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/incorporate-models/model-template#the-metadata.json-file)

## Specifying Model APIs

A bash script within the `model/framework` directory is interepreted by Ersilia as an API for the model. For example, `run.sh` corresponds to a model `run` API, and similarly, a `fit.sh` would correspond to a model `fit` API. However arbitrary file names for bash script files are not allowed, and the acceptable names are one of the following: [`run`, `fit`]. 

## Adding Example Input and Output

It is always helpful to provide an example input and output while contributing a model to ease the verification of the model's working. To ensure all models always have an example, Ersilia checks for example CSV files in the `model/framework/examples` directory. In particular, Ersilia looks for `input.csv`, and `output.csv` files in this folder. These files are used to generate the necessary API end points for building a model server and therefore must always be provided.
