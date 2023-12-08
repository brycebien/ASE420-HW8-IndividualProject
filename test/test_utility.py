from datetime import datetime, timedelta
import pytest
from src.utility import DateParser, RecordSorter
from unittest.mock import Mock

def test_DateParserToday():
    assert DateParser.parse('today') == datetime.now().strftime("%Y/%m/%d")

def test_DateParserDate():
   assert DateParser.parse('12/12/23') == '2023/12/12'

def test_DateParserDaysBetween():
    assert DateParser.daysBetween('12/12/23', '12/15/23') == ['2023/12/12', '2023/12/13', '2023/12/14', '2023/12/15']

def test_RecordSorterRecordSort():
    records = [('1', '2023/12/12', '10:00', '12:00', 'studied', ':STUDY'), ('2', '2023/12/12', '10:00', '3:00', 'studied', ':STUDY'), ('3', '2023/12/12', '12:00', '2:00', 'studied', ':STUDY')]
    assert RecordSorter.recordSort(records) == [('2', '2023/12/12', '10:00', '3:00', 'studied', ':STUDY'), ('3', '2023/12/12', '12:00', '2:00', 'studied', ':STUDY'),('1', '2023/12/12', '10:00', '12:00', 'studied', ':STUDY')]

def test_RecordSorterGetDifferenceInTime():
    assert RecordSorter.getDifferenceInTime('12:00pm','1:00pm') == timedelta(seconds=3600)