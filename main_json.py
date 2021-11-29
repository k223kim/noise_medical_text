import argparse
from generate_error import error
import json

def gen_eda(intput_file, output_file):
    with open(output_file, 'w') as out:
        total_output = []
        with open(intput_file) as f:
            total_data = json.load(f)
        for data in total_data:
            output = {}
            output['study_id'] = data['study_id']
            output['subject_id'] = data['subject_id']
            output['findings'] = data['findings']
            #generate error only for the impressions
            impression = data['impression']
            error_impression = error(impression)
            output['impression'] = error_impression
            output['background'] = data['background']
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