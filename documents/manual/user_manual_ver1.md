# User Manual

## Record Feature

### Introduction

The record feature allows users to input activities that they completed.
To input simply run 'python program.py record {command}' in the CUI.
Command takes DATE FROM TO TASK :TAG format.

### List of possible commands

* record today 09:30 10:00 'Studied Python' :STUDY
* record 2023/12/11 11:00am 1:00pm 'Studied Java' :STUDY
* record 12/08/2023 1:00pm 4:00pm 'Lifted Weights' :WORKOUT

## Query Feature

### Introduction

The query feature allows users to query from thier past records.
To query run 'python program.py query {command}' in the CUI.

### List of possible commands

* query today
* query 12/03/2023
* query 2023/12/08
* query :STUDY