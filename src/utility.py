from shlex import split as shlex_split
from datetime import datetime
from abc import ABC, abstractmethod
import re
from dateutil import parser


class RecordValidator(object):
    @staticmethod
    def validate(record_in):
        pattern = re.compile(r'^\S+\s+\S+\s+\S+\s+\'[^\']+\'\s+:\S+$')
        return bool(pattern.match(record_in))
    
class DateParser(object):
    @staticmethod
    def parse(date_in):
        return parser.parse(date_in).strftime("%Y/%m/%d")


class TimeTracker(object):
    def record(self, inputs):
        print(inputs)
        date, start_time, end_time, task, tag = inputs
        #TODO: implement entry to SQLite
        print(f"Recorded: {date} {start_time} - {end_time} - {task} - {tag}")

    def query(self, parameter):
        #TODO: implementation to query from SQLite
        print(f"Query: {parameter}")

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class RecordCommand(Command):
    def __init__(self, inputs):
        self.time_tracker = TimeTracker()
        self.record_validator = RecordValidator()
        self.date_parser = DateParser()
        self.input = inputs

    def execute(self):
        if self.record_validator.validate(self.input):
            inputs = shlex_split(self.input)
            if inputs[0].lower() == 'today':
                inputs[0] = datetime.now().strftime("%Y/%m/%d")
            else:
                inputs[0] = self.dateself.date_parser.parse(inputs[0])
            self.time_tracker.record(inputs)
        else:
            print("Invalid record input format. Please use DATE FROM TO TASK TAG format")

class Console(object):
    def __init__(self):
        self.time_tracker = TimeTracker()
        self.record_validator = RecordValidator()
        self.date_parser = DateParser()
        self.commands = []

    def addCommand(self, command):
        self.commands.append(command)

    def runCommands(self):
        for command in self.commands:
            command.execute()
    
    def processCommand(self, user_in):
        if user_in.startswith("query "):
            #TODO: implement query
            pass
        elif user_in.startswith("record "):
            record_in = user_in[len("record "):]
            self.addCommand(RecordCommand(record_in))