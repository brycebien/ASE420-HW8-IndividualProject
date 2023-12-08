import pytest
from src.commands import Console, PriorityCommand, ReportCommand, QueryCommand, RecordCommand, DeleteCommand, DatabaseManager
from unittest.mock import Mock

def test_recordCommandExecute(capsys):
    command = Mock(command='record',date='12/12/2023',start_time='10:00',end_time='11:00',task='Studied Java',tag=':STUDIED')
    RecordCommand().execute(command)
    cap = capsys.readouterr()
    assert "Recorded Record: 2023/12/12, 10:00, 11:00, 'Studied Java', :STUDIED\n" in cap.out

def test_queryCommandExecuteTag(capsys):
    command = Mock(command='query', query=':STUDIED')
    QueryCommand().execute(command)
    cap = capsys.readouterr()
    assert "(1, '2023/12/12', '10:00', '11:00', 'Studied Java', ':STUDIED')\n" in cap.out

def test_queryCommandExecuteTask(capsys):
    command = Mock(command='query', query='Studied Java')
    QueryCommand().execute(command)
    cap = capsys.readouterr()
    assert "No records found" not in cap.out

def test_queryCommandExecuteDate(capsys):
    command = Mock(command='query', query='12/12/2023')
    QueryCommand().execute(command)
    cap = capsys.readouterr()
    assert "No records found" not in cap.out

def test_queryCommandExecuteNoRecords(capsys):
    command = Mock(command='query', query='Nothing here')
    QueryCommand().execute(command)
    cap = capsys.readouterr()
    assert "No records found" in cap.out

def test_queryCommandExecuteQueryAll(capsys):
    PriorityCommand().execute()
    cap = capsys.readouterr()
    assert "No records found" not in cap.out

def test_deleteCommandExecute():
    DeleteCommand().execute()
    assert "All records have been deleted"