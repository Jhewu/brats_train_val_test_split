This script takes in a BraTS training directory 
and splits it into training, validation and testing
set. The reason being the only dataset containing 
ground truths is in the BraTS training set. If you're, 
late to the competition, you're unable to validate or
test your model, therefore we need to split the training
set and use it to validate and test our model. The scripts 
also uses threading to make this faster. 