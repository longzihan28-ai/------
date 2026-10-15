import json

_id_n = [0]
def nid():
    _id_n[0] += 1
    return f"AAAA{_id_n[0]:08d}Fr"

project_id = nid()
model_id = nid()
diagram_id = nid()
subsystem_id = nid()  # 系统边界

# ====== ACTORS ======
actor_names = ["用户", "顾客", "商家", "系统管理员"]
actor_ids = {}
actor_view_ids = {}
for name in actor_names:
    actor_ids[name] = nid()
    actor_view_ids[name] = nid()

# ====== USE CASES ======
uc_names = [
    "登录系统", "修改个人信息",
    "浏览商品", "购买商品", "验证账户余额", "使用优惠券",
    "查看订单", "确认收货", "申请退款",
    "管理购物车", "添加商品", "删除商品", "修改数量",
    "管理商品", "上架商品", "修改商品", "下架商品",
    "处理发货", "审核退款", "查看退款原因",
    "查看销售统计",
    "管理用户", "冻结账号", "解冻账号",
    "管理商品分类", "查看系统日志"
]
uc_ids = {}
uc_view_ids = {}
for name in uc_names:
    uc_ids[name] = nid()
    uc_view_ids[name] = nid()

# ====== LAYOUT ======
# 左侧参与者
actor_layout = {
    "用户":         (30, 20, 60, 90),
    "顾客":         (30, 250, 60, 90),
}
# 右侧参与者
actor_layout_right = {
    "商家":         (820, 450, 60, 90),
    "系统管理员":   (820, 950, 60, 90),
}

# 系统边界: x=150~790, y=10~1250
# 用例在系统边界内
# 中间列(主用例): x=270
# 右列(子用例): x=540
uc_layout = {
    # 用户公共
    "登录系统":       (270, 40, 120, 40),
    "修改个人信息":   (270, 100, 130, 40),
    # 顾客
    "浏览商品":       (270, 170, 110, 40),
    "购买商品":       (270, 230, 110, 40),
    "查看订单":       (270, 310, 110, 40),
    "申请退款":       (270, 380, 110, 40),
    "管理购物车":     (270, 450, 120, 40),
    # 商家
    "管理商品":       (270, 580, 110, 40),
    "处理发货":       (270, 650, 110, 40),
    "审核退款":       (270, 720, 110, 40),
    "查看销售统计":   (270, 790, 130, 40),
    # 管理员
    "管理用户":       (270, 880, 110, 40),
    "管理商品分类":   (270, 950, 130, 40),
    "查看系统日志":   (270, 1020, 130, 40),
    # 子用例 - 右列
    "验证账户余额":   (540, 220, 130, 40),
    "使用优惠券":     (540, 270, 110, 40),
    "确认收货":       (540, 320, 110, 40),
    "添加商品":       (540, 440, 110, 40),
    "删除商品":       (540, 490, 110, 40),
    "修改数量":       (540, 540, 110, 40),
    "上架商品":       (540, 575, 110, 40),
    "修改商品":       (540, 625, 110, 40),
    "下架商品":       (540, 675, 110, 40),
    "查看退款原因":   (540, 710, 130, 40),
    "冻结账号":       (540, 870, 110, 40),
    "解冻账号":       (540, 920, 110, 40),
}

def right_of(name, layout):
    x, y, w, h = layout[name]
    return (x + w, y + h / 2)

def left_of(name, layout):
    x, y, w, h = layout[name]
    return (x, y + h / 2)

def center_top(name, layout):
    x, y, w, h = layout[name]
    return (x + w / 2, y)

def center_bottom(name, layout):
    x, y, w, h = layout[name]
    return (x + w / 2, y + h)

# ====== MODEL ELEMENTS ======
model_elements = []

# 系统边界 SubSystem
model_elements.append({
    "_type": "UMLSubSystem",
    "_id": subsystem_id,
    "_parent": {"$ref": model_id},
    "name": "在线购物系统"
})

# Actors (owned by model)
for name in actor_names:
    model_elements.append({
        "_type": "UMLActor",
        "_id": actor_ids[name],
        "_parent": {"$ref": model_id},
        "name": name
    })

# Use Cases (owned by subsystem = inside system boundary)
for name in uc_names:
    model_elements.append({
        "_type": "UMLUseCase",
        "_id": uc_ids[name],
        "_parent": {"$ref": subsystem_id},
        "name": name
    })

# ====== RELATIONSHIPS ======

# Associations (Actor -> UseCase)
associations = [
    ("用户", "登录系统"), ("用户", "修改个人信息"),
    ("顾客", "浏览商品"), ("顾客", "购买商品"),
    ("顾客", "查看订单"), ("顾客", "申请退款"),
    ("顾客", "管理购物车"),
    ("商家", "管理商品"), ("商家", "处理发货"),
    ("商家", "审核退款"), ("商家", "查看销售统计"),
    ("系统管理员", "管理用户"),
    ("系统管理员", "管理商品分类"),
    ("系统管理员", "查看系统日志"),
]

