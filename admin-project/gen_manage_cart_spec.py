from docx import Document
from docx.shared import Pt, Cm
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()
style = doc.styles['Normal']
style.font.name = '宋体'
style.font.size = Pt(11)

title = doc.add_heading('表4-1  管理购物车用例文档', level=1)
title.alignment = WD_ALIGN_PARAGRAPH.CENTER

table = doc.add_table(rows=12, cols=2)
table.style = 'Table Grid'
table.alignment = WD_TABLE_ALIGNMENT.CENTER

for row in table.rows:
    row.cells[0].width = Cm(4)
    row.cells[1].width = Cm(12)

rows_data = [
    ("用例名称", "管理购物车"),
    ("用例编号", "UC004"),
    ("参与者", "顾客"),
    ("用例描述", "该用例描述一个系统顾客对购物车中的商品进行添加、删除和修改数量的行为"),
    ("触发器", "当顾客进入购物车页面时，用例触发"),
    ("前置条件", "顾客需要完成登录操作"),
    ("后置条件", "购物车中的商品信息被更新并保存，顾客可继续浏览或进入结算"),
    ("基本事件流",
     "1. 顾客进入购物车页面，系统显示当前购物车中的商品列表\n"
     "2. 顾客选择要执行的操作（添加商品、删除商品或修改数量）\n"
     "3. 系统验证操作请求的合法性\n"
     "4. 系统根据顾客的操作更新购物车中的商品信息\n"
     "5. 系统重新计算购物车中商品的总数量和总价格\n"
     "6. 系统保存更新后的购物车信息\n"
     "7. 系统刷新购物车页面并显示最新信息给顾客"),
    ("扩展事件流",
     "A-2 如果顾客选择添加商品，系统将新商品加入购物车，若商品已存在则累加数量\n"
     "A-4 如果顾客选择删除商品，系统将指定商品从购物车中移除\n"
     "A-4b 如果顾客选择修改数量，系统验证数量为正整数后更新；若数量为零则提示是否删除该商品"),
    ("结论", "当购物车页面刷新完成，顾客看到最新商品列表和价格信息时，用例结束"),
    ("数据需求",
     "D-1 购物车信息包括购物车编号、顾客账号、商品编号、商品名称、商品单价、商品数量、小计金额、总金额"),
    ("业务规则",
     "B-1 购物车中同一商品只能存在一条记录，重复添加时累加数量\n"
     "B-2 商品数量必须为大于等于0的整数，数量为0时自动移除该商品\n"
     "B-3 购物车商品总数量和总价格由系统自动计算，顾客不可手动修改"),
]

for i, (label, content) in enumerate(rows_data):
    cell_label = table.cell(i, 0)
    cell_content = table.cell(i, 1)

    cell_label.text = label
    for p in cell_label.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.size = Pt(11)
            run.font.name = '宋体'

    cell_content.text = content
    for p in cell_content.paragraphs:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.size = Pt(11)
            run.font.name = '宋体'

output_path = r"c:\Users\Lenovo\Desktop\管理购物车用例文档.docx"
doc.save(output_path)
print(f"已生成: {output_path}")
