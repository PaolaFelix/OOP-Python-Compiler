import unittest
import ast
import tempfile
import os
from unittest.mock import patch
from unit_test import has_oop, check_file


class TestParserModule(unittest.TestCase):

    def test_has_oop_with_class(self):
        code = "class MyClass:\n    pass"
        tree = ast.parse(code)
        self.assertTrue(has_oop(tree))

    def test_has_oop_without_class(self):
        code = "def my_function():\n    pass"
        tree = ast.parse(code)
        self.assertFalse(has_oop(tree))

    def test_check_file_with_oop(self):
        code = "class MyClass:\n    pass"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        with patch('builtins.print') as mock_print:
            check_file(tmp_path)
            mock_print.assert_called_with(f"{tmp_path}: ACCEPTED")
        os.unlink(tmp_path)

    def test_check_file_without_oop(self):
        code = "def func():\n    pass"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        with patch('builtins.print') as mock_print:
            check_file(tmp_path)
            mock_print.assert_called_with(f"{tmp_path}: REJECTED (No OOP structure found)")
        os.unlink(tmp_path)

    def test_check_file_with_syntax_error(self):
        code = "def bad(:\n    pass"
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name

        with patch('builtins.print') as mock_print:
            check_file(tmp_path)
            self.assertTrue(any("Syntax Error" in str(call) for call in mock_print.call_args_list))
        os.unlink(tmp_path)


if __name__ == '__main__':
    unittest.main()
