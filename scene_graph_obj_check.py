import json


with open('val_balanced_questions.json', 'r') as f:
    qs = json.load(f)
# with open('val_balanced_questions.json', 'r') as f:
    # qs.update(json.load(f))

with open('val_sceneGraphs.json', 'r') as f:
    sgs = json.load(f)
# with open('val_sceneGraphs.json', 'r') as f:
    # sgs.update(json.load(f))

with open('query_dict.json', 'r') as f:
    query_dict = json.load(f)

with open('lower_word_dict.json', 'r') as f:
    lower_word_dict = json.load(f)

upper_words = ['appliance', 'person', 'food', 'people', 'animal', 'animals', 'device', 'fruit', 'tree', 'trees',
               'cooking utensil', 'cooking utensils', 'vehicle', 'vehicles', 'vegetable', 'vegetables', 'container',
               'containers', 'baked good', 'toy', 'building', 'buildings', 'clothing', 'drink', 'drinks', 'weapon',
               'aircraft', 'sauce', 'dessert', 'desserts', 'furniture', 'bird', 'sign', 'bag', 'bottle', 'bottles',
               'meat', 'meats', 'utensil', 'utensils', ]


def find_select_from_scene_graph(image_id, argument):
    objects = []
    target = sgs[image_id]['objects']
    for obj_id, item in target.items():
        if argument['obj'] not in lower_word_dict.keys():
            if item['name'] == argument['obj']:
                item['id'] = obj_id
                objects.append(item)
        elif item['name'] == 'this' or item['name'] in lower_word_dict[argument['obj']]:
            item['id'] = obj_id
            objects.append(item)
    return objects


def find_filter_from_scene_graph(attribute, objs):
    filtered_objs = list()
    for obj in objs:
        if attribute in obj['attributes']:
            filtered_objs.append(obj)
        elif attribute.startswith('not('):
            if attribute[4:-1] not in obj['attributes']:
                filtered_objs.append(obj)
    return filtered_objs


def find_relate_from_scene_graph(image_id, relation, objs):
    related_objs = list()
    targets = sgs[image_id]['objects']
    if relation['relate'][1] == 'o':
        for obj in objs:
            for rel in obj['relations']:
                if rel['name'] == relation['relate'][0]:
                    if relation['obj'] not in lower_word_dict.keys():
                        if targets[rel['object']]['name'] == relation['obj']:
                            new_obj = targets[rel['object']]
                            new_obj['id'] = rel['object']
                            related_objs.append(new_obj)
                    elif relation['obj'] == '_' or relation['obj'] == 'this'\
                            or targets[rel['object']]['name'] in lower_word_dict[relation['obj']]:
                        new_obj = targets[rel['object']]
                        new_obj['id'] = rel['object']
                        related_objs.append(new_obj)
    else:
        for obj in objs:
            for idx, target in targets.items():
                for rel in target['relations']:
                    if rel['name'] == relation['relate'][0] and rel['object'] == obj['id']:
                        if relation['obj'] not in lower_word_dict.keys():
                            if target['name'] == relation['obj']:
                                new_obj = target
                                new_obj['id'] = idx
                                related_objs.append(new_obj)
                        elif relation['obj'] == '_' or relation['obj'] == 'this'\
                                or target['name'] in lower_word_dict[relation['obj']]:
                            new_obj = target
                            new_obj['id'] = idx
                            related_objs.append(new_obj)
    return related_objs


def process_query(qid, semantic, objs):
    argument = semantic['argument']
    query_options = list()
    if argument == 'name':
        for obj in objs:
            if obj['name'] not in query_options:
                query_options.append(obj['name'])
    else:
        for obj in objs:
            for attribute in query_dict[argument]:
                if attribute in obj['attributes'] and attribute not in query_options:
                    query_options.append(attribute)
    for item in query_options[:]:
        if item != qs[qid]['answer']:
            if item in upper_words and item in qs[qid]['question']:
                query_options.remove(item)
            elif item + 's' in upper_words and item + 's' in qs[qid]['question']:
                query_options.remove(item)
            elif item[:-1] in upper_words and item[:-1] in qs[qid]['question']:
                query_options.remove(item)
            elif (item == 'person' or item == 'people') and\
                    ('person' in qs[qid]['question'] or 'people' in qs[qid]['question']):
                query_options.remove(item)
    return query_options


def process_verify(image_id, semantic, objs):
    argument = semantic['argument']
    if 'rel' in semantic['operation']:
        argument = argument.split('(')[0][:-1]
        relation = argument.split(',')
        targets = sgs[image_id]['objects']
        if relation[2] == 'o':
            for obj in objs:
                for rel in obj['relations']:
                    if rel['name'] == relation[1] and targets[rel['object']]['name'] == relation[0]:
                        return ["yes"]
            return ["no"]
        else:
            for obj in objs:
                for idx, target in targets.items():
                    if target['name'] == relation[0]:
                        for rel in target['relations']:
                            if rel['name'] == relation[1] and rel['object'] == obj['id']:
                                return ["yes"]
            return ["no"]
    elif 'exist' in semantic['operation']:
        if objs:
                return ["yes"]
        return ["no"]
    else:
        for obj in objs:
            if argument in obj['attributes']:
                return ["yes"]
        return ["no"]


