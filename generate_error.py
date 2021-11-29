import re
import random
from random import shuffle

########################################################################
# Replace cm to mm or mm to cm
########################################################################    
# def unit_exits(sentence):
# #     all_lower = sentence.lower()
#     find_unit = re.findall("(\d+(?:\.\d*)?)\s*(cm|mm)", sentence)
#     if len(find_unit) > 0:
#         return True
#     else:
#         return False
    
def unit_replacement(sentence):
#     all_lower = sentence.lower()
    unit_dict = {
        "mm" : "cm",
        "cm" : "mm"
    }
    regex = re.compile("(%s)" % "|".join(map(re.escape, unit_dict.keys())))
    return regex.sub(lambda mo: unit_dict[mo.string[mo.start():mo.end()]], sentence) 

########################################################################
# Replace right, left, upper, lower, high, low, partially, fully, small, big
########################################################################    
# def cap(match):#in order to capitalize the first letter in a sentence
#     return(match.group().capitalize())

# def left2right(sentence):
#     l2r = re.compile(re.escape('left'), re.IGNORECASE)
#     l2r_result = l2r.sub('right', sentence)
    
#     l2r_final = re.compile(r'(?<=[\.\?!]\s)(\w+)')
#     return l2r_final.sub(cap, l2r_result)
    
# def right2left(sentence):
#     r2l = re.compile(re.escape('right'), re.IGNORECASE)
#     r2l_result = r2l.sub('left', sentence)
    
#     r2l_final = re.compile(r'(?<=[\.\?!]\s)(\w+)')
#     return r2l_final.sub(cap, r2l_result)

def replace_antonyms(sentence):
    antonyms = {
        "right" : "left",
        "left" : "right",
        "Right" : "Left",
        "Left" : "Right",
        "upper" : "lower",
        "lower" : "upper",
        "Upper" : "Lower",
        "Lower" : "Upper",
        "high" : "low",
        "low" : "high",
        "High" : "Low",
        "Low" : "High",
        "partially" : "fully",
        "fully" : "partially",
        "Partially" : "Fully",
        "Fully" : "Partially",
        "big" : "small",
        "small" : "big",
        "Big" : "Small",
        "Small" : "Big"
    }
    regex = re.compile("(%s)" % "|".join(map(re.escape, antonyms.keys())))
    return regex.sub(lambda mo: antonyms[mo.string[mo.start():mo.end()]], sentence)     

########################################################################
# where it actually generates errors
########################################################################  

def error(sentence):
    augmented_sentences = []
    
    replace the unit
    augmented_sentences.append(unit_replacement(sentence))
    #replace left to right
#     augmented_sentences.append(left2right(sentence))
    #replace right to left
#     augmented_sentences.append(right2left(sentence))

    #replace to antonyms
    augmented_sentences.append(replace_antonyms(sentence))
    
    #avoid duplicates (i.e. original sentences)
#     augmented_sentences = list(set(augmented_sentences))
#     shuffle(augmented_sentences)

    #append the original sentence if no augmentation happened
    if len(augmented_sentences) < 1:
        augmented_sentences.append(sentence)

    return augmented_sentences[0]