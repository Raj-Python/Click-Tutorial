#!/usr/bin/env python
from .base import BaseTutorialLesson

class TestBasicTypes(BaseTutorialLesson):

    def test_00_cli_valid_int_option(self):
        result = self.run_command(['--int-option', '42'])
        assert "int: 42\n" in result.output

    def test_01_cli_invalid_int_option(self):
        result = self.run_command(['--int-option', '3.14'])
        assert "Invalid value" in result.output
        assert result.exit_code == 2

    def test_02_cli_valid_float_option(self):
        result = self.run_command(['--float-option', '3.14'])
        assert "float: 3.14\n" in result.output

    def test_03_cli_invalid_float_option(self):
        result = self.run_command(['--float-option', 'abcd'])
        assert "Invalid value" in result.output
        assert result.exit_code == 2

    def test_04_cli_valid_bool_option(self):
        result = self.run_command(['--bool-option', 'True'])
        assert "bool: True\n" in result.output

    def test_05_cli_invalid_bool_option(self):
        result = self.run_command(['--bool-option', '3.14'])
        assert "Invalid value" in result.output
        assert result.exit_code == 2