def process_choose(image_id, semantic, objs):
    argument = semantic['argument']
    choose_options = list()
    if 'rel' in semantic['operation']:
        argument = argument.split('(')[0][:-1]
        relation = argument.split(',')
        relation[1] = relation[1].split('|')
        targets = sgs[image_id]['objects']
        if relation[2] == 'o':
            for obj in objs:
                for rel in obj['relations']:
                    if rel['name'] in relation[1] and targets[rel['object']]['name'] == relation[0]:
                        choose_options.append(rel['name'])
            return list(set(choose_options))
        else:
            for obj in objs:
                for idx, target in targets.items():
                    if target['name'] == relation[0]:
                        for rel in target['relations']:
                            if rel['name'] in relation[1] and rel['object'] == obj['id']:
                                choose_options.append(rel['name'])
            return list(set(choose_options))
    elif 'name' in semantic['operation']:
        argument = argument.split('|')
        for obj in objs:
            for ele in argument:
                if ele == obj['name']:
                    choose_options.append(ele)
        return list(set(choose_options))
    else:
        argument = argument.split('|')
        for obj in objs:
            for ele in argument:
                if ele in obj['attributes']:
                    choose_options.append(ele)
        return list(set(choose_options))


def parse_arg(semantic):
    is_filter = False
    is_select = False
    rel = []
    argument = semantic['argument']
    if 'filter' in semantic['operation']:
        is_filter = True
    elif 'select' == semantic['operation']:
        is_select = True
    elif 'relate' not in semantic['operation']:
        return {}
    args = argument.split(' (')
    obj = args[0]
    if not is_filter and len(args) != 1 and '-' not in args[1]:
        obj_id = args[1].split(')')[0]
    else:
        obj_id = "-1"
        if is_filter:
            obj = argument
    if len(obj.split(',')) > 1:
        obj = obj.split(',')
        rel = obj[1:]
        obj = obj[0]
    arg_dict = {
        'id': obj_id,
        'obj': obj,
        'dependencies': semantic['dependencies'],
        'relate': rel,
        'filter': is_filter,
        'select': is_select
    }
    return arg_dict


def expand(qid):
    expand_path = qs[qid]['semantic'].copy()
    added_path = list()
    possible_objs = list()
    idx = 0
    while expand_path:
        # choose the first expand node
        added_path.append(expand_path[0])
        expand_path.remove(expand_path[0])
        # find corresponding object in scene graph
        cur_arg = parse_arg(added_path[idx])
        if cur_arg:
            # select/filter/relate node
            image_id = qs[qid]['imageId']
            if cur_arg['select']:
                selected_objs = find_select_from_scene_graph(image_id, cur_arg)
                possible_objs.append(selected_objs)
            elif cur_arg['filter']:
                attribute = cur_arg['obj']
                dep = cur_arg['dependencies'][0]
                filtered_objs = find_filter_from_scene_graph(attribute, possible_objs[dep])
                possible_objs.append(filtered_objs)
            elif cur_arg['relate']:
                relation = cur_arg
                dep = cur_arg['dependencies'][0]
                related_objs = find_relate_from_scene_graph(image_id, relation, possible_objs[dep])
                possible_objs.append(related_objs)
        else:
            # question node
            image_id = qs[qid]['imageId']
            dep = added_path[idx]['dependencies']
            op_type = added_path[idx]['operation'].split()[0]
            if op_type == 'query':
                ret = process_query(qid, added_path[idx], possible_objs[dep[0]])
                possible_objs.append(ret)
            elif op_type == 'verify' or op_type == 'exist':
                ret = process_verify(image_id, added_path[idx], possible_objs[dep[0]])
                possible_objs.append(ret)
            elif op_type == 'choose':
                ret = process_choose(image_id, added_path[idx], possible_objs[dep[0]])
                possible_objs.append(ret)
            elif op_type == 'or':
                flag = False
                for ele in dep:
                    if possible_objs[ele] == ["yes"]:
                        possible_objs.append(["yes"])
                        flag = True
                        break
                if not flag:
                    possible_objs.append(["no"])
            elif op_type == 'and':
                flag = False
                for ele in dep:
                    if possible_objs[ele] == ["no"]:
                        possible_objs.append(["no"])
                        flag = True
                        break
                if not flag:
                    possible_objs.append(["yes"])
            else:
                possible_objs.append([""])

        idx += 1
    return possible_objs[-1]


if __name__ == "__main__":
    label = dict()
    for key, value in qs.items():
        expansion = expand(key)
        if value['answer'] in expansion or value['answer'] == '':
            expansion.remove(value['answer'])
        else:
            expansion.append('lost_answer')
        label[key] = {
            'img_id': value['imageId'],
            'label': {value['answer']: 1.0},
            'question_id': key,
            'sent': value['question'],
            'other_answers': expansion
        }
    with open('scene_graph_check_solution_val.json', 'w') as f:
        json.dump(label, f, indent=4)
    # expand("15899542") # semantic - 'food', scene graph - 'pizza'
    # expand("17141268") # no 'top'/'bottom' attribute in scene graph
    # expand('19238758')
