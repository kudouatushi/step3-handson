"""textutil のテスト。

Arrange-Act-Assert で書く。1テスト1振る舞い。テスト名は日本語で読める形。
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from textutil import normalize_spaces, strip_control


class TestStripControl(unittest.TestCase):
    def test_制御文字を取り除く(self):
        # Arrange
        text = "abc\x00def\x07ghi"

        # Act
        actual = strip_control(text)

        # Assert
        self.assertEqual(actual, "abcdefghi")

    def test_タブと改行は残す(self):
        # Arrange
        text = "a\tb\nc\rd"

        # Act
        actual = strip_control(text)

        # Assert
        self.assertEqual(actual, "a\tb\nc\rd")


class TestNormalizeSpaces(unittest.TestCase):
    def test_連続する半角スペースを1つに畳む(self):
        # Arrange
        text = "a   b  c"

        # Act
        actual = normalize_spaces(text)

        # Assert
        self.assertEqual(actual, "a b c")

    def test_全角スペースとタブも畳む(self):
        # Arrange
        text = "a　　b\t\tc"

        # Act
        actual = normalize_spaces(text)

        # Assert
        self.assertEqual(actual, "a b c")

    def test_行頭行末の空白を落とし改行は保持する(self):
        # Arrange
        text = "  a  \n  b  "

        # Act
        actual = normalize_spaces(text)

        # Assert
        self.assertEqual(actual, "a\nb")


if __name__ == "__main__":
    unittest.main()
