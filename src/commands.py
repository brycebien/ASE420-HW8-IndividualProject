import argparse
from datetime import datetime, timedelta
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
        
    @staticmethod
    def days_between(start, end):
        start_str = DateParser.parse(start)
        end_str = DateParser.parse(end)

        start = datetime.strptime(start_str, '%Y/%m/%d')
        end = datetime.strptime(end_str, '%Y/%m/%d')
        difference = end - start
        return [(start + timedelta(days=i)).date().strftime('%Y/%m/%d') for i in range(difference.days + 1)]

    
class DatabaseManager(object):
    def __init__(self):
        self.database = Database(DATABASE)
        self.query_database = QueryDatabase(DATABASE)
        self.record_database = RecordDatabase(DATABASE)
        self.delete_database = DeleteDatabase(DATABASE)

    def record(self, inputs):
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
        self.db_manager = DatabaseManager()

    def execute(self, command):
        res = DateParser.days_between(command.start_date, command.end_date)
        for day in res:
            self.db_manager.query(day, 'date')
        #query every date from start date to end date and add to list

        #print list?
        #self.query_database()


class Console(object):
    def __init__(self):
        self.record_manager = RecordCommand()
        self.query_manager = QueryCommand()
        self.delete_manager = DeleteCommand()
        self.report_manager = ReportCommand()

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


        return parser.parse_args()