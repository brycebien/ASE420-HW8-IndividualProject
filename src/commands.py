import argparse
from datetime import datetime
from shlex import split as shlex_split
from abc import ABC, abstractmethod
import re
from dateutil import parser
from src.database import Database, QueryDatabase, RecordDatabase, DeleteDatabase
    
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DateParser(object):
    @staticmethod
    def parse(date_in):
        try:
            if date_in.lower() == 'today':
                return datetime.now().strftime("%Y/%m/%d")
            return parser.parse(date_in).strftime("%Y/%m/%d")
        except ValueError:
            return None
    
class DatabaseManager(object):
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


class DeleteCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()
    def execute(self):
        self.db_manager.delete()

class QueryCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.date_parser = DateParser()
    
    def execute(self, command):
        if command.query.startswith(':'):
            print('query a tag')
        elif self.date_parser.parse(command.query) is not None:
            print('query by date')
        else: print(f'query sting:{command.query}')


class RecordCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.date_parser = DateParser()

    def execute(self, command):
        date = self.date_parser.parse(command.date)
        start_time = command.start_time
        end_time = command.end_time
        task = command.task
        if not command.tag.startswith(':'):
            tag = ':' + command.tag.upper()
        else:
            tag = command.tag.upper()

        print(f'ARGS::{date},{start_time},{end_time},{task},{tag}')

class Console(object):
    def __init__(self):
        self.record_manager = RecordCommand()
        self.query_manager = QueryCommand()
        self.delete_manager = DeleteCommand()

    def processCommand(self, command):
        if command.command == 'record':
            return self.record_manager.execute(command)
        if command.command == 'query':
            return self.query_manager.execute(command)
        if command.command == 'delete':
            return self.delete_manager.execute()
        
    def parseArgs(self):
        parser = argparse.ArgumentParser(description='Time Tracker')
        subparsers = parser.add_subparsers(dest='command', help='Commands')

        record_parser = subparsers.add_parser('record', help='Record a task')
        record_parser.add_argument('date', help='Enter Date (any format) or "today"')
        record_parser.add_argument('start_time', help='Enter a start time for the task')
        record_parser.add_argument('end_time', help='Enter a end time for the task')
        record_parser.add_argument('task', help='Enter what task you did enclosed with \' \'')
        record_parser.add_argument('tag', help='Enter a tag - tags must start with a :')

        query_parser = subparsers.add_parser('query', help='Enter query :TAG or DATE or \'TASK\'')
        query_parser.add_argument('query', help='Enter query :TAG or DATE or \'TASK\'')

        delete_parser = subparsers.add_parser('delete', help='Drop records from db')
        delete_parser.add_argument('drop_table', help='Drops all records in db')


        return parser.parse_args()