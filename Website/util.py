def getWordAmount(unit_topic_list:list, num_list:list, choosen_unit_topic:list):
    num = 0
    for element in choosen_unit_topic:
        idx = unit_topic_list.index(element)
        num += num_list[idx]

    return num

def addSpecificKeyValueToList(unit_topic_list:list, key_name:str):
    utList = []
    for element in unit_topic_list:
        utList.append(element[key_name])

    return utList