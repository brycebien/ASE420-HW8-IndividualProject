from datetime import datetime
from shlex import split as shlex_split
from abc import ABC, abstractmethod
import re
from dateutil import parser
from src.database import Database, QueryDatabase, RecordDatabase, DeleteDatabase


class RecordValidator(object):
    @staticmethod
    def validate(record_in):
        pattern = re.compile(r'^\S+\s+\S+\s+\S+\s+\'[^\']+\'\s+:\S+$')
        return bool(pattern.match(record_in))
    
class QueryValidator(object):
    @staticmethod
    def validate(query_in):
        pattern = re.compile(r"^(?:today|\d{1,2}/\d{1,2}/\d{4}|\d{4}/\d{1,2}/\d{2}|'[^']*')?$")
        return bool(pattern.match(query_in.strip()))
    
class DateParser(object):
    @staticmethod
    def parse(date_in):
        try:
            return parser.parse(date_in).strftime("%Y/%m/%d")
        except ValueError:
            return None
    
class TimeTracker(object):
    def __init__(self):
        self.database = Database('HW-8.db')
        self.query_database = QueryDatabase('HW-8.db')
        self.record_database = RecordDatabase('HW-8.db')
        self.delete_database = DeleteDatabase('HW-8.db')

    def record(self, inputs):
        print(inputs)
        date, start_time, end_time, task, tag = inputs
        tag = tag.upper()
        self.record_database.record(date, start_time, end_time, task, tag)

    def query(self, parameter):
        if parameter[0].startswith(':'):
            parameter[0] = parameter[0].upper() 
        res = self.query_database.query(parameter[0])
        print(res)

    def delete(self):
        self.delete_database.delete()

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DeleteCommand(Command):
    def __init__(self, inputs):
        self.input = inputs
        self.time_tracker = TimeTracker()
    def execute(self):
        self.time_tracker.delete()

class QueryCommand(Command):
    def __init__(self, inputs):
        self.time_tracker = TimeTracker()
        self.query_validator = QueryValidator()
        self.date_parser = DateParser()
        self.input = inputs
    
    def execute(self):
        if self.query_validator.validate(self.input):
            inputs = shlex_split(self.input)
            date = self.date_parser.parse(inputs[0])
            if date is not None:
                self.time_tracker.query([date])
            else:
                self.time_tracker.query(inputs)
        else:
            print("Invalid query input format. Please use query DATE, query today, or query :TAG format")


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
                inputs[0] = self.date_parser.parse(inputs[0])
            self.time_tracker.record(inputs)
        else:
            print("Invalid record input format. Please use DATE FROM TO TASK :TAG format")

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
            record_in = user_in[len("query "):]
            self.addCommand(QueryCommand(record_in))
        elif user_in.startswith("record "):
            record_in = user_in[len("record "):]
            self.addCommand(RecordCommand(record_in))
        elif user_in == "drop":
            self.addCommand(DeleteCommand(user_in))