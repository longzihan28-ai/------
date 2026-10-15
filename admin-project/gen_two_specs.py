from docx import Document
from docx.shared import Pt, Cm
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

style = doc.styles['Normal']
style.font.name = '宋体'
style.font.size = Pt(11)


def add_use_case_table(doc, title_text, rows_data):
    """添加一个用例规格说明表格"""
    title = doc.add_heading(title_text, level=1)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    table = doc.add_table(rows=len(rows_data), cols=2)
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    for row in table.rows:
        row.cells[0].width = Cm(4)
        row.cells[1].width = Cm(12)

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


# ====== 表2: 申请退款用例文档 ======
refund_apply = [
    ("用例名称", "申请退款"),
    ("用例编号", "UC005"),
    ("参与者", "顾客"),
    ("用例描述", "该用例描述一个系统顾客对已购买的订单申请退款的行为"),
    ("触发器", "当顾客在订单列表中选择申请退款时，用例触发"),
    ("前置条件", "顾客已登录系统，且存在已完成的订单"),
    ("后置条件", "如果退款申请提交成功，则触发商家审核退款流程；否则提示错误信息"),
    ("基本事件流",
     "1. 顾客在订单列表中选择需要退款的订单\n"
     "2. 系统验证订单状态是否允许退款\n"
     "3. 顾客填写退款原因并提交退款申请\n"
     "4. 系统验证退款申请信息的合法性\n"
     "5. 系统保存退款申请记录，并将退款状态置为\"待审核\"\n"
     "6. 系统将退款申请通知发送至对应商家\n"
     "7. 系统生成退款申请提交确认页面并发送给顾客"),
    ("扩展事件流",
     "A-2 如果订单状态不允许退款（如订单未发货且未付款），系统提示无法退款并终止用例\n"
     "A-4 如果退款原因信息不完整或非法，系统提示顾客补充完整后重新提交"),
    ("结论", "当顾客收到退款申请提交确认页面或错误提示信息时，用例结束"),
    ("数据需求",
     "D-1 退款申请信息包括退款申请编号、订单号、顾客账号、退款原因、退款金额、申请时间"),
    ("业务规则",
     "B-1 只有订单状态为\"已付款\"或\"已发货\"时才允许申请退款\n"
     "B-2 退款金额不得超过订单实际支付金额"),
]
add_use_case_table(doc, "表2-1  申请退款用例文档", refund_apply)

doc.add_page_break()

# ====== 表3: 审核退款用例文档 ======
refund_review = [
    ("用例名称", "审核退款"),
    ("用例编号", "UC006"),
    ("参与者", "商家"),
    ("用例描述", "该用例描述一个系统商家对顾客提交的退款申请进行审核的行为"),
    ("触发器", "当商家在退款管理中选择待审核的退款申请时，用例触发"),
    ("前置条件", "商家已登录系统，且存在待审核的退款申请"),
    ("后置条件", "如果审核通过，则退款流程进入退款处理阶段；如果审核不通过，则通知顾客并终止退款"),
    ("基本事件流",
     "1. 商家在退款管理列表中选择一条待审核的退款申请\n"
     "2. 系统显示退款申请详情，商家查看退款原因\n"
     "3. 商家根据退款原因和订单信息做出审核决定\n"
     "4. 商家提交审核结果（通过或不通过）\n"
     "5. 系统保存审核结果，更新退款申请状态\n"
     "6. 系统将审核结果通知发送给顾客\n"
     "7. 如果审核通过，系统将退款流程转入退款处理阶段"),
    ("扩展事件流",
     "A-3 如果商家认为退款原因不充分，选择审核不通过，系统记录拒绝原因并通知顾客\n"
     "A-2 如果退款申请信息缺失或不完整，系统提示商家补充查看相关订单信息后再做决定"),
    ("结论", "当退款申请状态被更新为\"审核通过\"或\"审核不通过\"，且顾客收到通知时，用例结束"),
    ("数据需求",
     "D-1 审核信息包括退款申请编号、商家账号、审核结果、审核意见、审核时间"),
    ("业务规则",
     "B-1 商家必须先查看退款原因后才能提交审核结果\n"
     "B-2 审核结果只能为\"通过\"或\"不通过\"两种状态"),
]
add_use_case_table(doc, "表3-1  审核退款用例文档", refund_review)

output_path = r"c:\Users\Lenovo\Desktop\退款相关用例文档.docx"
doc.save(output_path)
print(f"已生成: {output_path}")
