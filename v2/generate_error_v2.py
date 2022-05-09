import numpy as np
import random
import re

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
                curr_val = np.random.choice(vals, 1, replace=False, p=probs).item()
                new_num1 = curr_num * curr_val
                new_num2 = curr_num / curr_val
                new = [new_num1, new_num2]
                new_probs = [0.5, 0.5]
                final_new = np.random.choice(new, 1, replace=False, p=new_probs).item()
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
        return []
    else:
        new_sentence = " ".join(new_list)
        return [new_sentence]

########################################################################
# Apply unit error if possible. If not, return empty list
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
        return []
    else:
        random.shuffle(result)
        result = result[0]
        regex = re.compile("(%s)" % "|".join(map(re.escape, result.keys())))
        unit_error = regex.sub(lambda mo: result[mo.string[mo.start():mo.end()]], sentence)
        return [unit_error]
########################################################################
# Apply adjective error if applicable. If not, return empty list
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
        return []
    else:
        random.shuffle(result)
        l = min(len(result), 2)
        adjective_errors = []
        for i in range(l):
            curr_result = result[i]
            regex = re.compile("(%s)" % "|".join(map(re.escape, curr_result.keys())))
            adjective_errors.append(regex.sub(lambda mo: curr_result[mo.string[mo.start():mo.end()]], sentence))
        return adjective_errors        

########################################################################
# Apply keyword error if applicable. IF not, return empty list
########################################################################  
def keyword_error(sentence):
    result = []
    keywords = {
        "LUL":0,
        "RUL":0,
        "LLL":0,
        "RLL":0,
        "RML":0,
        "LML":0
    }
    for key in keywords.keys():
        if key in sentence:
            keywords[key] += 1
    found_keys = set(list({k:v for k,v in keywords.items() if v > 0}))
    if len(found_keys) == 0:
        return []
    else:
        other_keys = list(set(list(keywords)) - found_keys)
        found_keys = list(found_keys)    
        random.shuffle(found_keys)
        l = min(len(found_keys), 2)            
        keyword_errors = []

        for i in range(l):
            existing = found_keys[i]
            new_keyword = random.choice(other_keys)
            keyword_errors.append(sentence.replace(existing, new_keyword))     
        
        return keyword_errors


########################################################################
# Apply factual error
########################################################################   
def factual_error(sentence):
    #number error
    ne = number_error(sentence)
    #unit error
    ue = unit_error(sentence)
    #adjective error
    ae = adjective_error(sentence)
    #keyword error
    ke = keyword_error(sentence)

    final_factual_error = ne + ue + ae + ke
    return final_factual_error

