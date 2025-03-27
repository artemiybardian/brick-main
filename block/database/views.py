from .models import *
import pprint

def get_path(req_obj):
    ans = [(req_obj.id, req_obj.item_name)]
    curr = ThemeObjLinks.objects.get(obj = req_obj.id).high
    while True:
        ans.append((curr.id, curr.collection_name))
        if curr.id == 1:
            break
        curr = ThemeLinks.objects.get(low = curr.id).high
        
    ans.reverse()
    return ans

def get_catalog_path(id):
    ans = []
    curr = Theme.objects.get(id = id)
    while True:
        ans.append((curr.id, curr.collection_name))
        if curr.id == 1:
            break
        curr = ThemeLinks.objects.get(low = curr.id).high
        
    ans.reverse()
    return ans

def consists_of(ident):
    return {"Sets": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 0))),
                "Parts": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 1))),
                "MF": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 2))),
                "Books": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 3))),
                "Gear": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 4))),
                "Catalogs": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 5))),
                "Instructions": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 6))),
                "Boxes": len(list(x.part_count for x in Links.objects.filter(set = ident, part_class = 7)))}

def appears_in(ident):
    return {"Sets": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 0))),
                "Parts": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 1))),
                "MF": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 2))),
                "Books": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 3))),
                "Gear": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 4))),
                "Catalogs": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 5))),
                "Instructions": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 6))),
                "Boxes": len(list(x.part_count for x in Links.objects.filter(part = ident, set_class = 7)))}

def rec_tree(id):
    tree = {}
    children = ThemeLinks.objects.filter(high = id)
    for i in children:
        t = rec_tree(i.low.id)
        if t:
            tree[(i.low.id, i.low.collection_name, i.low.size)] = t
        else:
            if "final" not in tree.keys():
                tree["final"] = [(i.low.id, i.low.collection_name, i.low.size)]
            else:
                tree["final"] += [(i.low.id, i.low.collection_name, i.low.size)]
    return tree

def elem(id):
    children = [x for x in ThemeLinks.objects.filter(high = id)]
    ans = [(x.obj.id, x.obj.item_name, get_path(x.obj))  for x in ThemeObjLinks.objects.filter(high = id)]
    stack = children
    while stack:
        a = stack.pop(0)
        ans += [(x.obj.id, x.obj.item_name, get_path(x.obj))  for x in ThemeObjLinks.objects.filter(high = a.low.id)]
        stack += [x for x in ThemeLinks.objects.filter(high = a.low.id)]
    return ans

def obj_exists(arg_id):
    return True if (len(Obj.objects.filter(id = arg_id))>0) else False

def theme_exists(arg_id):
    return True if (len(Theme.objects.filter(id = arg_id))>0) else False

def return_object(arg_id):
    req_obj = Obj.objects.get(id = arg_id)
    ans = {"item_name" : req_obj.item_name,
           "item_no" : req_obj.id,
           "year_first_release" : req_obj.year_first_release,
           "year_last_release" : req_obj.year_last_release,
           "weight" : req_obj.weight,
           "pack_dim" : req_obj.pack_dim,
           "stud_dim" : req_obj.stud_dim,
           "item_dim" : req_obj.item_dim,
           "flat_dim" : req_obj.flat_dim,
           "instructions" : req_obj.instructions,
           "images" : list(x.address for x in Images.objects.filter(item_id=req_obj.id)) if req_obj.id != 1 else [],
           "colors" : {i.color: i.address for i in Images.objects.filter(item_id=req_obj.id)} if req_obj.id ==1 else {},
           "item_consists_of" : consists_of(req_obj.id),
           "item_appears_in" : appears_in(req_obj.id),
           "path" : get_path(req_obj),
           "class" : req_obj.item_class
           }
    return ans

def return_subcatalogs(id):
    ans = {
        "path" : get_catalog_path(id),
        "tree" : rec_tree(id)
    }

    return ans

def return_elements(id):
    ans = {
        "path" : get_catalog_path(id),
        "elems" : elem(id)
    }

    return ans

def return_appears_in(type, id):
    return [{"item_name" : req_obj.set.item_name,
           "item_no" : req_obj.set.id,
           "year_first_release" : req_obj.set.year_first_release,
           "year_last_release" : req_obj.set.year_last_release,
           "weight" : req_obj.set.weight,
           "pack_dim" : req_obj.set.pack_dim,
           "stud_dim" : req_obj.set.stud_dim,
           "item_dim" : req_obj.set.item_dim,
           "flat_dim" : req_obj.set.flat_dim,
           "instructions" : req_obj.set.instructions,
           "images" : list(x.address for x in Images.objects.filter(item_id=req_obj.set.id)) if req_obj.set.id != 1 else [],
           "colors" : {i.color: i.address for i in Images.objects.filter(item_id=req_obj.set.id)} if req_obj.set.id ==1 else {},
           "item_consists_of" : consists_of(req_obj.set.id),
           "item_appears_in" : appears_in(req_obj.set.id),
           "path" : get_path(req_obj.set),
           "class" : req_obj.set.item_class,
           "part_count" : req_obj.part_count,
           } for req_obj in Links.objects.filter(part = id, set_class = type)]

def return_consists_of(type, id):
    return [{"item_name" : req_obj.part.item_name,
           "item_no" : req_obj.part.id,
           "year_first_release" : req_obj.part.year_first_release,
           "year_last_release" : req_obj.part.year_last_release,
           "weight" : req_obj.part.weight,
           "pack_dim" : req_obj.part.pack_dim,
           "stud_dim" : req_obj.part.stud_dim,
           "item_dim" : req_obj.part.item_dim,
           "flat_dim" : req_obj.part.flat_dim,
           "instructions" : req_obj.part.instructions,
           "images" : list(x.address for x in Images.objects.filter(item_id=req_obj.part.id)) if req_obj.part.id != 1 else [],
           "colors" : {i.color: i.address for i in Images.objects.filter(item_id=req_obj.part.id)} if req_obj.part.id ==1 else {},
           "item_consists_of" : consists_of(req_obj.part.id),
           "item_appears_in" : appears_in(req_obj.part.id),
           "path" : get_path(req_obj.part),
           "class" : req_obj.part.item_class,
           "part_count" : req_obj.part_count,
           } for req_obj in Links.objects.filter(set = id, part_class = type)]

def build_tree_recursive(id):
    children = ThemeLinks.objects.filter(high=id)
    num_childen_obj = ThemeObjLinks.objects.filter(high=id).count()
    r = sum(build_tree_recursive(x.low.id) for x in children) + num_childen_obj
    Theme.objects.filter(id=id).update(size=r)
    return r

