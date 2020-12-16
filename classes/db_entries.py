#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@Created On: Sep 3rd, 2020
@Author: Smith Joshua 
@Email: joshua.smith.228@us.af.mil

@updated On:
@Updated By:
@Email:

@db_entries: Object class for database entries.

"""
import decimal
from collections import OrderedDict


class db_table_entry(object):
    def __init__(self, table_name, values):
        self.values = OrderedDict()
        self.table_name = table_name

        for key, value in values.items():
            if type(value) == decimal.Decimal or type(value) == float:
                self.values[key] = float(value)
            elif type(value) == int:
                self.values[key] = value
            elif type(value) == bool:
                self.values[key] = value
            elif type(value) == list:
                self.values[key] = value
            elif value.isdigit() or value.startswith('-') and value[1:].isdigit():
                self.values[key] = int(value)
            else:
                self.values[key] = value

    def __str__(self):
        to_return = ""
        for key, value in self.values.items():
            if value is None:
                value = "null"
            else:
                value = str(value)
            to_return += str(key) + " : " + value + ", "

        return to_return[:-2]

    def get_values(self):
        return list(self.values.values())

    def get_fields(self):
        return list(self.values.keys())

