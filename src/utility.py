from abc import abstractmethod
from datetime import datetime


class CommandHandler(object):
    def __init__(self):
        pass

class Record(CommandHandler):
    def record(self, inputs):
        self.checkCommand(inputs)

    def checkCommand(self, inputs):
        checked_inputs = []
        format = '%Y/%m/%d'
        try:
            datetime.strptime(inputs[0],format)
            checked_inputs.append(datetime.strptime(inputs[0],format).date())
        except ValueError:
            print('Invalid Date Time Format please enter YYYY/MM/DD')
            return None



