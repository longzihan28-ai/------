import win32com.client
import pythoncom
import os

pythoncom.CoInitialize()

word = win32com.client.Dispatch('Word.Application')
word.Visible = False
doc = word.Documents.Open(r'c:\Users\Lenovo\Desktop\面向对象系统分析与设计实验报告1.doc')

# Save as HTML to extract embedded images
html_path = r'c:\Users\Lenovo\Desktop\report_export'
doc.SaveAs(html_path, FileFormat=10)  # wdFormatHTML = 10

# Also count inline shapes (embedded images)
print(f'InlineShapes count: {doc.InlineShapes.Count}')
for i in range(1, doc.InlineShapes.Count + 1):
    shape = doc.InlineShapes(i)
    print(f'Shape {i}: Type={shape.Type}, Range text nearby: {shape.Range.Paragraphs(1).Range.Text[:50]}')

# Count tables
print(f'\nTables count: {doc.Tables.Count}')
for i in range(1, doc.Tables.Count + 1):
    table = doc.Tables(i)
    print(f'\nTable {i}: Rows={table.Rows.Count}, Cols={table.Columns.Count}')
    for ri in range(1, table.Rows.Count + 1):
        row_data = []
        for ci in range(1, table.Columns.Count + 1):
            try:
                cell = table.Cell(ri, ci)
                text = cell.Range.Text.strip().replace(chr(7), '').replace('\r', ' ')
                row_data.append(text)
            except:
                row_data.append('(merged)')
        print(f'  Row {ri}: {" | ".join(row_data)}')

doc.Close(False)
word.Quit()
pythoncom.CoUninitialize()

# List exported files
print('\n=== EXPORTED FILES ===')
for f in os.listdir(html_path if os.path.isdir(html_path) else os.path.dirname(html_path)):
    print(f)
