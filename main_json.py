import argparse
from generate_error import error
import json
import pandas as pd
from tqdm import tqdm
########################################################################
# Group different labels
########################################################################  
# def group_errors(total_data):
#     no_finding = []
#     enlarged_cardiomediastinum = []
#     cardiomegaly = []
#     lung_lesion = []
#     lung_opacity = []
#     edema = []
#     consolidation = []
#     pneumonia = []
#     atelectasis = []
#     pneumothorax = []
#     pleural_effusion = []
#     pleural_other = []
#     fracture = []
#     support_devices = []
#     for data in total_data:
#         if "No Finding" in data["label"]:
#             no_finding.append(data)
#         if "Enlarged Cardiomediastinum" in data["label"]:
#             enlarged_cardiomediastinum.append(data["study_id"])
#         if "Cardiomegaly" in data["label"]:
#             cardiomegaly.append(data["study_id"])
#         if "Lung Lesion" in data["label"]:
#             lung_lesion.append(data["study_id"])
#         if "Lung Opacity" in data["label"]:
#             lung_opacity.append(data["study_id"])
#         if "Edema" in data["label"]:
#             edema.append(data["study_id"])
#         if "Consolidation" in data["label"]:
#             consolidation.append(data["study_id"])
#         if "Pneumonia" in data["label"]:
#             pneumonia.append(data["study_id"])  
#         if "Atelectasis" in data["label"]:
#             atelectasis.append(data["study_id"])
#         if "Pneumothorax" in data["label"]:
#             pneumothorax.append(data["study_id"])  
#         if "Pleural Effusion" in data["label"]:
#             pleural_effusion.append(data["study_id"])  
#         if "Pleural Other" in data["label"]:
#             pleural_other.append(data["study_id"])   
#         if "Fracture" in data["label"]:
#             fracture.append(data["study_id"])   
#         if "Support Devices" in data["label"]:
#             support_devices.append(data["study_id"]) 
#     labels = [no_finding, enlarged_cardiomediastinum, cardiomegaly, lung_lesion, lung_opacity, edema, consolidation, pneumonia, atelectasis, pneumothorax, pleural_effusion, pleural_other, fracture, support_devices]
#     return labels
            
    
def gen_eda(input_file, output_file):
    with open(output_file, 'w+') as out:
        total_output = []
        with open(input_file) as f:
            total_data = json.load(f)
        df = pd.read_json(input_file)
#         total_labels = group_errors(total_data)
        for data in tqdm(total_data):
#             import pdb;pdb.set_trace()
            output = {}
            output['study_id'] = data['study_id']
            output['subject_id'] = data['subject_id']
#             output["uid"] = data["uid"]
#             output["MeSH"] = data["MeSH"]
#             output["Problems"] = data["Problems"]
#             output["image"] = data["image"]
#             output["indication"] = data["indication"]
#             output["comparison"] = data["comparison"]
            # output['findings'] = data['findings']
            #generate error only for the impressions
#             impression = data['impression']
            error_findings, error_impression, error_label = error(df, data)
            output['findings'] = error_findings
            output['impression'] = error_impression
            output['background'] = data['background']
            output['label'] = data['label']
            output['error_label'] = error_label
#             import pdb;pdb.set_trace()
            total_output.append(output)
        json.dump(total_output, out)
#     print("generated augmented sentences with eda for " + train_orig + " to " + output_file + " with num_aug=" + str(num_aug))
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=str, help="input file of unaugmented data")
    parser.add_argument("--output", required=False, type=str, help="output file of unaugmented data")
    args = parser.parse_args()
    if args.output:
        output = args.output
    else:
        from os.path import dirname, basename, join
        output = join(dirname(args.input), 'eda_' + basename(args.input))    
    gen_eda(args.input, output)
    
if __name__ == "__main__":
    main()