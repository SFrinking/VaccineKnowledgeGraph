# GetSentences

This script will extract the sentences for given frames from NAF files, and output them together with a sentiment analysis result done by the VADER package. 

## Installation

To get this script working, you need to install the following packages:

	lxml
	pandas
	csv
	argparse
	os
	pickle
	vaderSentiment

## Usage

To run the script, type the following in the command prompt:
	
	python getsentences.py [inputfolder with NAF files] [outputfolder (which should exist)] [optional arguments]
	
	optional arguments: 	-s: get the sentiment analysis and output as a csv
			-p: output the sentences as a dictionary in a pickle file
			-c: ouput the frames, sentences and text as a csv
	
	warning: -s and -c do not work together, since they both output the files with the same name

	make sure that in the same folder as the script are the following things:
		inputfolder (as given in the command)
		outputfolder (as given in the command)
		a .txt file called "Frames.txt" which has all frames that should be searches for, seperated by a newline. Make sure the frames are exactly similar to the ones used by Framenet.