"""
Customs Data Extractor V2 - Core Module
Supports both Export (TKX) and Import (TKN) declarations
"""

import xlrd
from openpyxl import load_workbook, Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import os
import re
from enum import Enum
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Callable
from pathlib import Path


class DeclarationType(Enum):
    """Type of customs declaration"""
    EXPORT = "export"
    IMPORT = "import"


class ExtractionProgress:
    """Progress tracking for extraction process"""
    
    def __init__(self):
        self.total_steps = 0
        self.current_step = 0
        self.status_message = ""
        self.is_complete = False
        self.has_error = False
        self.error_message = ""
    
    @property
    def progress_percent(self) -> int:
        """Get progress as percentage (0-100)"""
        if self.total_steps == 0:
            return 0
        return int((self.current_step / self.total_steps) * 100)


class BaseExtractor(ABC):
    """Base class for customs declaration extractors"""
    
    @abstractmethod
    def get_sheet_name(self) -> str:
        """Get the sheet name to process"""
        pass
    
    @abstractmethod
    def extract_block_data(self, start_row: int) -> Optional[Dict[str, any]]:
        """Extract data from a single block"""
        pass
    
    def __init__(self, input_file: str, progress_callback: Optional[Callable] = None):
        """Initialize extractor"""
        self.input_file = input_file
        self.progress_callback = progress_callback
        self.progress = ExtractionProgress()
        self.workbook = None
        self.sheet = None
        self.data_blocks = []
        
        # Detect file format
        self.file_ext = Path(input_file).suffix.lower()
        self.is_xls = (self.file_ext == '.xls')
    
    def _update_progress(self, step: int, message: str):
        """Update progress and call callback"""
        self.progress.current_step = step
        self.progress.status_message = message
        
        if self.progress_callback:
            self.progress_callback(self.progress)
    
    def get_cell_value(self, row: int, col: int):
        """Get cell value - works for both xlrd and openpyxl"""
        if self.is_xls:
            return self.sheet.cell_value(row, col)
        else:
            return self.sheet.cell(row, col).value
    
    @staticmethod
    def format_number(value) -> str:
        """Format number from Vietnamese format to Excel format"""
        if value is None or value == "":
            return ""
        
        value_str = str(value).strip()
        if not value_str:
            return ""
        
        # Bỏ dấu chấm (thousands separator)
        value_str = value_str.replace('.', '')
        # Đổi dấu phẩy thành dấu chấm (decimal separator)
        value_str = value_str.replace(',', '.')
        
        return value_str
    
    def load_workbook(self) -> bool:
        """Load Excel workbook"""
        try:
            self._update_progress(0, f"Đang mở file: {Path(self.input_file).name}")
            
            if self.is_xls:
                self.workbook = xlrd.open_workbook(self.input_file)
                self.sheet = self.workbook.sheet_by_name(self.get_sheet_name())
                nrows = self.sheet.nrows
                ncols = self.sheet.ncols
            else:
                self.workbook = load_workbook(self.input_file, data_only=True)
                self.sheet = self.workbook[self.get_sheet_name()]
                nrows = self.sheet.max_row
                ncols = self.sheet.max_column
            
            self._update_progress(1, f"✓ Đã load sheet {self.get_sheet_name()} ({nrows} hàng, {ncols} cột)")
            return True
        except Exception as e:
            self.progress.has_error = True
            self.progress.error_message = f"Lỗi khi mở file: {str(e)}"
            if self.progress_callback:
                self.progress_callback(self.progress)
            return False
    
    def get_preview_data(self) -> List[Dict[str, str]]:
        """Get preview of data blocks for display"""
        preview = []
        for idx, block_start in enumerate(self.data_blocks[:20], 1):
            data = self.extract_block_data(block_start)
            if data:
                desc = data.get('description', '')
                origin = data.get('origin', '')
                if origin:
                    desc_display = f"{desc} ({origin})"
                else:
                    desc_display = desc
                
                preview.append({
                    'index': idx,
                    'hs_code': data.get('hs_code', ''),
                    'description': desc_display[:100] + '...' if len(desc_display) > 100 else desc_display,
                    'qty1': str(data.get('qty1', '')),
                    'unit1': data.get('unit1', '')
                })
        return preview
    
    def create_output_file(self, output_file: str) -> bool:
        """Create Excel output file with extracted data"""
        try:
            self._update_progress(4, f"Đang tạo file output...")
            
            wb = Workbook()
            ws = wb.active
            ws.title = "data"
            
            # Header
            headers = [
                "Mô tả hàng hóa", 
                "Xuất xứ",
                "Mã số hàng hóa", 
                "Số lượng (1)", 
                "Đơn vị 1", 
                "Số lượng (2)", 
                "Đơn vị 2",
                "Đơn giá hóa đơn",
                "Trị giá hóa đơn"
            ]
            ws.append(headers)
            
            # Format header
            header_font = Font(bold=True, size=11, color="FFFFFF")
            header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
            header_alignment = Alignment(horizontal="center", vertical="center")
            
            for cell in ws[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            
            # Write data
            total_blocks = len(self.data_blocks)
            for idx, block_start in enumerate(self.data_blocks, 1):
                self._update_progress(4 + idx, f"Đang ghi dữ liệu khối {idx}/{total_blocks}...")
                
                data = self.extract_block_data(block_start)
                if data:
                    row = [
                        data.get('description', ''),
                        data.get('origin', ''),
                        data.get('hs_code', ''),
                        data.get('qty1', ''),
                        data.get('unit1', ''),
                        data.get('qty2', ''),
                        data.get('unit2', ''),
                        data.get('unit_price', ''),
                        data.get('invoice_value', '')
                    ]
                    ws.append(row)
            
            # Format columns
            ws.column_dimensions['A'].width = 70
            ws.column_dimensions['B'].width = 10
            ws.column_dimensions['C'].width = 15
            ws.column_dimensions['D'].width = 15
            ws.column_dimensions['E'].width = 12
            ws.column_dimensions['F'].width = 15
            ws.column_dimensions['G'].width = 12
            ws.column_dimensions['H'].width = 18
            ws.column_dimensions['I'].width = 18
            
            # Borders
            thin_border = Border(
                left=Side(style='thin'),
                right=Side(style='thin'),
                top=Side(style='thin'),
                bottom=Side(style='thin')
            )
            
            for row in ws.iter_rows(min_row=1, max_row=len(self.data_blocks) + 1, 
                                   min_col=1, max_col=9):
                for cell in row:
                    cell.border = thin_border
                    cell.alignment = Alignment(vertical="top", wrap_text=True)
            
            # Save
            wb.save(output_file)
            self._update_progress(4 + total_blocks + 1, f"✓ Đã lưu file: {Path(output_file).name}")
            return True
            
        except Exception as e:
            self.progress.has_error = True
            self.progress.error_message = f"Lỗi khi tạo file: {str(e)}"
            if self.progress_callback:
                self.progress_callback(self.progress)
            return False
    
    def run(self, output_file: str) -> bool:
        """Run complete extraction process"""
        self.progress.total_steps = 5 + len(self.data_blocks) if hasattr(self, 'data_blocks') else 10
        
        if not self.load_workbook():
            return False
        
        num_blocks = self.find_data_blocks()
        if num_blocks == 0:
            self.progress.has_error = True
            self.progress.error_message = "Không tìm thấy dữ liệu nào!"
            if self.progress_callback:
                self.progress_callback(self.progress)
            return False
        
        self.progress.total_steps = 5 + num_blocks
        
        if not self.create_output_file(output_file):
            return False
        
        self.progress.is_complete = True
        self.progress.current_step = self.progress.total_steps
        self.progress.status_message = f"✓ Hoàn thành! Đã trích xuất {num_blocks} khối dữ liệu"
        if self.progress_callback:
            self.progress_callback(self.progress)
        
        return True


class ExportExtractor(BaseExtractor):
    """Extractor for Export declarations (TKX)"""
    
    # Column definitions (0-based)
    COL_LABEL = 2
    COL_VALUE = 5       # Column F
    COL_QTY_VALUE = 16  # Column Q
    COL_UNIT = 24       # Column Y
    COL_INVOICE_PRICE = 17  # Column R
    
    # Offsets
    OFFSET_DESCRIPTION = 1
    OFFSET_QTY1 = 4
    OFFSET_QTY2 = 5
    OFFSET_INVOICE = 6
    
    def get_sheet_name(self) -> str:
        return 'TKX'
    
    @staticmethod
    def extract_origin(description: str) -> tuple:
        """Extract country of origin from description pattern #&XX"""
        if not description:
            return "", ""
        
        pattern = r'#&([A-Z]{2,})\s*$'
        match = re.search(pattern, description)
        
        if match:
            origin = match.group(1)
            return description, origin
        
        return description, ""
    
    def find_data_blocks(self) -> int:
        """Find all data blocks in export sheet"""
        try:
            self._update_progress(2, "Đang tìm kiếm các khối dữ liệu...")
            self.data_blocks = []
            
            if self.is_xls:
                max_rows = self.sheet.nrows
            else:
                max_rows = self.sheet.max_row
            
            for row_idx in range(max_rows):
                try:
                    if self.is_xls:
                        cell_value = self.get_cell_value(row_idx, self.COL_LABEL)
                    else:
                        cell_value = self.get_cell_value(row_idx + 1, self.COL_LABEL + 1)
                    
                    if cell_value and "Mã số hàng hóa" in str(cell_value):
                        if self.is_xls:
                            hs_code = self.get_cell_value(row_idx, self.COL_VALUE)
                        else:
                            hs_code = self.get_cell_value(row_idx + 1, self.COL_VALUE + 1)
                        
                        hs_code_str = str(hs_code).strip() if hs_code else ""
                        
                        if isinstance(hs_code, (int, float)):
                            hs_code_str = str(int(hs_code))
                        
                        if hs_code_str.isdigit() and len(hs_code_str) == 8:
                            if self.is_xls:
                                self.data_blocks.append(row_idx)
                            else:
                                self.data_blocks.append(row_idx + 1)
                except:
                    continue
            
            self._update_progress(3, f"✓ Tìm thấy {len(self.data_blocks)} khối dữ liệu")
            return len(self.data_blocks)
            
        except Exception as e:
            self.progress.has_error = True
            self.progress.error_message = f"Lỗi khi tìm dữ liệu: {str(e)}"
            if self.progress_callback:
                self.progress_callback(self.progress)
            return 0
    
    def extract_block_data(self, start_row: int) -> Optional[Dict[str, any]]:
        """Extract data from export declaration block"""
        data = {}
        
        try:
            if self.is_xls:
                hs_code = self.get_cell_value(start_row, self.COL_VALUE)
                description_raw = self.get_cell_value(start_row + self.OFFSET_DESCRIPTION, self.COL_VALUE)
                qty1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_QTY_VALUE)
                unit1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_UNIT)
                qty2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_QTY_VALUE)
                unit2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_UNIT)
                invoice_value = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_VALUE)
                unit_price = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_INVOICE_PRICE)
            else:
                hs_code = self.get_cell_value(start_row, self.COL_VALUE + 1)
                description_raw = self.get_cell_value(start_row + self.OFFSET_DESCRIPTION, self.COL_VALUE + 1)
                qty1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_QTY_VALUE + 1)
                unit1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_UNIT + 1)
                qty2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_QTY_VALUE + 1)
                unit2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_UNIT + 1)
                invoice_value = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_VALUE + 1)
                unit_price = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_INVOICE_PRICE + 1)
            
            # HS code
            if isinstance(hs_code, (int, float)):
                data['hs_code'] = str(int(hs_code))
            else:
                data['hs_code'] = str(hs_code).strip() if hs_code else ""
            
            # Description + origin
            description_str = str(description_raw).strip() if description_raw else ""
            original_desc, origin = self.extract_origin(description_str)
            data['description'] = original_desc
            data['origin'] = origin
            
            # Format numbers
            data['qty1'] = self.format_number(qty1)
            data['unit1'] = str(unit1).strip() if unit1 else ""
            data['qty2'] = self.format_number(qty2)
            data['unit2'] = str(unit2).strip() if unit2 else ""
            data['invoice_value'] = self.format_number(invoice_value)
            data['unit_price'] = self.format_number(unit_price)
            
            return data
            
        except Exception as e:
            return None


