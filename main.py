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
    time = re.findall(r'\d+', time)
    if len(time) != 4:
        return False
    for i in time:
        if len(i) < 2:
            return False

    return True


def shift_by_time(subtitle):

    subtitle.shift_time_by_time(forward, sys.argv[4])
    subtitle.save()
    delimiter = '+'
    if not forward:
        delimiter = '-'
    print('Shifting is done: ' + delimiter + sys.argv[4])


def smart_shift_handler(time_list):
    first = Subtitle.convert_to_time(time_list[0][0])
    first = Subtitle.convert_time_to_ms(first)
    for i in range(1, len(time_list)):
        current = Subtitle.convert_to_time(time_list[i][0])
        current = Subtitle.convert_time_to_ms(current)
        if first - current >= 50:
            return False

    return True


def smart_shift(subtitle):
    time = []
    steps = 0
    for i in range(len(subtitle.dialogues)):
        steps += 1
        second_subtitle_dialog = second_subtitle.dialogues[i][1].split(',')[1]  # Get start time of the line
        time.append(subtitle.line_difference(i, second_subtitle_dialog))
        if steps == 5:
            if smart_shift_handler(time):
                subtitle.shift_time_by_time(time[0][1], time[0][0])
                subtitle.save()
                delimiter = {
                    True: '+',
                    False: '-'
                }
                print('Shifting is done. Difference is {}{}'.format(
                    delimiter[time[0][1]],
                    time[0][0]
                ))
                exit(0)
            else:
                time.clear()
                steps = 0
    print("Can't do smart shifting...")


def multiple_rename(subtitle):
    subtitle.rename(mask[1:-1], regex, sys.argv[1])  # The last one is folder


def start(func):
    if not os.path.isdir(sys.argv[1]):
        if not is_valid(sys.argv[1]):
            pass
        else:
            func(Subtitle(sys.argv[1]))
    else:
        for file in os.listdir(sys.argv[1]):
            file_path = os.path.join(sys.argv[1], file)
            if not is_valid(file_path):
                pass
            else:
                func(Subtitle(file_path))


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
    --smart - automatically calculate difference between two files and shift times
              accordingly 
            Accept only one file, folder is not allowed
        Example:
        asst incorrect_timing.ass --smart correct_timing.ass
    --rename - rename all files in folder. Accepts mask, regex and counter start point
               Mask example: 'ShowName - {}', where '{}' is counter
               Regex example: dd, regex defines counter format, in this case
                              counter would be 01, 02, 03 and so on..
    Example of --rename:
    asst subtitle_folder --rename '[SubGroup]Anime - {}' dd 04
    
        result of this command would be:
            [SubGroup]Anime - 04.ass
            [SubGroup]Anime - 05.ass
            [SubGroup]Anime - 06.ass
            And so on...
        """
    )
    exit(0)

is_dir = True
if not os.path.isdir(sys.argv[1]):
    is_dir = False

if sys.argv[2] == '--sbt':
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

    start(shift_by_time)
elif sys.argv[2] == '--rename':  # Only for directories
    if not is_dir:
        print('Only directories are allowed')
        exit(0)

    try:
        Subtitle.counter = int(sys.argv[-1]) - 1
    except ValueError:
        print('Incorrect counter start point')
        exit(0)

    regex = sys.argv[-2]
    for i in regex:
        if i != 'd':
            print('Incorrect regex')
            exit(0)

    args = sys.argv[3:-2]
    mask = ' '.join(args)
    if mask[0] != "'" and mask[-1] != "'":
        print('Mask should be wrapped in single quotes')
        exit(0)
    if not re.search('{}', mask):
        print('Incorrect mask. Mask should contain at least one {}')
        exit(0)

    start(multiple_rename)
elif sys.argv[2] == '--smart':  # Only for a single file
    if is_dir:
        print('Only a single file allowed')
        exit(0)
    second_subtitle = Subtitle(sys.argv[3])
    start(smart_shift)
else:
    print('Unknown option, type "--help" for list of available options')
    exit(0)
