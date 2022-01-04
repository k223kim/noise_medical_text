import re
import random
from random import shuffle
import numpy as np
from constants import *

# from numba import jit, cuda
########################################################################
# Check if the current patient has a label of "N/A" (i.e. not applicable for both the perception and interpretation error)
########################################################################  
def label_exists(data):
    if "N/A" in data["label"]:
        return False
    else:
        return True

########################################################################
# Check if the current patient has a label of "No Finding" or "N/A" (i.e. only applicable for perception error)
######################################################################## 
def can_interpretation_error(data):
    if "No Finding" not in data["label"] and "N/A" not in data["label"]:
        return True
    else:
        return False

########################################################################
# Apply percetion (#1 error)
########################################################################  
def perception_error(data, df):
    #if current label is No Finding, add a random label
    #else, remove the label
    current_label = data["label"]
    if "No Finding" in current_label:
        possible_label = list(set(CATEGORIES) - set(current_label))
        new_label = random.choice(possible_label)
    else:
        new_label = "No Finding"
    filtered = df.loc[df["label_joined"].str.contains(new_label)]
    filtered_patients = filtered["study_id"].to_list()
    if len(filtered_patients) == 0:
        import pdb;pdb.set_trace()
    new_patient = random.choice(filtered_patients)
    new_impression = filtered[filtered["study_id"] == new_patient]["impression"].item()
    
    return new_impression

########################################################################
# new_interpretation error (#2 error)
########################################################################  
def new_interpretation_error(data, df):
    #we must consider the label tree from chexpert labeler
    current_label = data["label"]
    exclude_label = []
    for l in current_label:
        if l in CARDIO:
            exclude_label += CARDIO
        if l in LUNGOPACITY:
            exclude_label += LUNGOPACITY
        exclude_label.append(l)
    exclude_label = list(set(exclude_label))
    exclude_label.append("No Finding")
    possible_label = list(set(list(CATEGORIES)) - set(exclude_label))
    new_label = random.choice(possible_label)
    new_df = df
    for ex in exclude_label:
        new_df = new_df.loc[~df["label_joined"].str.contains(ex) & new_df["label_joined"].str.contains(new_label)]    
    filtered_patients = new_df["study_id"].to_list()
    new_patient = random.choice(filtered_patients)
    new_impression = new_df[new_df["study_id"] == new_patient]["impression"].item()
    
    return new_impression            

########################################################################
# Apply percetion (#1 error) and interpretation error (#2 error)
########################################################################  
def percetion_interpretation_error(data, df, dop):
    #if dop is true, apply perception error
    #else, apply interpretation error
    #pick a random error that is not part of the current patient's error
    current_label = data["label"]
    if dop:
        new_label = "No Finding"
    else:
        possible_label = list(set(CATEGORIES) - set(current_label))
        new_label = random.choice(possible_label)

    #now find a different patient that has a label that matches "new_label" (the selected new label)
    #notice that we do not want the new patient to have overlapping labels to the original patient
    ori_label = ",".join(current_label)
    filtered = df.loc[~df["label_joined"].str.contains(ori_label) & df["label_joined"].str.contains(new_label)]
    
    filtered_patients = filtered["study_id"].to_list()
    new_patient = random.choice(filtered_patients)
    new_impression = filtered[filtered["study_id"] == new_patient]["impression"].item()
    
    return new_impression
    
########################################################################
# Is number error applicable? if so, return the new sentence
########################################################################  
def number_error(sentence):
    list_sentence = re.findall(r'(?:[a-zA-Z]+)|(?:\d+(?:\.\d+)?(?::?\d+)?)', sentence)
    vals = [10, 100]
    probs = [0.5, 0.5]
    new_list = []    
    valid_nums = []
    for i, n in enumerate(list_sentence):
        if not n.isalpha() and i != len(list_sentence)-1:
            if list_sentence[i+1] == "mm" or  list_sentence[i+1] == "cm":
                curr_num = float(n)
                valid_nums.append(n)
                curr_val = np.random.choice(vals, 1, replace=True, p=probs).item()
                new_num1 = curr_num * curr_val
                new_num2 = curr_num / curr_val
                new = [new_num1, new_num2]
                new_probs = [0.5, 0.5]
                final_new = np.random.choice(new, 1, replace=True, p=new_probs).item()
                str_final_new = str(final_new)
                if len(str_final_new) > 7:
                    final_new = round(final_new)
                new_list.append(str(final_new))
            else:
                new_list.append(n)
        else:
            new_list.append(n)
