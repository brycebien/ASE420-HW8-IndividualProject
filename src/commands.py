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
    def daysBetween(start, end):
        start_str = DateParser.parse(start)
        end_str = DateParser.parse(end)

        start = datetime.strptime(start_str, '%Y/%m/%d')
        end = datetime.strptime(end_str, '%Y/%m/%d')
        difference = end - start
        return [(start + timedelta(days=i)).date().strftime('%Y/%m/%d') for i in range(difference.days + 1)]
    
class RecordSorter(object):
    @staticmethod
    def recordSort(records):
        times = []
        for record in records:
            times.append(RecordSorter.getDifferenceInTime(record[2], record[3]).seconds)

        for i in range(len(times)):
            times[i] = timedelta(seconds=times[i])
        
        res = list(zip(records, times))
        res.sort(key=lambda record: record[1], reverse=True)

        return [record for record, _ in res]      

    @staticmethod
    def getDifferenceInTime(start, end):
        if 'am' in start.lower() or 'pm' in start.lower() or 'am' in end.lower() or 'pm' in end.lower():
            start_time = datetime.strptime(start, '%I:%M%p')
            end_time = datetime.strptime(end, '%I:%M%p')
        else:
            start_time = datetime.strptime(start, '%H:%M')
            end_time = datetime.strptime(end, '%H:%M')
        return end_time - start_time

    
class DatabaseManager(object):
    def __init__(self):
        self.__database = Database(DATABASE)
        self.__query_database = QueryDatabase(DATABASE)
        self.__record_database = RecordDatabase(DATABASE)
        self.__delete_database = DeleteDatabase(DATABASE)

    def record(self, inputs):
        self.__record_database.record(inputs)

    def query(self, parameter, method): 
        if method == 'date':
            self.__query_database.queryDate(parameter)
        elif method == 'tag':
            self.__query_database.queryTag(parameter)
        else:
            self.__query_database.queryTask(parameter)
    
    def queryAll(self):
        return self.__query_database.queryAll()

    def delete(self):
        self.__delete_database.delete()


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