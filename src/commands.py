import argparse
from abc import ABC, abstractmethod
from src.database import Database, QueryDatabase, RecordDatabase, DeleteDatabase
from src.utility import DateParser, RecordSorter

DATABASE = 'HW-8.db'

class DatabaseManager(object):
    def __init__(self):
        self.__database = Database(DATABASE)
        self.__query_database = QueryDatabase(DATABASE)
        self.__record_database = RecordDatabase(DATABASE)
        self.__delete_database = DeleteDatabase(DATABASE)

    def record(self, inputs):
        self.__record_database.record(inputs)

    def query(self, parameter, method): 
        self.__query_database.query(parameter,method)
    
    def queryAll(self):
        return self.__query_database.queryAll()

    def delete(self):
        self.__delete_database.delete()

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class DeleteCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()
    def execute(self):
        self.db_manager.delete()

class QueryCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()
    
    def execute(self, command):
        if DateParser.parse(command.query) is not None:
            self.db_manager.query(DateParser.parse(command.query), 'date')
        elif command.query.startswith(':'):
            self.db_manager.query(command.query.upper(), 'tag')
        else:
            self.db_manager.query(command.query, 'task')

class RecordCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()

    def execute(self, command):
        date = DateParser.parse(command.date)
        start_time = command.start_time
        end_time = command.end_time
        task = command.task
        if not command.tag.startswith(':'):
            tag = ':' + command.tag.upper()
        else:
            tag = command.tag.upper()
        self.db_manager.record([date,start_time,end_time,task,tag])
        print(f'Recorded Record: {date}, {start_time}, {end_time}, \'{task}\', {tag}')

class ReportCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()

    def execute(self, command):
        res = DateParser.daysBetween(command.start_date, command.end_date)
        for day in res:
            print(f'{day}:')
            self.db_manager.query(day, 'date')

class PriorityCommand(Command):
    def __init__(self):
        self.db_manager = DatabaseManager()

    def execute(self):
        all_queries = self.db_manager.queryAll()
        records = RecordSorter.recordSort(all_queries)
        print('Tasks that took the most time from most to least:')
        for record in records:
            print(record)

class Console(object):
    def __init__(self):
        self.record_manager = RecordCommand()
        self.query_manager = QueryCommand()
        self.delete_manager = DeleteCommand()
        self.report_manager = ReportCommand()
        self.priority_manager = PriorityCommand()

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
        if command.command == 'report':
            return self.report_manager.execute(command)
        if command.command == 'priority':
            return self.priority_manager.execute()
        
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

        report_parser = subparsers.add_parser('report', help='Report all records')
        report_parser.add_argument('start_date', help='Start of date range for report')
        report_parser.add_argument('end_date', help='End of date range for report')

        priority_parser = subparsers.add_parser('priority', help='Return tasks that took up most of your time')

        return parser.parse_args()