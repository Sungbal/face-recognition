#!/usr/bin/env python

# NOTE: PROGRAM NEEDS GETCHAR IN ORDER TO FUNCTION UNDER THE CASE WHERE PATHS
#       EXIST!!!

# PROGRAM INFO:
# Splits data into given fractions. Make sure that the input directory structure
# contains folders with the NAMES Of the classes desired. As an example, this
# script will divide the strucuture below (assuming Data is your data dir):
#        Data/1     Data/2      Data/3      Data/4
# into
#       Training/1  Testing/1   Validation/1    Training/2  Testing/2   etc...
# Use the script along with -h in order to see more options

import os
import random
import argparse
import shutil
import getch

def splitData(pathToDirectory:str, pTrain:int, pVal:int, pTest:int)->None:
    ### Generate list of folders and create three paths
    ###   1) data/training
    ###   2) data/validation 
    ###   3) data/testing
    TRAIN_PATH = os.path.abspath(pathToDirectory+"/../images/17/crop/training/")
    VAL_PATH = os.path.abspath(pathToDirectory+"/../images/17/crop/validation/")
    TEST_PATH = os.path.abspath(pathToDirectory+"/../images/17/crop/testing/")
    allLoc = [TRAIN_PATH, VAL_PATH, TEST_PATH]

    # Check for possible overwrites
    for elem in allLoc:
        if os.path.exists(elem):
            print('Path {} already exists! Overwrite? (y/n)'.format(elem))
            char = getch.getch()
            if char.lower() != 'y':
                print('Terminated....')
                return
            else:
                shutil.rmtree(elem)
                while(os.path.exists(elem)):
                    pass # Hold to ensure race condition doesn't ensue when making dirs
                os.makedirs(elem)
        else:
            os.makedirs(elem)

    # Iterate through all directories and perform shuffling
    for directory in os.listdir(pathToDirectory):
        print("Processing {}...".format(directory).ljust(60), end='', flush=True)
        files = [os.path.join(pathToDirectory, directory, file) for file in
                    os.listdir(os.path.join(pathToDirectory, directory))]
        print("Number of files found: {}".format(len(files)))

        # Check for sufficient file quantity
        if(len(files) < 3):
            raise Exception('Insufficient data available for split!')

        # Enough files present. Choose three random files to start off shuffle
        for init_path in allLoc:
            toPart = random.choice(files)
            os.makedirs(os.path.join(init_path, directory))
            shutil.copy(toPart, os.path.join(init_path,directory))
            files.remove(toPart)

        # Now proceed to randomly select files in appropriate quantities for rest
        if(len(files) > 0):
            population = [1, 2, 3]
            weights = [float(pTrain)/100, float(pVal)/100, float(pTest)/100]
            split = random.choices(population, weights, k=len(files))
            for elem,loc in enumerate(split):
                shutil.copy(files[elem], os.path.join(allLoc[loc-1],directory))

            # Small insurance of probability distribution
            from collections import Counter
            evalCount = Counter(split)
            print("Split:{},{},{}".format(evalCount[1]+1, evalCount[2]+1, evalCount[3]+1))

def parseArgs():
    parser = argparse.ArgumentParser(description="Split data into training/validation/testing sets")
    parser.add_argument('src_dir', help='source directory')
    parser.add_argument('split', metavar='P', type=int, nargs=3, help="Three integers\
                         representing the T/V/S split for the dataset specified")
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()
    src_dir = args.src_dir.rstrip('/')
    split = args.split

    # Check for valid split
    if(sum(split)!=100):
        raise Exception('Invalid cummulative values for split: {}'.format(sum(split)))

    # Check for existant directory
    if not os.path.exists(src_dir):
        raise Exception('Directory does not exist ({})'.format(src_dir))

    # Pass to function to create folders as needed
    splitData(os.path.abspath(src_dir), split[0], split[1], split[2])
