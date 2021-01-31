-- READ ME --
First, run the getsentences.py script to extract the data from the NAF files and perform a VADER sentiment analysis on it (see the readme documentation of the script for further details). The output of the script will be the input of X.
The script STAN loops through the NAF files, finds on the basis of the cue the frames provided by FrameNet and filters out the relevant 
frames. The relevant frames are handselected. Returns a folder of files with in every file the relevant sentence id's.
The script source_cue_content first makes a identifier dictionary form the source cue content in the CoNNL files, then it loops through 
the files with relevant sentence ids, takes this sentence id's and matches this filename and sentence id to the source cue content dictionary.
It does this by the triple tags such as #I-content-21648#B-content-21676:21674-Cue_21675-Source given in the CoNNL files. It returns the
knowledge graph as a dictionary. This dictionary is used as input for a lexicon based approach to calculate the factuality of a triple.
Finally, script Clustering_W2V_30.ipnyb groups the triples by using word embeddings on the content. It takes the centroid content as group.

Getting Started
1. Download the zipfolder 'Group1_System' and unpack it
2. Run getsentences.py, this provides output folder 'Polarity + Sents 3'
3. Download 4GB 'GoogleNews-vectors-negative300.bin'from https://code.google.com/archive/p/word2vec/
4. Open Knowledge_Graphs_Script2.ipnyb with Jupyter Notebook
2. Change PATH variable to your own path
3. Run script
4. Open Clustering_W2V_30.ipnyb with Jupyter Notebook
5. Run script

Requirements:
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
#NAME?
