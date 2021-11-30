import re
import random
from random import shuffle
import numpy as np

########################################################################
# Is unit error applicable?
########################################################################  
def unit_error(sentence):
    result = []
    unit_dict = {
        "cm_mm" : {
            "cm" : "mm",
            "mm" : "cm"      
        }
    }    
    for i in unit_dict.keys():
        key_ = i.split("_")
        key1, key2 = key_[0], key_[1]
        if key1 in sentence or key2 in sentence:
            result.append(unit_dict[i])
    if len(result) == 0:
        return {}
    else:
        shuffle(result)
        return result[0]
    
########################################################################
# Is adjective error applicable?
########################################################################  
def adjective_error(sentence):
    result = []
    adjective_dict = {
        "left_right" : {
            "right" : "left",
            "left" : "right",
            "Right" : "Left",
            "Left" : "Right",        
        },
        "upper_lower" : {
            "upper" : "lower",
            "lower" : "upper",
            "Upper" : "Lower",
            "Lower" : "Upper"
        },
        "high_low" : {
            "high" : "low",
            "low" : "high",
            "High" : "Low",
            "Low" : "High"
        },
        "partially_fully" : {
            "partially" : "fully",
            "fully" : "partially",
            "Partially" : "Fully",
            "Fully" : "Partially",
        },
        "big_small" : {
            "big" : "small",
            "small" : "big",
            "Big" : "Small",
            "Small" : "Big"        
        },
        "mild_aggressive" : {
            "mild" : "aggressive",
            "aggressive" : "mild",
            "Mild" : "Aggressive",
            "Aggressive" : "Mild"
        }
    }
    for i in adjective_dict.keys():
        key_ = i.split("_")
        key1, key2 = key_[0], key_[1]
        if key1 in sentence.lower() or key2 in sentence.lower():
            result.append(adjective_dict[i])
    if len(result) == 0:
        return {}
    else:
        shuffle(result)
        return result[0]
    
########################################################################
# Is (#3) writing error applicable?
########################################################################  
def can_writing_error(sentence):
    #check if the impression has no significance (if the label is "no findings")
    #e.g. No acute cardiopulmonary process.
    
    unit_dict = unit_error(sentence)
    adjective_dict = adjective_error(sentence)

    if not unit_dict:#no unit in the sentence
        if not adjective_dict:#no adjective to replace
            return False
        else:#only adjective can be replaced
            return adjective_dict
    else:
        if not adjective_dict:#only unit can be replaced
            return unit_dict
        else:#both are applicable
            probs = [0.5, 0.5]
            dicts = [unit_dict, adjective_dict]
            choice_dict = np.random.choice(dicts, 1, replace=True, p=probs)
            return choice_dict[0]
########################################################################
# Apply Writing error (error #3)
########################################################################  
def writing_error(replace_dict, sentence):
    #use replace_dict to replace the selected word
    regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
    return regex.sub(lambda mo: replace_dict[mo.string[mo.start():mo.end()]], sentence) 

########################################################################
# where it actually generates errors
########################################################################  

def error(sentence):
    prob2 = []
    #probability of selecting (perception error + interpretion error) vs (writing error)
    augmented_sentences = []
    
    #check for writing error
    we = can_writing_error(sentence)
    if we:#if writing error is possible
        augmented_sentences.append(writing_error(we, sentence))

    #append the original sentence if no augmentation happened
    if len(augmented_sentences) < 1:
        augmented_sentences.append(sentence)

    return augmented_sentences[0]