assoc_views = []
for actor_name, uc_name in associations:
    rel_id = nid()
    end1_id = nid()
    end2_id = nid()
    view_id = nid()

    # Determine if actor is on left or right
    if actor_name in actor_layout:
        tx, ty = right_of(actor_name, actor_layout)
    else:
        tx, ty = left_of(actor_name, actor_layout_right)
    hx, hy = left_of(uc_name, uc_layout) if actor_name in actor_layout else right_of(uc_name, uc_layout)
    pts = f"{int(tx)},{int(ty)} {int(hx)},{int(hy)}"

    model_elements.append({
        "_type": "UMLAssociation",
        "_id": rel_id,
        "_parent": {"$ref": model_id},
        "end1": {
            "_type": "UMLAssociationEnd",
            "_id": end1_id,
            "_parent": {"$ref": rel_id},
            "reference": {"$ref": actor_ids[actor_name]},
            "navigable": True,
            "aggregation": "none"
        },
        "end2": {
            "_type": "UMLAssociationEnd",
            "_id": end2_id,
            "_parent": {"$ref": rel_id},
            "reference": {"$ref": uc_ids[uc_name]},
            "navigable": True,
            "aggregation": "none"
        }
    })
    # tail=actor, head=usecase
    assoc_views.append((view_id, rel_id, actor_view_ids[actor_name], uc_view_ids[uc_name], pts))

# Generalizations (Actor -> Actor)
generalizations = [
    ("顾客", "用户"),
    ("商家", "用户"),
    ("系统管理员", "用户"),
]

gen_views = []
for child, parent in generalizations:
    rel_id = nid()
    view_id = nid()
    # child could be left or right, parent is left
    if child in actor_layout:
        cx, cy, cw, ch = actor_layout[child]
    else:
        cx, cy, cw, ch = actor_layout_right[child]
    px, py, pw, ph = actor_layout["用户"]
    tx = cx + cw / 2
    ty = cy
    hx = px + pw / 2
    hy = py + ph
    pts = f"{int(tx)},{int(ty)} {int(hx)},{int(hy)}"

    model_elements.append({
        "_type": "UMLGeneralization",
        "_id": rel_id,
        "_parent": {"$ref": model_id},
        "source": {"$ref": actor_ids[child]},
        "target": {"$ref": actor_ids[parent]}
    })
    gen_views.append((view_id, rel_id, actor_view_ids[child], actor_view_ids["用户"], pts))

# Include relationships (必须)
includes = [
    ("购买商品", "验证账户余额"),
    ("审核退款", "查看退款原因"),
]

inc_views = []
for base, inclusion in includes:
    rel_id = nid()
    view_id = nid()
    bx, by, bw, bh = uc_layout[base]
    ix, iy, iw, ih = uc_layout[inclusion]
    tx = bx + bw
    ty = by + bh / 2
    hx = ix
    hy = iy + ih / 2
    pts = f"{int(tx)},{int(ty)} {int(hx)},{int(hy)}"

    model_elements.append({
        "_type": "UMLInclude",
        "_id": rel_id,
        "_parent": {"$ref": model_id},
        "source": {"$ref": uc_ids[base]},
        "target": {"$ref": uc_ids[inclusion]}
    })
    inc_views.append((view_id, rel_id, uc_view_ids[base], uc_view_ids[inclusion], pts))

# Generalization for management sub-functions
uc_generalizations = [
    ("添加商品", "管理购物车"),
    ("删除商品", "管理购物车"),
    ("修改数量", "管理购物车"),
    ("上架商品", "管理商品"),
    ("修改商品", "管理商品"),
    ("下架商品", "管理商品"),
    ("冻结账号", "管理用户"),
    ("解冻账号", "管理用户"),
]

uc_gen_views = []
for child, parent in uc_generalizations:
    rel_id = nid()
    view_id = nid()
    cx, cy, cw, ch = uc_layout[child]
    px, py, pw, ph = uc_layout[parent]
    tx = cx
    ty = cy + ch / 2
    hx = px + pw
    hy = py + ph / 2
    pts = f"{int(tx)},{int(ty)} {int(hx)},{int(hy)}"

    model_elements.append({
        "_type": "UMLGeneralization",
        "_id": rel_id,
        "_parent": {"$ref": model_id},
        "source": {"$ref": uc_ids[child]},
        "target": {"$ref": uc_ids[parent]}
    })
    uc_gen_views.append((view_id, rel_id, uc_view_ids[child], uc_view_ids[parent], pts))

# Extend relationships
extends = [
    ("使用优惠券", "购买商品"),
    ("确认收货", "查看订单"),
]