########################################################################
# When interpretation error is applied, we must check for numbers and date and replace them accordingly
######################################################################## 
def match_nums_date(sentence, error_sentence, ori_findings):
    #collect all info from original sentence
    ori_numbers = []
    ori_dates = []
    ori_left = []
    ori_right = []
    ori_upper = []
    ori_lower = []
    ori_high = []
    ori_low = []
    ori_key_words = []

    ori_sentence = re.findall(r'(?:[a-zA-Z]+)|(?:\d+(?:\.\d+)?(?::?\d+)?)(?:\s*[a|p|c]?\.?m\.?m?)', sentence)
    #we will maintain dates in original findings
    ori_dates = re.findall(r'\d{4}-\d{2}-\d{2}|\d{4}-\d{2}-\d{1}|\d{4}-\d{1}-\d{2}|\d{4}-\d{1}-\d{1}|\d{2}-\d{2}-\d{2}|\d{2}-\d{2}-\d{1}|\d{2}-\d{1}-\d{2}|\d{2}-\d{1}-\d{1}',ori_findings)
    for idx, ori in enumerate(ori_sentence):
        if not ori.isalpha():
            if "cm" in ori or "mm" in ori:
                ori_numbers.append(ori)

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
        elif ori_sentence[idx] == "LUL" or ori_sentence[idx] == "RUL" or ori_sentence[idx] == "LLL" or ori_sentence[idx] == "RLL" or ori_sentence[idx] == "RML" or ori_sentence[idx] == "LML":
            ori_key_words.append(ori)

    #collect all info from error sentence
    err_numbers = []
    err_dates = []
    err_left = []
    err_right = []
    err_upper = []
    err_lower = []
    err_high = [] 
    err_low = []
    err_key_words = []

    err_sentence = re.findall(r'(?:[a-zA-Z]+)|(?:\d+(?:\.\d+)?(?::?\d+)?)(?:\s*[a|p|c]?\.?m\.?m?)', error_sentence)
    err_dates = re.findall(r'\d{4}-\d{2}-\d{2}|\d{4}-\d{2}-\d{1}|\d{4}-\d{1}-\d{2}|\d{4}-\d{1}-\d{1}|\d{2}-\d{2}-\d{2}|\d{2}-\d{2}-\d{1}|\d{2}-\d{1}-\d{2}|\d{2}-\d{1}-\d{1}',error_sentence)
    for idx, err in enumerate(err_sentence):
        if not err.isalpha():
            if "cm" in err or "mm" in err:
                err_numbers.append(err)
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
        elif err_sentence[idx] == "LUL" or err_sentence[idx] == "RUL" or err_sentence[idx] == "LLL" or err_sentence[idx] == "RLL" or err_sentence[idx] == "RML" or err_sentence[idx] == "LML":
            err_key_words.append(err)


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
    #check if there is "no change" in both sentence and error_sentence
    lower_sentence = sentence.lower()
    lower_error_sentence = error_sentence.lower()
    date_change = 0
    if len(ori_dates) > 0:
        if "no" in lower_sentence and "change" in lower_sentence and "no" in lower_error_sentence and "change" in lower_error_sentence:
            #do not change date
            pass
        else:
            #change dates with 70% chance
            date_change = random.choices([0, 1], [0.3, 0.7])[0]
    # print(date_change)/

    if date_change:    
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

    #change key words
    if len(ori_key_words) > 0 and len(err_key_words) > 0:
        ori_left, ori_right, ori_middle, ori_upper, ori_lower = [], [], [], [], []
        for words in ori_key_words:
            if words.startswith("R"):
                ori_right.append(words)
            if words.startswith("L"):
                ori_left.append(words)
            if words[1] == "U":
                ori_upper.append(words)
            if words[1] == "L":
                ori_lower.append(words)
            if words[1] == "M":
                ori_middle.append(words)
        err_left, err_right, err_middle, err_upper, err_lower = [], [], [], [], []
        for words in err_key_words:
            if words.startswith("R"):
                err_right.append(words)
            if words.startswith("L"):
                err_left.append(words)
            if words[1] == "U":
                err_upper.append(words)
            if words[1] == "L":
                err_lower.append(words)
            if words[1] == "M":
                err_middle.append(words)

        if ori_left and not ori_right and err_right:
            #replace right to left
            for err in err_right:
                new_err = "L"+err[1:]
                final_sentence = final_sentence.replace(err, new_err)
            if err_upper:
                for err in err_upper:
                    if err.startswith("R"):
                        new_err = "L"+err[1:]
                        err_upper.remove(err)
                        err_upper.append(new_err)
            if err_lower:
                for err in err_lower:
                    if err.startswith("R"):
                        new_err = "L"+err[1:]
                        err_lower.remove(err)
                        err_lower.append(new_err)      
            if err_middle:
                for err in err_middle:
                    if err.startswith("R"):
                        new_err = "L"+err[1:]
                        err_middle.remove(err)
                        err_middle.append(new_err)    
        if ori_right and not ori_left and err_left:
            #replace left to right
            for err in err_left:
                new_err = "R"+err[1:]
                final_sentence = final_sentence.replace(err, new_err)

            if err_upper:
                for err in err_upper:
                    if err.startswith("L"):
                        new_err = "R"+err[1:]
                        err_upper.remove(err)
                        err_upper.append(new_err)
            if err_lower:
                for err in err_lower:
                    if err.startswith("L"):
                        new_err = "R"+err[1:]
                        err_lower.remove(err)
                        err_lower.append(new_err)      
            if err_middle:
                for err in err_middle:
                    if err.startswith("L"):
                        new_err = "R"+err[1:]
                        err_middle.remove(err)
                        err_middle.append(new_err)  

        if ori_upper and not ori_lower and not ori_middle and (err_lower or err_middle):
            #replace lower or middle -> upper
            if err_lower:
                for err in err_lower:
                    new_err = err[0]+"U"+err[2:]
                    final_sentence = final_sentence.replace(err, new_err)
            if err_middle:
                for err in err_middle:
                    new_err = err[0]+"U"+err[2:]
                    final_sentence = final_sentence.replace(err, new_err)
        if ori_lower and not ori_upper and not ori_middle and (err_upper or err_middle):
            #replace upper or middle -> lower
            if err_upper:
                for err in err_upper:
                    new_err = err[0]+"L"+err[2:]
                    final_sentence = final_sentence.replace(err, new_err)
            if err_middle:
                for err in err_middle:
                    new_err = err[0]+"L"+err[2:]
                    final_sentence = final_sentence.replace(err, new_err)        
        if ori_middle and not ori_upper and not ori_lower and (err_upper or err_lower):
            #replace upper or lower -> middle
            if err_upper:
                for err in err_upper:
                    new_err = err[0]+"M"+err[2:]
                    final_sentence = final_sentence.replace(err, new_err)
            if err_middle:
                for err in err_lower:
                    new_err = err[0]+"M"+err[2:]
                    final_sentence = final_sentence.replace(err, new_err)             

    return final_sentence

