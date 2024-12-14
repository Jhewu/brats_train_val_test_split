split_train_val_test is a script takes in a BraTS training directory 
and splits it into training, validation and testing
set. The reason being the only dataset containing 
ground truths is in the BraTS training set. If you're, 
late to the competition, you're unable to validate or
test your model, therefore we need to split the training
set and use it to validate and test our model. The scripts 
also uses threading to make this faster. 

Meanwhile split_train_val_test_YOLO is a version of the 
split_train_val_test, and it's used to prepare the dataset
for YOLO. The train_data folder should already contain the slices,
therefore we are creating 3 separate directories and copying the 
respective split onto the folders. 
