# ass-tools
CLI tools for working with .ASS subtitles 

```
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
```
