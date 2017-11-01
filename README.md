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
```
