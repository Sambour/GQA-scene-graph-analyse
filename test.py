import os
import json


def get_a_short_example_of_questions():
    '''
    qas = []
    with open("train_all_questions/train_all_questions_0.json", 'r') as f:
        qas = json.load(f)
    qas = {key:value for key, value in list(qas.items())[:200]}
    with open('test.json', 'w') as f:
        json.dump(qas, f, indent=4)
    '''
    with open('train_balanced_questions.json', 'r') as f:
        qas = json.load(f)
    small_qas = {'111007521': qas['111007521'], '00569849': qas['00569849'], '17616592': qas['17616592'], }
    with open('test.json', 'w') as f:
        json.dump(small_qas, f, indent=4)


def get_semantic_operation():
    ops = []
    with open("val_all_questions.json", "r") as f:
        qas = json.load(f)
        for key, value in qas.items():
            flag = 0
            for semantic in value['semantic']:
                if semantic['operation'] not in ops:
                    ops.append(semantic['operation'])
                if 'select' in semantic['operation']:
                    flag = 1
            if flag == 0:
                print(key, flag)
    # with open('semantic_ops.json', 'w') as f:
        # json.dump(ops, f, indent=4)


def get_all_query_types():
    types = []
    with open("val_balanced_questions.json", "r") as f:
        qas = json.load(f)
        for key, value in qas.items():
            for semantic in value['semantic']:
                if semantic['operation'] == 'query' and semantic['argument'] not in types:
                    types.append(semantic['argument'])

    with open("train_balanced_questions.json", "r") as f:
        qas = json.load(f)
        for key, value in qas.items():
            for semantic in value['semantic']:
                if semantic['operation'] == 'query' and semantic['argument'] not in types:
                    types.append(semantic['argument'])
    with open('query_types.json', 'w') as f:
        json.dump(types, f, indent=4)


def get_instance_for_query_types():
    query_dict = dict()
    with open('query_types.json', 'r') as f:
        qlist = json.load(f)
        for query in qlist:
            query_dict[query] = list()
    with open("train_balanced_questions.json", "r") as f:
        qas = json.load(f)
        for key, value in qas.items():
            for semantic in value['semantic']:
                if semantic['operation'] == 'query'and semantic['argument'] != 'name'\
                        and value['answer'] not in query_dict[semantic['argument']]:
                    query_dict[semantic['argument']].append(value['answer'])
    with open("val_balanced_questions.json", "r") as f:
        qas = json.load(f)
        for key, value in qas.items():
            for semantic in value['semantic']:
                if semantic['operation'] == 'query'and semantic['argument'] != 'name'\
                        and value['answer'] not in query_dict[semantic['argument']]:
                    query_dict[semantic['argument']].append(value['answer'])
    with open('query_dict.json', 'w') as f:
        json.dump(query_dict, f, indent=4)


def get_object_types():
    with open('train_balanced_questions.json', 'r') as f:
        qs = json.load(f)
    with open('val_balanced_questions.json', 'r') as f:
        qs.update(json.load(f))

    with open('train_sceneGraphs.json', 'r') as f:
        sgs = json.load(f)
    with open('val_sceneGraphs.json', 'r') as f:
        sgs.update(json.load(f))

    lowerword_dict = dict()

    for key, value in qs.items():
        for semantic in value['semantic']:
            split = semantic['argument'].split(' (')
            if len(split) > 1:
                upper = split[0]
                obj_ids = split[1].split(')')[0]
                if 'rel' in semantic['operation']:
                    upper = upper.split(',')[0]
                if ',' in obj_ids:
                    obj_ids = obj_ids.split(',')
                else:
                    obj_ids = [obj_ids]
                for obj_id in obj_ids:
                    if '-' not in obj_id:
                        lower = sgs[value['imageId']]['objects'][obj_id]['name']
                        if upper not in lowerword_dict.keys() and upper != '_' and upper != 'this':
                            lowerword_dict[upper] = list()
                        if lower not in lowerword_dict[upper]:
                            lowerword_dict[upper].append(lower)

    with open('lower_word_dict.json', 'w') as f:
        json.dump(lowerword_dict, f, indent=4)


def analyze_scene_graph_check():
    with open('scene_graph_check_solution_val.json', 'r') as f:
        qas = json.load(f)
    wrong_cases = dict()
    for key, value in qas.items():
        if value['other_answers'] and 'no' not in value['label'].keys() and 'yes' not in value['label'].keys():
            if 'lost_answer' not in value['other_answers']:
                wrong_cases[key] = value
        elif value['label'] == {'no': 1.0} and 'yes' in value['other_answers']:
            value['other_answers'].remove('lost_answer')
            wrong_cases[key] = value
    with open('wrong_cases_val.json', 'w') as f:
        json.dump(wrong_cases, f, indent=4)
    print(len(wrong_cases)/len(qas))
    # print(list(wrong_cases.values())[:-5])


if __name__ == '__main__':
    # get_all_query_types()
    # get_instance_for_query_types()
    # get_object_types()
    analyze_scene_graph_check()
    # get_a_short_example_of_questions()
    # get_semantic_operation()
