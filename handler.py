import re
import os
from datetime import timedelta


class Subtitle:

    counter = 0
    difference = ''
    difference_forward = True

    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(self.file_path, 'r', encoding='utf-8')
        self.lines = self.file.readlines()
        self.file.close()
        self.dialogues = []
        self.get_dialogues()

    def get_dialogues(self):
        for i in range(len(self.lines)):
            if self.lines[i].startswith('Dialogue:'):
                self.dialogues.append([i, self.lines[i]])

    @staticmethod
    def convert_to_time(time):
        time = re.findall(r'\d+', time)
        time = list(map(int, time))
        return time

    @staticmethod
    def convert_time_to_ms(time):
        return time[0] * 21600000 + time[1] * 6000 + time[2] * 100 + time[3]

    @staticmethod
    def calculate_time(number1, number2, forward):
        '''
        number1: start time/end time
        number2: shift time
        [0] - hours
        [1] - minutes
        [2] - seconds
        [3] - milliseconds
        '''
        hours = 0
        minutes = 0
        seconds = 0
        if forward:
            milliseconds = number1[3] + number2[3]
            if milliseconds >= 100:
                seconds += 1
                milliseconds -= 100
            seconds += number1[2] + number2[2]
            if seconds >= 60:
                minutes += 1
                seconds -= 60
            minutes += number1[1] + number2[1]
            if minutes >= 60:
                hours += 1
                minutes -= 60
            hours += number1[0] + number2[0]
        else:
            milliseconds = number1[3] - number2[3]
            if milliseconds < 0:
                seconds -= 1
                milliseconds += 100
            seconds += number1[2] - number2[2]
            if seconds < 0:
                minutes -= 1
                seconds += 60
            minutes += number1[1] - number2[1]
            if minutes >= 60:
                hours += 1
                minutes -= 60
            hours += number1[0] - number2[0]

        if hours < 0 or minutes < 0 or seconds < 0 or milliseconds < 0:
            print('Out of range. Try to input correct timing')
            exit(0)

        return '{}:{}:{}.{}'.format(
            str(hours).zfill(2),
            str(minutes).zfill(2),
            str(seconds).zfill(2),
            str(milliseconds).zfill(2)
        )

    def shift_time_by_time(self, forward=True, shift_time='00:00:00.00'):
        shift_time = self.convert_to_time(shift_time)
        for i in range(len(self.dialogues)):
            dialog_line = self.dialogues[i][1].split(',')
            start_time = self.convert_to_time(dialog_line[1])
            end_time = self.convert_to_time(dialog_line[2])
            dialog_line[1] = self.calculate_time(start_time, shift_time, forward)
            dialog_line[2] = self.calculate_time(end_time, shift_time, forward)
            self.dialogues[i][1] = ','.join(dialog_line)

    def line_difference(self, line_number, second_time='00:00:00.00'):
        dialog_line = self.dialogues[line_number][1].split(',')
        first_time = self.convert_to_time(dialog_line[1])
        second_time = self.convert_to_time(second_time)
        forward = True
        if self.convert_time_to_ms(first_time) > self.convert_time_to_ms(second_time):
            difference = self.calculate_time(first_time, second_time, False)
            forward = False
        else:
            difference = self.calculate_time(first_time, second_time, False)

        return [difference, forward]

    @classmethod
    def change_counter(cls):
        cls.counter += 1
        return cls.counter

    def rename(self, mask, regex, folder):
        counter = self.change_counter()
        file_name = mask.replace('{}', str(counter).zfill(len(regex))) + '.ass'
        file_name = os.path.join(folder, file_name)
        os.rename(self.file_path, file_name)
        if os.name == 'nt':
            tmp = self.file_path.split('\\')[-1]
        else:
            tmp = self.file_path.split('/')[-1]
        print('File "{}" successfully renamed'.format(tmp))

    def save(self):
        output_file = open(self.file_path, 'w', encoding='utf-8')
        for i in self.dialogues:
            self.lines[i[0]] = i[1]

        for i in self.lines:
            output_file.write(i)

        output_file.close()

