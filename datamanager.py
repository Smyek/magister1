import csv, re

amount = 195022

"""генератор: выдает по строке из таблиц (id, text)"""
def data_spewer(skipper=lambda x: False):
    for filename in ["positive", "negative"]:
        with open("data/%s.csv" % filename, "r", encoding="utf-8") as f:
            for line in f:
                elements = line.split('";"')
                if len(elements) != 12 or skipper(elements[3]): continue
                id, ttext = elements[0][1:], elements[3]
                yield [id, ttext]

def messages_with_hashtags():
    dataListOfLists = []
    for array in data_spewer(lambda x: True if not "#" in x else False):
        dataListOfLists.append(array)
    return dataListOfLists

def save_csv(filename, dataListOfLists, header=["id", "ttext"]):
    with open('data/output/%s.csv' % filename, 'w', encoding="utf-8", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        for array in dataListOfLists:
            writer.writerow(array)

def count():
    c = 0
    for i in data_spewer(): c += 1
    return c

def update_files():
    save_csv("hashtags_messages", messages_with_hashtags())

if __name__ == "__main__":
    #for id, ttext in data_spewer():
    update_files()
    pass