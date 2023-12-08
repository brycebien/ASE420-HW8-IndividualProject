from datetime import datetime, timedelta
from dateutil import parser

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
