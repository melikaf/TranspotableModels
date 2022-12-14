# TranspotableModels

## Installing Packages ##

```python
pip3 install requirements.txt
```

## Running CP and OD models ##
```python
python3 transport.py
```
## Running XGB and LR based models ##
```python
python3 soph_models.py
```
## Config File Information ##

- defaults: A json file indicates the default value for all the input features. Please note that a valid value should be chosen for all the features available in the target location.
- zone_pairs: A list of tuples, showing the source population and target population values for each experiment.
- important_cols: List of important features using for sophisticated models. (A default value can not be found for all the features)
- def_key: Default Key containing tuples of important columns and their default value. Using for sophisticated models.

## pred.py functions and information ##
- calc_pred: Calculate predicted conditional probabilities for all the pairs in the target dataset.
  - Inputes:
    - gp1: Dataframe used as the source population.
    - gp2: Dataframe used as the target population.
    - p: The dictionary contains the the conditional probilities in the source population.
    - p2: The dictionary contains the conditional probilities in the target population. (Only default values gonna be used in the experiments though.)
    - label_col: The target feature. In the given dataset it is "duration_days".
    - split_col: The feature used as the populations. In the given dataset it is "ECOZONE".
    - defaults:  The json file indicates the default value for all the input features.
    - h: The true value of the target feature. The default is 1.
  - Outputs:
    - List of true labels in the target populations.
    - List of predicted conditional probabilities with CP model.
    - List of predicted conditional probabilities with D model.
    - List of predicted conditional probabilities with OD model.
    - Number of instances where D model fails to predict a valid number (predicted conditional probability is greater than 1).
    - Total number of instances in this experiments. (Usually it is number of input features * number of samples).
    
- calc_loss: Calculate average log loss for all the given models.
  - Inputes:
    - List of true labels in the target populations.
    - List of predicted conditional probabilities with CP model.
    - List of predicted conditional probabilities with D model.
    - List of predicted conditional probabilities with OD model.
  - Outputs:
    - Average Log Loss of CP model.
    - Average Log Loss of D model.
    - Average Log Loss of OD model.
    
- loss: Calculate average log loss for sophisticated models (XGB and LR based models.)
  - Inputes:
    - List of true labels in the target populations.
    - List of predicted conditional probabilities with the sophisticated model.
  - Outputs:
    - Average Log Loss of the given prediction.
    - Number of Errors in predicting log loss. (Samples with prediction 0 or 1.)

## p_calculator.py functions and information ##
- calc_p: For given source and target zones, calculate and return related dataframes and json of conditional probabilities in both populations.
- calc_p_def: For given source and target zones, calculate and return related dataframes and json of conditional probabilities in both populations. This function is for sophisticated models and use important columns.

## transport.py ##

This is the main file. By running this file as mentioned above, you will run CP, D and OD models for all the pairs mentioned in the config.py. The output, will be written in result.csv file. The outputs are ordered as: source_population, Target Population, Average Log Loss for CP, Average Log Loss for D, Average Log Loss for OD, number of samples failed in D model, total number of samples, Rate of the failure for D model.

## soph_models.py ##
This is the main file. By running this file as mentioned above, you will run LR and XGB based models for all the pairs mentioned in the config.py. The output, will be written in soph_models.csv file.  The outputs are ordered as: source_population, Target Population, LR-C Avg Loss, LR-D Avg Loss, LR-O Avg Loss, XGB-C Avg Loss, XGB-D Avg Loss, XGB-OD Avg Log loss

    
