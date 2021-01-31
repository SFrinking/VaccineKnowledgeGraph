import lxml
from lxml import etree as ET
import pandas as PD
import csv
import argparse
import os
import pickle
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def get_text(sent_id, tree):
    """
    For a certain sent_id, return the text that corresponds
    """
    
    string = ""
    for element in tree.xpath("//text/wf[@sent='%s']" % sent_id):
        string += " " + element.text
    
    
    return(string)
    
def get_sent(span_term_ids, tree):
    """
    For a certain term_id, return the sent_id that corresponds
    """
    word_id = get_word_id(span_term_ids, tree)
    sentence = tree.xpath("//text/wf[@id='%s']" % word_id)[0].attrib["sent"]
    
    return (sentence)   

def get_word_id (any_id, tree):
    """
    For a certain id, return the word_id that corresponds
    """
    word_id = "w" + any_id[1:]
    return(word_id)
    

def get_word(term_id, tree):
    """
    For a certain term_id, return the word that corresponds
    """
    word_id = get_word_id(term_id, tree)
    word = tree.xpath("//text/wf[@id='%s']" % word_id)[0].text
    return(word)
   
def getSentiment(text):
    """
    For a certain sentence text, return the sentiment
    """
    
    score = analyser.polarity_scores(text)
    if score["compound"] > 0.3:
        result = "positive"
    elif score["compound"] < 0.3:
        result = "negative"
    else: 
        result = "neutral"
    return(result)
    

def dctToCsv(dct, filename, type = "all"):
    """
    Output the dictionary to a .csv file for further analysis
    
    :optional argument = type (default = "all"): if this is set to sentiment, it will not iterate over the values
    """
    #open the output directory
    with open(output_directory + os.sep + filename+ '.csv', 'w', newline="", encoding = "utf-8") as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(["sent_id", "sent_text", "polarity"])
        for key, value in dct.items():
            if type == "sentiment":
                writer.writerow([key, value[0], value[1]])
            else:
                for values in value:
                    try:
                        writer.writerow([key, values])
                    except:
                        print("Error caused by: ", key, " and ", value, "\n")

def sentSetToPickle(sentSet, filename):
    """
    Output the set of sentences to a pickle file
    """
    with open(output_directory + os.sep + filename+ '.pickle', 'wb') as outfile:
        pickle.dump(sentSet, outfile)
        
###Taken from the Applied Text Mining Course ©VU Amsterdam
def define_commandline_input():
    '''
    Defines arguments. options and commands for the commandline (using the argparse package)
    @rtype: ArgumentParser
    @returns: parser with all commandline arguments, options and commands
    '''

    parser = argparse.ArgumentParser(description='extracts information from NAF files')
    #adding obligatory arguments of input file and output file
    parser.add_argument('inputdir', metavar='in', type=str, nargs=1, help='path to the directory of input dirs (NAF)')
    parser.add_argument('outputdir', metavar='out', type=str, nargs=1, help='path to directory of outputdirs (CSV)')
    #adding optional arguments
    parser.add_argument('-p', '--pickle', action='store_true', help='output information to a pickle file')
    parser.add_argument('-c', '--csv', action='store_true', help='output information to a csv file')
    parser.add_argument('-s', '--sentiment', action='store_true', help='get the sentiment data and output it to a csv file')
    
    return parser
###


def extractInformation(filedir,filename):

    #empty dictionaries and set
    dctOfFrames = dict()
    dctSentiment = dict()
    sentSet = set()
    
    #load the xml file
    tree = ET.parse(filedir)
    
    #iterate over the frames
    for frame in listOfFrames:
        
        dctOfFrames[frame] = []
        
        
        for element in tree.xpath("//srl/predicate/externalReferences/externalRef[@resource='FrameNet' and @reference ='%s']" % frame):
            term_id = element.getparent().getparent().find("span").find("target").attrib["id"]
            word = get_word(term_id, tree) 
            sent_id = get_sent(term_id, tree)
            sentText = get_text(sent_id, tree)
            
            
            
            #if the frame is Statemen, check whether it's an opinion, then add
            if frame == "Statement":
                opinionOfStatement = tree.xpath("//opinions/opinion/opinion_expression/span/target[@id='%s']" % term_id)
                if len(opinionOfStatement) > 0:
                    polarity = opinionOfStatement[0].getparent().getparent().attrib["polarity"]
                    dctOfFrames[frame].extend([[word, sent_id, sentText, polarity]])
                    sentSet.add(sent_id)
            else:
                dctOfFrames[frame].extend([[word, sent_id, sentText]])
                sentSet.add(sent_id)
            
            
            
            if my_arguments.sentiment:
                if sent_id not in dctSentiment:
                    dctSentiment[sent_id] = [sentText, getSentiment(sentText)]
                else:
                    continue
                
    
    
    #output the file as a csv
    if my_arguments.csv: 
        dctToCsv(dctOfFrames, filename)
    
    #output the sentSet
    if my_arguments.pickle:
        sentSetToPickle(sentSet, filename)
    
    if my_arguments.sentiment:
        dctToCsv(dctSentiment, filename, type = "sentiment")

def main():
    
    #get all files in the input directory
    for naffile in os.listdir(naf_directory):
        filename = naffile.rstrip('.naf')
        filedir = naf_directory + os.path.sep + naffile
        print(filedir)
        extractInformation(filedir, filename)
        
    

if __name__ == '__main__':
    
    #instantiate object
    analyser = SentimentIntensityAnalyzer()
    
    ###Taken from the Applied Text Mining Course ©VU Amsterdam
    parser = define_commandline_input()
    my_arguments = parser.parse_args()
    
    naf_directory = my_arguments.inputdir[0]
    output_directory = my_arguments.outputdir[0]
    ###
    
    #open the file with frames to check for
    with open("Frames.txt", "r") as infile:
        frames = infile.read()
            
    #put it in a list
    listOfFrames = frames.split()
    
    
    
    main()