class ImportExtractor(BaseExtractor):
    """Extractor for Import declarations (TKN)"""
    
    # Column definitions (0-based)
    COL_LABEL = 2       # Column C
    COL_VALUE = 6       # Column G
    COL_QTY_VALUE = 21  # Column V
    COL_UNIT = 30       # Column AF (31 in 1-based = PCE)
    COL_INVOICE_VALUE = 8   # Column I
    COL_ORIGIN = 23     # Column X
    
    # Offsets
    OFFSET_DESCRIPTION = 1
    OFFSET_QTY1 = 4
    OFFSET_QTY2 = 5
    OFFSET_INVOICE = 6
    OFFSET_ORIGIN = 11  # Row N+11 for origin
    
    def get_sheet_name(self) -> str:
        return 'TKN'
    
    def find_data_blocks(self) -> int:
        """Find all data blocks in import sheet"""
        try:
            self._update_progress(2, "Đang tìm kiếm các khối dữ liệu...")
            self.data_blocks = []
            
            if self.is_xls:
                max_rows = self.sheet.nrows
            else:
                max_rows = self.sheet.max_row
            
            for row_idx in range(max_rows):
                try:
                    if self.is_xls:
                        cell_value = self.get_cell_value(row_idx, self.COL_LABEL)
                    else:
                        cell_value = self.get_cell_value(row_idx + 1, self.COL_LABEL + 1)
                    
                    if cell_value and "Mã số hàng hóa" in str(cell_value):
                        if self.is_xls:
                            hs_code = self.get_cell_value(row_idx, self.COL_VALUE)
                        else:
                            hs_code = self.get_cell_value(row_idx + 1, self.COL_VALUE + 1)
                        
                        hs_code_str = str(hs_code).strip() if hs_code else ""
                        
                        if isinstance(hs_code, (int, float)):
                            hs_code_str = str(int(hs_code))
                        
                        if hs_code_str.isdigit() and len(hs_code_str) == 8:
                            if self.is_xls:
                                self.data_blocks.append(row_idx)
                            else:
                                self.data_blocks.append(row_idx + 1)
                except:
                    continue
            
            self._update_progress(3, f"✓ Tìm thấy {len(self.data_blocks)} khối dữ liệu")
            return len(self.data_blocks)
            
        except Exception as e:
            self.progress.has_error = True
            self.progress.error_message = f"Lỗi khi tìm dữ liệu: {str(e)}"
            if self.progress_callback:
                self.progress_callback(self.progress)
            return 0
    
    def extract_block_data(self, start_row: int) -> Optional[Dict[str, any]]:
        """Extract data from import declaration block"""
        data = {}
        
        try:
            if self.is_xls:
                hs_code = self.get_cell_value(start_row, self.COL_VALUE)
                description_raw = self.get_cell_value(start_row + self.OFFSET_DESCRIPTION, self.COL_VALUE)
                qty1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_QTY_VALUE)
                unit1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_UNIT)
                qty2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_QTY_VALUE)
                unit2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_UNIT)
                invoice_value = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_INVOICE_VALUE)
                unit_price = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_QTY_VALUE)
                origin = self.get_cell_value(start_row + self.OFFSET_ORIGIN, self.COL_ORIGIN)
            else:
                hs_code = self.get_cell_value(start_row, self.COL_VALUE + 1)
                description_raw = self.get_cell_value(start_row + self.OFFSET_DESCRIPTION, self.COL_VALUE + 1)
                qty1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_QTY_VALUE + 1)
                unit1 = self.get_cell_value(start_row + self.OFFSET_QTY1, self.COL_UNIT + 1)
                qty2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_QTY_VALUE + 1)
                unit2 = self.get_cell_value(start_row + self.OFFSET_QTY2, self.COL_UNIT + 1)
                invoice_value = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_INVOICE_VALUE + 1)
                unit_price = self.get_cell_value(start_row + self.OFFSET_INVOICE, self.COL_QTY_VALUE + 1)
                origin = self.get_cell_value(start_row + self.OFFSET_ORIGIN, self.COL_ORIGIN + 1)
            
            # HS code
            if isinstance(hs_code, (int, float)):
                data['hs_code'] = str(int(hs_code))
            else:
                data['hs_code'] = str(hs_code).strip() if hs_code else ""
            
            # Description (no origin extraction from text)
            data['description'] = str(description_raw).strip() if description_raw else ""
            
            # Origin from dedicated row/cell
            data['origin'] = str(origin).strip() if origin else ""
            
            # Format numbers
            data['qty1'] = self.format_number(qty1)
            data['unit1'] = str(unit1).strip() if unit1 else ""
            data['qty2'] = self.format_number(qty2)
            data['unit2'] = str(unit2).strip() if unit2 else ""
            data['invoice_value'] = self.format_number(invoice_value)
            data['unit_price'] = self.format_number(unit_price)
            
            return data
            
        except Exception as e:
            return None
