"""
This script is a version of the split_train_val_test, and 
it's used to prepare the dataset for YOLO. The train_data 
folder should already contain the slices, therefore we are 
creating 3 separate directories and copying the respective 
split onto the folders. 
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
       
def CopyFile(src_list, src_base, dest_base):
    for file in src_list:
        src_dir = os.path.join(src_base, file)
        dest_dir = os.path.join(dest_base, file)
        if os.path.exists(src_dir):
            shutil.copy(src_dir, dest_dir)
        else:
            print(f"Source directory does not exist: {src_dir}")

"""Main Runtime"""
def Split_Train_Val_Test_YOLO(): 
    # set up cwd and training and validation paths
    root_dir = os.getcwd()
    training_dir = os.path.join(root_dir, TRAINING_FOLDER)

    # list of directories in training and validation
    slices_list = os.listdir(training_dir)
    slices_length = len(slices_list)
    print(f"There is a total of: {slices_length} slices in the directory\n")

    # creating the split through indexes
    train_index = ceil(slices_length*TRAIN_SPLIT)
    print(f"Splitting... training set is {train_index} long")

    val_index = ceil(slices_length*VAL_TEST_SPLIT)
    print(f"Splitting... validation set is {val_index} long")

    test_index = slices_length-train_index-val_index
    print(f"Splitting... validation set is {test_index} long")

    # randomly shuffle the list before splitting 
    shuffle(slices_list)

    # create the respective train, val and test split
    train_list = slices_list[:train_index]
    val_list = slices_list[train_index:train_index+val_index]
    test_list = slices_list[train_index+val_index:]

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
    train_thread = threading.Thread(target=CopyFile, args=(train_list, training_dir, train_dest))
    threads.append(train_thread)
    train_thread.start()

    # Create and start thread for validation data
    val_thread = threading.Thread(target=CopyFile, args=(val_list, training_dir, val_dest))
    threads.append(val_thread)
    val_thread.start()

    # Create and start thread for test data
    test_thread = threading.Thread(target=CopyFile, args=(test_list, training_dir, test_dest))
    threads.append(test_thread)
    test_thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("All directories copied successfully.")

if __name__ == "__main__": 
    Split_Train_Val_Test_YOLO()
    print("\nFinish splitting the dataset, please check your directory for dataset_split folder\n")