########################################################################
# calculate the distance from the current centroid to the rest of the other centroids
######################################################################## 

def get_distance(cluster_info, current):
    current_centroid = cluster_info[current]
    rest_centroid = cluster_info
    distance = np.zeros([rest_centroid.shape[0]])
    for i, row in enumerate(rest_centroid):
        distance[i] = 1 - np.dot(current_centroid, row)
    return distance

def farthest_k_clusters(distance, k, current_cluster):
    #get k+1 just in case it includes current cluster
    indices = np.argpartition(distance, -k-1)[-k-1:]
    #check if indices has current cluster
    if current_cluster in indices:
        indices = np.delete(indices, np.where(indices == current_cluster))
    else:
        indices = indices[1:]
    return indices
    
def closest_k_clusters(distance, k, current_cluster):
    #we do +1 since we want to disregard the current cluster
    max_val = max(distance)
    temp_distance = np.where(distance <= 0.2, max_val, distance)
    indices = np.argpartition(temp_distance, k+1)[:k+1]
    #check if indices has current cluster
    if current_cluster in indices:
        indices = np.delete(indices, np.where(indices == current_cluster))
    else:
        indices = indices[1:]
    return indices

def other_k_clusters(current_cluster, farthest, closest, total_num_clusters, k):
    indices = np.array(range(total_num_clusters))
    indices = np.delete(indices, np.where(indices == current_cluster))
    for c in closest:
        indices = np.delete(indices, np.where(indices == c))  
    for f in farthest:  
        indices = np.delete(indices, np.where(indices == f))
    selected_indices = np.random.choice(indices, k)
    return selected_indices    

def swap_impression(index, df):
    new_clusters = df[df["cluster"] == index]["index"]
    new_clusters = new_clusters.to_numpy()
    new_patient = np.random.choice(new_clusters)
    new_impression = df[df["index"]==new_patient]["impression"]
    return new_impression

########################################################################
# where impression error actually generates errors
########################################################################  
def error(data, df, cluster_info, k, ori_impression, ori_findings):
    #k indicates the top k closest/farthest cluster from the current cluster
    current_cluster = int(data["cluster"])
    distance = get_distance(cluster_info, current_cluster)

    new_impressions, error_labels, error_clusters = [],[], []

    ####interpretive error

    #swap between top 2 farthest cluster
    farthest_indices = farthest_k_clusters(distance, 2, current_cluster)
    for idx in farthest_indices:
        assert idx != current_cluster
        new_impression = swap_impression(idx, df).item()
        new_impression = match_nums_date(ori_impression, new_impression, ori_findings)
        new_impressions.append(new_impression)
        error_labels.append("2")
        error_clusters.append(str(idx))

    #swap between top 5 closest cluster
    closest_indices = closest_k_clusters(distance, 5, current_cluster)
    for idx in closest_indices:
        assert idx != current_cluster
        new_impression = swap_impression(idx, df).item()
        new_impression = match_nums_date(ori_impression, new_impression, ori_findings)
        new_impressions.append(new_impression)
        error_labels.append("1")
        error_clusters.append(str(idx))

    #swap between other clusters
    other_indices = other_k_clusters(current_cluster, farthest_indices, closest_indices, len(distance), 3)
    for idx in other_indices:
        new_impression = swap_impression(idx, df).item()
        new_impression = match_nums_date(ori_impression, new_impression, ori_findings)
        new_impressions.append(new_impression)
        error_labels.append("3")
        error_clusters.append(str(idx))

    ####factual error
    factual_errors = factual_error(ori_impression)
    for fe in factual_errors:
        new_impressions.append(fe)
        error_labels.append("4")
        error_clusters.append(str(current_cluster))

    return new_impressions, error_labels, error_clusters