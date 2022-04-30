import argparse
from generate_error import error

def gen_eda(input_file, output_file):

    writer = open(output_file, 'w')
    lines = open(input_file, 'r').readlines()

    for i, line in enumerate(lines):
        sentence = line
        aug_sentences = error(sentence)
        for aug_sentence in aug_sentences:
            writer.write(aug_sentence + '\n')

    writer.close()
    print("generated augmented sentences with eda for " + train_orig + " to " + output_file + " with num_aug=" + str(num_aug))
    
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