#     print(valid_nums)
    if len(valid_nums) == 0:
        return False
    else:
        new_sentence = " ".join(new_list)
        return new_sentence
    
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
        "big_small" : {
            "big" : "small",
            "small" : "big",
            "Big" : "Small",
            "Small" : "Big"        
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
    number_err = number_error(sentence)
    
    possible_error = []
    if unit_dict:
        possible_error.append(unit_dict)
    if adjective_dict:
        possible_error.append(adjective_dict)
    if number_err:
        possible_error.append(number_err)

    if len(possible_error) == 0:
        return False
    elif len(possible_error) == 1:
        return possible_error[0]
    else:
        if len(possible_error) == 2:
            probs = [0.5, 0.5]
        else:
            probs = [0.35, 0.35, 0.3]
        choice_dict = np.random.choice(possible_error, 1, replace=True, p=probs)
        
        return choice_dict[0]
    
########################################################################
# Apply Writing error (error #3)
########################################################################  
def writing_error(replace_dict, sentence):
    if isinstance(replace_dict, str):#this means that the number error has been selected
        return replace_dict
    else:#it is either an adjective error or an unit error
        #use replace_dict to replace the selected word
        regex = re.compile("(%s)" % "|".join(map(re.escape, replace_dict.keys())))
        return regex.sub(lambda mo: replace_dict[mo.string[mo.start():mo.end()]], sentence) 
    
def cap(match):
    return(match.group().capitalize())

#############################################################################################################
# When interpretation error is applied, we must check for numbers and date and replace them accordingly
#############################################################################################################
def match_nums_date(sentence, error_sentence):
    #collect all info from original sentence
    ori_numbers = []
    ori_dates = []
    ori_left = []
    ori_right = []
    ori_upper = []
    ori_lower = []
    ori_high = []
    ori_low = []

    ori_sentence = re.findall(r'(?:[a-zA-Z]+)|(?:\d+(?:\.\d+)?(?::?\d+)?)(?:\s*[a|p|c]?\.?m\.?m?)', sentence)
    for idx, ori in enumerate(ori_sentence):
        if not ori.isalpha():
            if "cm" in ori or "mm" in ori:
                ori_numbers.append(ori)
            if "a.m." in ori or "a.m" in ori or "am" in ori or\
            "p.m." in ori or "p.m" in ori or "pm" in ori:
                ori_dates.append(ori)

        if ori_sentence[idx] == "left" or ori_sentence[idx] == "Left":
            ori_left.append(ori)
        elif ori_sentence[idx] == "right" or ori_sentence[idx] == "Right":
            ori_right.append(ori)
        elif ori_sentence[idx] == "upper" or ori_sentence[idx] == "Upper":
            ori_upper.append(ori)
        elif ori_sentence[idx] == "lower" or ori_sentence[idx] == "Lower":
            ori_lower.append(ori)
        elif ori_sentence[idx] == "high" or ori_sentence[idx] == "High":
            ori_high.append(ori)
        elif ori_sentence[idx] == "low" or ori_sentence[idx] == "Low":
            ori_low.append(ori)

    #collect all info from error sentence
    err_numbers = []
    err_dates = []
    err_left = []
    err_right = []
    err_upper = []
    err_lower = []
    err_high = [] 
    err_low = []

    err_sentence = re.findall(r'(?:[a-zA-Z]+)|(?:\d+(?:\.\d+)?(?::?\d+)?)(?:\s*[a|p|c]?\.?m\.?m?)', error_sentence)
    for idx, err in enumerate(err_sentence):
        if not err.isalpha() and idx != len(err_sentence) - 1:
            if "cm" in err or "mm" in err:
                err_numbers.append(err)
            if "a.m." in err or "a.m" in err or "am" in err or\
            "p.m." in err or "p.m" in err or "pm" in err:
                err_dates.append(err)
        if err_sentence[idx] == "left" or err_sentence[idx] == "Left":
            err_left.append(err)
        elif err_sentence[idx] == "right" or err_sentence[idx] == "Right":
            err_right.append(err)
        elif err_sentence[idx] == "upper" or err_sentence[idx] == "Upper":
            err_upper.append(err)
        elif err_sentence[idx] == "lower" or err_sentence[idx] == "Lower":
            err_lower.append(err)
        elif err_sentence[idx] == "high" or err_sentence[idx] == "High":
            err_high.append(err)
        elif err_sentence[idx] == "low" or err_sentence[idx] == "Low":
            err_low.append(err)


    final_sentence = error_sentence

    # #replace only if the numbers match
    if len(ori_left) > 0 and len(ori_right) == 0 and len(err_right) > 0:
        for err in err_right:
            if err == "Right":
                final_sentence = final_sentence.replace(err, "Left")
            else:
                final_sentence = final_sentence.replace(err, "left")
    elif len(ori_right) > 0 and len(ori_left) == 0 and len(err_left) > 0:
        for err in err_left:
            if err == "Left":
                final_sentence = final_sentence.replace(err, "Right")
            else:
                final_sentence = final_sentence.replace(err, "right")

    if len(ori_upper) > 0 and len(ori_lower) == 0 and len(err_lower) > 0:
        for err in err_lower:
            if err == "Lower":
                final_sentence = final_sentence.replace(err, "Upper")
            else:
                final_sentence = final_sentence.replace(err, "upper")
    elif len(ori_lower) > 0 and len(ori_upper) == 0 and len(err_upper) > 0:
        for err in err_upper:
            if err == "Upper":
                final_sentence = final_sentence.replace(err, "Lower")
            else:
                final_sentence = final_sentence.replace(err, "lower")

    if len(ori_high) > 0 and len(ori_low) == 0 and len(err_low) > 0:
        for err in err_low:
            if err == "Low":
                final_sentence = final_sentence.replace(err, "High")
            else:
                final_sentence = final_sentence.replace(err, "high")
    elif len(ori_low) > 0 and len(ori_high) == 0 and len(err_high) > 0:
        for err in err_high:
            if err == "High":
                final_sentence = final_sentence.replace(err, "Low")
            else:
                final_sentence = final_sentence.replace(err, "low")

    if len(ori_numbers) > 0 and len(err_numbers) > 0:
        if len(ori_numbers) >= len(err_numbers):
            np_ori_numbers = np.array(ori_numbers)
            np.random.shuffle(np_ori_numbers)
            for idx in range(len(err_numbers)):
                final_sentence = final_sentence.replace(err_numbers[idx], np_ori_numbers[idx])
        else:
            np_err_numbers = np.array(err_numbers)
            np.random.shuffle(np_err_numbers)
            for idx in range(len(ori_numbers)):
                final_sentence = final_sentence.replace(np_err_numbers[idx], ori_numbers[idx])
            
    if len(ori_dates) > 0 and len(err_dates) > 0:
        if len(ori_dates) >= len(err_dates):
            np_ori_dates = np.array(ori_dates)
            np.random.shuffle(np_ori_dates)            
            for num in range(len(err_dates)):
                final_sentence = final_sentence.replace(err_dates[num], np_ori_dates[num])
        else:
            np_err_dates = np.array(err_dates)
            np.random.shuffle(np_err_dates)
            for num in range(len(ori_dates)):
                final_sentence = final_sentence.replace(np_err_dates[num], ori_dates[num])
                
    return final_sentence

########################################################################
# where it actually generates errors
########################################################################  
def error(df, data):
#     import pdb;pdb.set_trace()
    sentence = data["impression"]
    prob = [0.5, 0.5]
    #probability of selecting (interpretation error) vs (writing error)
    augmented_sentences = []
    label = label_exists(data)
    types_of_error = []
    if label:#check if label exists
        #used for perception and interpretation error
        df["label_joined"] = df["label"].str.join(sep=",")
        #apply perception error
        types_of_error.append("perception_error")
#         augmented_sentences.append(perception_error(data, df))
        if (can_interpretation_error(data)):
            types_of_error.append("interpretation_error")
#             augmented_sentences.append(new_interpretation_error(data, df))
    
    #check for writing error
    #only when the label is not "No Finding"
    if "No Finding" not in data["label"]:
        we = can_writing_error(sentence)
        if we:#if writing error is possible
            types_of_error.append("writing_error")
#             augmented_sentences.append(writing_error(we, sentence))
        
#     import pdb;pdb.set_trace()
    if len(types_of_error) < 1:
        selected_augmentation = sentence
        error_label = 0
    else:
        if len(types_of_error) == 1:
            selected_error = types_of_error[0]
        else:
            if "perception_error" in types_of_error:#there are too many perception error at this point
                types_of_error.remove("perception_error")
            if len(types_of_error) == 1:
                selected_error = types_of_error[0]
            elif len(types_of_error) == 2: #only two errors were applicable
                prob = [0.5, 0.5]
                selected_error = np.random.choice(types_of_error, 1, prob).item()
            # else: #all three errors were applicable
#                 prob = [0, 0.5, 0.5]
#             selected_error = np.random.choice(types_of_error, 1, prob).item()
        if selected_error == "writing_error":
            selected_augmentation = writing_error(we, sentence)
            error_label = 3
        elif selected_error == "perception_error":
            selected_augmentation = perception_error(data, df)
            error_label = 1
        elif selected_error == "interpretation_error":
            selected_augmentation = new_interpretation_error(data, df)
            selected_augmentation = match_nums_date(sentence, selected_augmentation)
            error_label = 2
            
        
#     #append the original sentence if no augmentation happened
#     if len(augmented_sentences) < 1:
#         selected_augmentation = sentence
        
#     elif len(augmented_sentences) == 1:
#         selected_augmentation = augmented_sentences[0]
#     else:
#         if len(augmented_sentences) == 2:#only two errors were applicable
#             prob = [0.5, 0.5]
#         else:#all three errors were applicable
#             prob = [0.35, 0.35, 0.3]
#         selected_augmentation = np.random.choice(augmented_sentences, 1, prob).item()
    return selected_augmentation, error_label