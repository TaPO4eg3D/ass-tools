import sys
import os
import re
from handler import Subtitle


def is_valid(file_str):
    if file_str.endswith('.ass'):
        return True
    print('Not valid format, you can work only with .ass files')
    return False


# Check time format
def is_time_valid(time):
    time = re.findall(r'\d+', sys.argv[4])
    if len(time) != 4:
        return False
    for i in time:
        if len(i) < 2:
            return False

    return True


def shift_by_time(subtitle):
    forward = True
    if sys.argv[3] == '-forward':
        pass
    elif sys.argv[3] == '-backward':
        forward = False
    else:
        print('Unknown parameter, for this option only -forward and -backward available')
        exit(0)

    if not is_time_valid(sys.argv[4]):
        print('Incorrect format of time. Time should be like 00:00:00.00')
        exit(0)

    subtitle.shift_time_by_time(forward, sys.argv[4])
    subtitle.save()
    delimiter = '+'
    if not forward:
        delimiter = '-'
    print('Shifting is done: ' + delimiter + sys.argv[4])


def shift_by_line(subtitle):
    subtitle.shift_time_by_first_line(sys.argv[3])
    subtitle.save()


def multiple_rename(subtitle, mask, regex):
    if not re.search('{}', mask):
        print('Enter correct mask')
        exit(0)
    subtitle.rename(mask[1:-1], regex, sys.argv[1])  # The last one is folder


# Handle parameters
def parameters(file, is_dir=False):
    subtitle = Subtitle(file)
    if sys.argv[2] == '--sbt':
        shift_by_time(subtitle)
    elif sys.argv[2] == '--rename':
        if not is_dir:
            print('Only directory allowed')
            exit(0)
        args = sys.argv[3:-1]
        args = ' '.join(args)
        multiple_rename(subtitle, args, sys.argv[-1])
    elif sys.argv[2] == '--sbl':
        if is_dir:
            print('Directory is not allowed')
            exit(0)
        shift_by_line(subtitle)
    else:
        print('Unknown option, type "--help" for list of available options')
        exit(0)


# Check on file or dir
if sys.argv[1] == '--help':
    print(
        """
Script takes parameters in order:
    file/folder --[function] -[parameter](if function has one) [time]
Example:
    asst subtitle_folder --sbt -forward 00:00:01.10

All available functions:
    --help  - display this page
    --sbt   - shift times accept extra arguments:
        -forward    - shift times forward
        -backward   - shift times backward
    --sbl - calculate difference between first dialog and input, then shift times
            Accept only one file, folder is not allowed
    --rename - rename all files in folder. Accepts mask and regex
               Mask example: 'ShowName - {}', where '{}' is counter
               Regex example: dd, regex defines counter format, in this case
                              counter would be 01, 02, 03 and so on..
    Example of --rename:
    asst subtitle_folder --rename '[SubGroup]Anime - {}' dd
    
        result of this command would be:
            [SubGroup]Anime - 01.ass
            [SubGroup]Anime - 02.ass
            [SubGroup]Anime - 03.ass
            And so on...
        """
    )
    exit(0)
if not os.path.isdir(sys.argv[1]):
    if not is_valid(sys.argv[1]):
        pass
    else:
        parameters(sys.argv[1])
else:
    for file in os.listdir(sys.argv[1]):
        file_path = os.path.join(sys.argv[1], file)
        if not is_valid(file_path):
            pass
        else:
            parameters(file_path, True)