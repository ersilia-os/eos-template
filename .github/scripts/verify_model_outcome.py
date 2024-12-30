import csv

def is_null_value(value):
    if value in ['', None, 'None']:
        return True
    return False

def check_null_outcomes_in_output_csv(csv_file_path):
    """
    Check if all outcomes in the output csv file are null
    Returns True if all outcomes are null, False otherwise
    """
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        row = next(csv_reader)
        for val in row[2:]: # Skip the first two columns (Inchikey and input)
            if isinstance(val, str):
                # Handle "['None', ' None',  'None', ...]" case
                val = val.replace('[', '').replace(']', '').split(',')
                val = [v.strip() for v in val]
            
            if isinstance(val, list):
                for v in val:
                    if not is_null_value(v):
                        return False
            else:
                if not is_null_value(val):
                    return False
    return True

if __name__ == '__main__':
    # Read file path from command line
    import sys
    if len(sys.argv) < 2:
        print('Usage: python verify_model_output.py <output_csv_file>')
        exit(1)

    output_csv_file = sys.argv[1]

    if check_null_outcomes_in_output_csv(output_csv_file):
        # If there are null outcomes, exit with status code 1
        print('All outcomes are null')
    else:
        print('Some outcomes are not null')

