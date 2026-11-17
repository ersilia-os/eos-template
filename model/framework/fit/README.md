# Fit folder

This folder is only required for models with source `Internal` or `Replicated`. It should contain the data and code used to train the model, and results of model performance.

Once this folder holds training code or data, the whole folder is stored in S3 with [eosvc](https://github.com/ersilia-os/eosvc), not in git: add `"fit": "public"` to `access.json`, add `model/framework/fit/*` to `.gitignore`, and run `eosvc upload --path fit`. A model without a training step keeps this skeleton in git. See [Checkpoints and storage](https://ersilia.gitbook.io/ersilia-book/ersilia-model-hub/model-contribution/model-template#checkpoints-and-storage).

Please adhere to the following structure:

## `data` folder
This folder should contain the original data. If data processing is applied, please save a new file and do not modify the original. 

## `src` folder
Code to clean the data, train the model and plot the model performance results. Use the following notation:
- 00_data_cleaning.py: functions to clean data. This should include, at the minimmum, the standardisation of molecules using RDKIT or the `standardiser` package.
- 01_fit.py: code to train the actual model. Best practice would be to do a 5-fold (or 3-fold) cross-validation at 80-20 data split and train a final model with all the available data
- 02_performance.py: basic plots to assess model performance. At least, AUROC and a box plot or dot plot showing the predicted values for True Positives and True Negatives.

## `results` folder
Model performance information collected in `.json`, `.csv` and figures.

# Exceptions
In case of proprietary data, please include the relevant details about model training in the description of the model (method used, model performance during crossvalidation)

For models belonging to the `External` subtype, or where data is proprietary, this folder should be removed before pushing the first commit.