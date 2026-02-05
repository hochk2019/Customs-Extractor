
import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractor_core_v2 import ExportExtractor, ImportExtractor, BaseExtractor

class TestCustomsExtractor(unittest.TestCase):

    def test_number_format(self):
        """Test number formatting logic"""
        # Integers
        self.assertEqual(BaseExtractor.format_number("100"), 100)
        self.assertEqual(BaseExtractor.format_number(100), 100)
        
        # Floats with dot decimal
        self.assertEqual(BaseExtractor.format_number("100.50"), 100.50)
        self.assertEqual(BaseExtractor.format_number(100.50), 100.50)
        
        # Vietnamese format: dot thousands, comma decimal
        # Ideally: 1.000,50 -> 1000.5
        # The current implementation replaces dot with empty, and comma with dot.
        # So 1.000,50 -> 1000,50 -> 1000.50
        self.assertEqual(BaseExtractor.format_number("1.000,50"), 1000.5)
        self.assertEqual(BaseExtractor.format_number("10.000,00"), 10000.0)
        
        # Simple integer with thousands separator
        self.assertEqual(BaseExtractor.format_number("10.000"), 10000)
        
        # Empty values
        self.assertEqual(BaseExtractor.format_number(""), "")
        self.assertEqual(BaseExtractor.format_number(None), "")

    @patch('extractor_core_v2.load_workbook')
    def test_export_sheet_recognition_xlsx(self, mock_load_workbook):
        """Test EXPORT sheet recognition with XLSX"""
        mock_wb = MagicMock()
        mock_load_workbook.return_value = mock_wb
        
        extractor = ExportExtractor("dummy.xlsx")
        
        # Case 1: Standard name 'TKX'
        mock_wb.sheetnames = ['Sheet1', 'TKX']
        mock_wb.__getitem__.return_value = MagicMock()
        self.assertTrue(extractor.load_workbook())
        self.assertEqual(extractor.found_sheet_name, 'TKX')
        
        # Case 2: Alias 'ToKhaiXuat02'
        mock_wb.sheetnames = ['Sheet1', 'ToKhaiXuat02']
        self.assertTrue(extractor.load_workbook())
        self.assertEqual(extractor.found_sheet_name, 'ToKhaiXuat02')
        
        # Case 3: Case insensitive
        mock_wb.sheetnames = ['Sheet1', 'tokhaixuat02']
        self.assertTrue(extractor.load_workbook())
        self.assertEqual(extractor.found_sheet_name, 'tokhaixuat02')
        
        # Case 4: No match
        mock_wb.sheetnames = ['Sheet1', 'Sheet2']
        self.assertFalse(extractor.load_workbook())
    
    @patch('extractor_core_v2.load_workbook')
    def test_import_sheet_recognition_xlsx(self, mock_load_workbook):
        """Test IMPORT sheet recognition with XLSX"""
        mock_wb = MagicMock()
        mock_load_workbook.return_value = mock_wb
        
        extractor = ImportExtractor("dummy.xlsx")
        
        # Case 1: Alias 'ToKhaiNhap2'
        mock_wb.sheetnames = ['TKN', 'ToKhaiNhap2']
        # It picks the first match in the alias list order? No, it loops sheet names.
        # Actually logic loops sheet names and checks if in aliases.
        # If 'TKN' is in sheetnames and aliases, it matches TKN.
        self.assertTrue(extractor.load_workbook())
        self.assertEqual(extractor.found_sheet_name, 'TKN')
        
        # Case 2: Alias 'Tờ khai nhập'
        mock_wb.sheetnames = ['Data', 'Tờ khai nhập']
        self.assertTrue(extractor.load_workbook())
        self.assertEqual(extractor.found_sheet_name, 'Tờ khai nhập')

    @patch('extractor_core_v2.load_workbook')
    def test_find_declaration_id(self, mock_load_workbook):
        """Test declaration ID detection"""
        # Mock sheet data
        mock_wb = MagicMock()
        mock_sheet = MagicMock()
        mock_load_workbook.return_value = mock_wb
        
        # Scenario 1: Import ID (10...)
        extractor = ImportExtractor("dummy.xlsx")
        extractor.is_xls = False
        extractor.sheet = mock_sheet
        extractor.sheet.max_row = 10
        
        # openpyxl returns rows as tuples of cells
        # Create a mock cell with value
        cell_val = MagicMock()
        cell_val.value = "Số tờ khai: 101234567890"
        
        # Mock getting row 1
        extractor.sheet.__getitem__.return_value = [cell_val]
        
        extracted_id = extractor.find_declaration_id()
        self.assertEqual(extracted_id, "101234567890")
        
        # Scenario 2: Export ID (30...)
        extractor_ex = ExportExtractor("dummy.xlsx")
        extractor_ex.is_xls = False
        extractor_ex.sheet = mock_sheet
        extractor_ex.sheet.max_row = 10
        
        cell_val2 = MagicMock()
        cell_val2.value = " tờ khai 309876543210 "
        extractor_ex.sheet.__getitem__.return_value = [cell_val2]
        
        extracted_id_ex = extractor_ex.find_declaration_id()
        self.assertEqual(extracted_id_ex, "309876543210")
        
        # Scenario 3: No ID
        cell_val3 = MagicMock()
        cell_val3.value = "Just some text"
        extractor.sheet.__getitem__.return_value = [cell_val3]
        
        self.assertEqual(extractor.find_declaration_id(), "")

if __name__ == '__main__':
    unittest.main()
