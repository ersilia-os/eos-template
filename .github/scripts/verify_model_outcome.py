import csv

def check_non_null_outcomes_in_output_csv(csv_file_path):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        row = next(csv_reader)
        for val in row[2:]: # Skip the first two columns (Inchikey and input)
            if val not in ['', None]: # Returns if even one outcome is not null
                return False
    return True

if __name__ == '__main__':
    # Read file path from command line
    import sys
    if len(sys.argv) < 2:
        print('Usage: python verify_model_output.py <output_csv_file>')
        exit(1)

    output_csv_file = sys.argv[1]

    if check_non_null_outcomes_in_output_csv(output_csv_file):
        # If there are null outcomes, exit with status code 1
        print('All outcomes are null')
    else:
        print('Some outcomes are not null')

