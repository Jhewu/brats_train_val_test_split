"""
This script takes in a BraTS training directory 
and splits it into training, validation and testing
set. The reason being the only dataset containing 
ground truths is in the BraTS training set. If you're, 
late to the competition, you're unable to validate or
test your model, therefore we need to split the training
set and use it to validate and test our model. The scripts 
also uses threading to make this faster. 
"""

"""Imports"""
import os
from math import ceil
from random import shuffle
import shutil
import threading

"""HYPERPARAMETERS"""
TRAINING_FOLDER = "train_data"

TRAIN_SPLIT = 0.7
VAL_TEST_SPLIT = 0.15

"""Helper Functions"""
def CreateDir(folder_name):
   if not os.path.exists(folder_name):
       os.makedirs(folder_name) 
       
def CopyDir(src_list, src_base, dest_base):
    for dir in src_list:
        src_dir = os.path.join(src_base, dir)
        dest_dir = os.path.join(dest_base, dir)
        if os.path.exists(src_dir):
            shutil.copytree(src_dir, dest_dir)
        else:
            print(f"Source directory does not exist: {src_dir}")

"""Main Runtime"""
def Split_Train_Val_Test(): 
    # set up cwd and training and validation paths
    root_dir = os.getcwd()
    training_dir = os.path.join(root_dir, TRAINING_FOLDER)

    # list of directories in training and validation
    patients_train_list = os.listdir(training_dir)
    patients_length = len(patients_train_list)
    print(f"There is a total of: {patients_length} patients in the directory\n")

    # creating the split through indexes
    train_index = ceil(patients_length*TRAIN_SPLIT)
    print(f"Splitting... training set is {train_index} long")

    val_index = ceil(patients_length*VAL_TEST_SPLIT)
    print(f"Splitting... validation set is {val_index} long")

    test_index = patients_length-train_index-val_index
    print(f"Splitting... validation set is {test_index} long")

    # randomly shuffle the list before splitting 
    shuffle(patients_train_list)

    # create the respective train, val and test split
    train_list = patients_train_list[:train_index]
    val_list = patients_train_list[train_index:train_index+val_index]
    test_list = patients_train_list[train_index+val_index:]

    # create directories for each split
    train_dest = "dataset_split/train/"
    val_dest = "dataset_split/val/"
    test_dest = "dataset_split/test/"
    CreateDir(train_dest)
    CreateDir(val_dest)
    CreateDir(test_dest)

    # define the threads for copying directories
    threads = []

    # Create and start thread for training data
    train_thread = threading.Thread(target=CopyDir, args=(train_list, training_dir, train_dest))
    threads.append(train_thread)
    train_thread.start()

    # Create and start thread for validation data
    val_thread = threading.Thread(target=CopyDir, args=(val_list, training_dir, val_dest))
    threads.append(val_thread)
    val_thread.start()

    # Create and start thread for test data
    test_thread = threading.Thread(target=CopyDir, args=(test_list, training_dir, test_dest))
    threads.append(test_thread)
    test_thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All directories copied successfully.")

if __name__ == "__main__": 
    Split_Train_Val_Test()
    print("\nFinish splitting the dataset, please check your directory for dataset_split folder\n")