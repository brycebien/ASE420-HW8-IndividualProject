import pytest
from src.commands import Console, ReportCommand, QueryCommand, RecordCommand, DeleteCommand, DatabaseManager
from unittest.mock import Mock

def test_recordCommandExecute():
    command = Mock(command='record',date='12/12/2023',start_time='10:00',end_time='11:00',task='Studied Java',tag=':STUDIED')
    RecordCommand().execute(command)
    assert "Recorded Record: 2023/12/12, 10:00, 11:00, 'Studied Java', :STUDY"

def test_queryCommandExecuteTag():
    command = Mock(command='query', query=':STUDIED')
    QueryCommand().execute(command)
    assert "(1, 2023/12/12, 10:00, 11:00, 'Studied Java', :STUDY)"

def test_queryCommandExecuteTask():
    command = Mock(command='query', query='\'Studied Java\'')
    QueryCommand().execute(command)
    assert "(1, 2023/12/12, 10:00, 11:00, 'Studied Java', :STUDY)"

def test_queryCommandExecuteDate():
    command = Mock(command='query', query='12/12/2023')
    QueryCommand().execute(command)
    assert "(1, 2023/12/12, 10:00, 11:00, 'Studied Java', :STUDY)"

def test_queryCommandExecuteNoRecords():
    command = Mock(command='query', query='\'Nothing here\'')
    QueryCommand().execute(command)
    assert "No records found"

def test_deleteCommandExecute():
    DeleteCommand().execute()
    assert "All records have been deleted"