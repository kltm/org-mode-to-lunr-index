####
#### Seed code taken from ChatGPT prompt.
####

import json
import re
import logging
import os
import argparse
import sys

###
### kltm boilerplate.
###

## Logger basic setup.
logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger('bulk-convert')
LOG.setLevel(logging.WARNING)

def die(instr):
    """Die a little inside."""
    LOG.error(instr)
    sys.exit(1)

def main():
    """The main runner for our script."""

    ## Deal with incoming.
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='More verbose output')
    parser.add_argument('-f', '--file',
                        help='[optional] The local file to use in an action.')
    # parser.add_argument('-o', '--output',
    #                     help='[optional] The local file to use in an action.')

    args = parser.parse_args()

    ## Verbose toggle.
    if args.verbose:
        LOG.setLevel(logging.INFO)
        LOG.info('Verbose: on')

    # ## Check JSON output file.
    # if args.output:
    #     LOG.info('Will output to: ' + args.output)
    # else:
    #     die('need output file')

    ## Convert the filename into a referential base for use later on.
    filename = None
    if args.file:
        #filename = os.path.basename(args.file)
        filename = args.file
        LOG.info('Will parse: ' + filename)
    else:
        die('need input file')

    ## Basic parse. First, cleanse the file of non-entries for an easier second
    ## pass.
    filtered_lines = []
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:

            ## Read ahead until we get real data.
            if re.match(r"^\#", line): # skip heading comments
                continue
            elif re.match(r"^\* ", line): # skip month section headers
                continue
            # elif re.match(r"^\** ", line): # pause on daily, grab date
            #     continue
            else:
                filtered_lines.append(line)

    cleansed_text = "".join(filtered_lines)

    ## Now use the fact that we have highly uniform text to make grabbing days
    ## easier.
    docs = []
    #print(cleansed_text)
    #LOG.info(len(cleansed_text.split('^** ')))
    LOG.info(len(re.split(r'\n\*\* ', cleansed_text)))
    for day_blob in re.split(r'\n\*\*\ ', cleansed_text):
        #day_blob = day_blob.strip()
        if not day_blob:
            continue
        elif re.match(r'^\*\*\ ', day_blob): # trim the initial item
            day_blob = day_blob[3:]

        ## Get the day.
        day = None
        day_blob_lines = day_blob.split('\n')
        day = day_blob_lines[0]
        ## Continue "trick" as above.
        day_blob_wo_date = "\n".join(day_blob_lines[1:])

        for entry in re.split(r'\n\*\*\*\ ', day_blob_wo_date):
            if not entry:
                continue
            elif re.match(r'^\*\*\*\ ', entry): # trim the initial item
                entry = entry[4:]

                ## Get the title.
                title = None
                entry_lines = entry.split('\n')
                title = entry_lines[0]
                ## Continue "trick" as above.
                entry_body = "\n".join(entry_lines[1:])

                ## Assembly.
                docs.append({
                    #"status": None,
                    "date": day.strip(),
                    "title": title.strip(),
                    #"tags": [tag.strip()],
                    "text": entry_body
                })

    json_data = json.dumps(docs, indent=4)
    print(json_data)

## You saw it coming...
if __name__ == '__main__':
    main()
