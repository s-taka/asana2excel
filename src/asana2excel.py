# -*- coding: utf-8 -*-

import pprint
import argparse

import csv
import json

from openpyxl import Workbook
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.chart import LineChart
from openpyxl.chart import Reference

import logging
import re
import datetime

import sys

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def read_dependencies(asana_csv):
    blocked_by = {}
    blocking = {}
    with open(asana_csv) as csvfile:
        asana_csv_in = csv.reader(csvfile, dialect=csv.excel)
        for row in asana_csv_in:
            blocked_by[row[0]] = row[14]
            blocking[row[0]] = row[15]
    return blocked_by, blocking

def main():
    tmplate_excel_file = 'template.xlsx'

    parser = argparse.ArgumentParser(description='run for cache modules')
    parser.add_argument('json_file', help='a json file exported from asana')
    parser.add_argument('csv_file', help='a csv file exported from asana')
    parser.add_argument('out_excel_file', help='output wbs')

    args = parser.parse_args()
    json_file = args.json_file
    csv_file = args.csv_file
    out_excel_file = args.out_excel_file

    blocked_by, blocking = read_dependencies(csv_file)
    with open(json_file) as in_data:
        asana_data = json.load(in_data)

    write_column_def = {
        'section': 'B',
        'task_name_level': ['C','D','E'],
        'start_on': 'G',
        'due_on': 'H',
        'assignee': 'I',
        'completed': 'K',
        'completed_at': 'L',
        'link': 'M',
        'blocked_by': 'O',
        'blocking': 'P'
    }
    start_row = 5

    wb = load_workbook(tmplate_excel_file)
    wb_wbs = wb['WBS']
    current_info = {'current_row': start_row, 'current_section': ''}
 
    def write_wbs(tasks, current_level, max_level):
        if current_level > max_level:
            return
        for i, task in enumerate(tasks):
            task_name = task['name']
            try:
                start_on =  datetime.datetime.strptime(task['start_on'], '%Y-%m-%d')
            except:
                start_on = ''

            try:
                due_on = datetime.datetime.strptime(task['due_on'], '%Y-%m-%d')
            except:
                due_on = ''
            permalink_url = task['permalink_url']

            completed = '〇' if task['completed'] else ''
            try:
                completed_at = datetime.datetime.strptime(task['completed_at'][0:10], '%Y-%m-%d')
            except:
                completed_at = ''
            task_id = task['gid']
            try:
                assignee = task['assignee']['name']
            except:
                assignee = ''
            try:
                section_name = task['memberships'][0]['section']['name']
                if current_info['current_section'] != section_name:
                    print('{}, {}'.format(current_info['current_row'], section_name))
                    wb_wbs['{}{}'.format(write_column_def['section'], current_info['current_row'])] = section_name
                    current_info['current_section'] = section_name
                    current_info['current_row'] += 1
            except:
                pass
            print('{}, {} {} / {} - {} : {} [complete:{} in {}]   [{}]'.format(current_info['current_row'], '    ' * current_level, task_name, start_on, due_on, assignee, completed, completed_at, permalink_url))
            wb_wbs['{}{}'.format(write_column_def['task_name_level'][current_level], current_info['current_row'])] = task_name
            wb_wbs['{}{}'.format(write_column_def['start_on'], current_info['current_row'])] = start_on
            wb_wbs['{}{}'.format(write_column_def['due_on'], current_info['current_row'])] = due_on
            wb_wbs['{}{}'.format(write_column_def['assignee'], current_info['current_row'])] = assignee
            wb_wbs['{}{}'.format(write_column_def['completed'], current_info['current_row'])] = completed
            wb_wbs['{}{}'.format(write_column_def['completed_at'], current_info['current_row'])] = completed_at
            wb_wbs['{}{}'.format(write_column_def['link'], current_info['current_row'])] = permalink_url
            wb_wbs['{}{}'.format(write_column_def['blocked_by'], current_info['current_row'])] = blocked_by[task_id]
            wb_wbs['{}{}'.format(write_column_def['blocking'], current_info['current_row'])] = blocking[task_id]
            current_info['current_row'] += 1
            write_wbs(task['subtasks'], current_level + 1, max_level)
        return

    write_wbs(asana_data['data'], 0, 2)
    wb.save(out_excel_file)

    return

if __name__ == "__main__":
    main()