ext_views = []
for extending, base in extends:
    rel_id = nid()
    view_id = nid()
    ex, ey, ew, eh = uc_layout[extending]
    bx, by, bw, bh = uc_layout[base]
    tx = ex
    ty = ey + eh / 2
    hx = bx + bw
    hy = by + bh / 2
    pts = f"{int(tx)},{int(ty)} {int(hx)},{int(hy)}"

    model_elements.append({
        "_type": "UMLExtend",
        "_id": rel_id,
        "_parent": {"$ref": model_id},
        "source": {"$ref": uc_ids[extending]},
        "target": {"$ref": uc_ids[base]}
    })
    ext_views.append((view_id, rel_id, uc_view_ids[extending], uc_view_ids[base], pts))

# ====== VIEWS ======
views = []

# System boundary (SubSystemView) - 必须在最前面(最底层)
subsys_view_id = nid()
views.append({
    "_type": "UMLSubSystemView",
    "_id": subsys_view_id,
    "_parent": {"$ref": diagram_id},
    "model": {"$ref": subsystem_id},
    "left": 150, "top": 10, "width": 640, "height": 1070,
    "collapsed": False,
    "stereotypeDisplay": "none"
})

# Actor views (left)
for name in ["用户", "顾客"]:
    x, y, w, h = actor_layout[name]
    views.append({
        "_type": "UMLActorView",
        "_id": actor_view_ids[name],
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": actor_ids[name]},
        "left": x, "top": y, "width": w, "height": h
    })

# Actor views (right)
for name in ["商家", "系统管理员"]:
    x, y, w, h = actor_layout_right[name]
    views.append({
        "_type": "UMLActorView",
        "_id": actor_view_ids[name],
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": actor_ids[name]},
        "left": x, "top": y, "width": w, "height": h
    })

# Use case views
for name in uc_names:
    x, y, w, h = uc_layout[name]
    views.append({
        "_type": "UMLUseCaseView",
        "_id": uc_view_ids[name],
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": uc_ids[name]},
        "left": x, "top": y, "width": w, "height": h
    })

# Association views
for view_id, rel_id, tail_v, head_v, pts in assoc_views:
    views.append({
        "_type": "UMLAssociationView",
        "_id": view_id,
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": rel_id},
        "head": {"$ref": head_v},
        "tail": {"$ref": tail_v},
        "points": pts,
        "showLabel": False
    })

# Generalization views (actors)
for view_id, rel_id, tail_v, head_v, pts in gen_views:
    views.append({
        "_type": "UMLGeneralizationView",
        "_id": view_id,
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": rel_id},
        "head": {"$ref": head_v},
        "tail": {"$ref": tail_v},
        "points": pts,
        "showLabel": False
    })

# Generalization views (use cases)
for view_id, rel_id, tail_v, head_v, pts in uc_gen_views:
    views.append({
        "_type": "UMLGeneralizationView",
        "_id": view_id,
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": rel_id},
        "head": {"$ref": head_v},
        "tail": {"$ref": tail_v},
        "points": pts,
        "showLabel": False
    })

# Include views
for view_id, rel_id, tail_v, head_v, pts in inc_views:
    views.append({
        "_type": "UMLIncludeView",
        "_id": view_id,
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": rel_id},
        "head": {"$ref": head_v},
        "tail": {"$ref": tail_v},
        "points": pts,
        "showLabel": True
    })

# Extend views
for view_id, rel_id, tail_v, head_v, pts in ext_views:
    views.append({
        "_type": "UMLExtendView",
        "_id": view_id,
        "_parent": {"$ref": diagram_id},
        "model": {"$ref": rel_id},
        "head": {"$ref": head_v},
        "tail": {"$ref": tail_v},
        "points": pts,
        "showLabel": True
    })

# ====== DIAGRAM ======
diagram = {
    "_type": "UMLUseCaseDiagram",
    "_id": diagram_id,
    "_parent": {"$ref": model_id},
    "name": "在线购物系统用例图",
    "defaultDiagram": True,
    "ownedViews": views
}
model_elements.append(diagram)

# ====== MODEL ======
model = {
    "_type": "UMLModel",
    "_id": model_id,
    "_parent": {"$ref": project_id},
    "name": "Model",
    "ownedElements": model_elements
}

# ====== PROJECT ======
project = {
    "_type": "Project",
    "_id": project_id,
    "name": "在线购物系统",
    "ownedElements": [model]
}

# ====== OUTPUT ======
output_path = r"c:\Users\Lenovo\Desktop\在线购物系统用例图.mdj"
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(project, f, ensure_ascii=False, indent=2)

print(f"已生成: {output_path}")
print(f"参与者: {len(actor_names)}, 用例: {len(uc_names)}")
print(f"关联: {len(associations)}, 泛化(参与者): {len(generalizations)}, 泛化(用例): {len(uc_generalizations)}")
print(f"包含: {len(includes)}, 扩展: {len(extends)}")
print(f"视图元素: {len(views)} (含 {len(assoc_views)+len(gen_views)+len(uc_gen_views)+len(inc_views)+len(ext_views)} 条关系线)")
print("新增: 系统边界(SubSystem), 参与者左右分布")
