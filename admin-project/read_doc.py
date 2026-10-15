import win32com.client
import pythoncom
pythoncom.CoInitialize()

word = win32com.client.Dispatch('Word.Application')
word.Visible = False
doc = word.Documents.Open(r'c:\Users\Lenovo\Desktop\面向对象系统分析与设计实验报告1.doc')

print('=== PARAGRAPHS ===')
for i, p in enumerate(doc.Paragraphs):
    text = p.Range.Text.strip()
    if text:
        print(f'{i}: {text}')

print('\n=== TABLES ===')
for ti, table in enumerate(doc.Tables):
    print(f'--- Table {ti} ---')
    for ri, row in enumerate(table.Rows):
        cells = []
        for ci, cell in enumerate(row.Cells):
            cells.append(cell.Range.Text.strip().replace(chr(7), ''))
        print(f'Row {ri}: {" | ".join(cells)}')

doc.Close(False)
word.Quit()
pythoncom.CoUninitialize()
