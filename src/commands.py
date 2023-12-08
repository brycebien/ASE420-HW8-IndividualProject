import argparse
from datetime import datetime
from abc import ABC, abstractmethod
from dateutil import parser
from src.database import Database, QueryDatabase, RecordDatabase, DeleteDatabase

DATABASE = 'HW-8.db'
    
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DateParser(object):
    @staticmethod
    def parse(date_in):
        try:
            if date_in.lower() == 'today': return datetime.now().strftime("%Y/%m/%d")
            return parser.parse(date_in).strftime("%Y/%m/%d")
        except ValueError:
            return None
    
class DatabaseManager(object):
    def __init__(self):
        self.database = Database(DATABASE)
        self.query_database = QueryDatabase(DATABASE)
        self.record_database = RecordDatabase(DATABASE)
        self.delete_database = DeleteDatabase(DATABASE)

    def record(self, inputs):
        print(inputs)
        self.record_database.record(inputs)

    def query(self, parameter, method): 
        if method == 'date':
            self.query_database.queryDate(parameter)
        elif method == 'tag':
            self.query_database.queryTag(parameter)
        else:
            self.query_database.queryTask(parameter)

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
        if self.date_parser.parse(command.query) is not None:
            self.db_manager.query(self.date_parser.parse(command.query), 'date')
        elif command.query.startswith(':'):
            self.db_manager.query(command.query.upper(), 'tag')
        else:
            self.db_manager.query(command.query, 'task')


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

        self.db_manager.record([date,start_time,end_time,task,tag])
        print(f'ARGS::{date},{start_time},{end_time},{task},{tag}')

class Console(object):
    def __init__(self):
        self.record_manager = RecordCommand()
        self.query_manager = QueryCommand()
        self.delete_manager = DeleteCommand()

    def run(self):
        args = self.__parseArgs()
        self.__processCommand(args)

    def __processCommand(self, command):
        if command.command == 'record':
            return self.record_manager.execute(command)
        if command.command == 'query':
            return self.query_manager.execute(command)
        if command.command == 'delete':
            return self.delete_manager.execute()
        
    def __parseArgs(self):
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