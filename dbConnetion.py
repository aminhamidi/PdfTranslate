import os
import sqlite3
import io
import json,os



if os.path.exists("words.db"):
        os.remove("words.db")

con = sqlite3.connect('words.db', check_same_thread=False)

cur = con.cursor()

def insert_word_from_csv_to_db():
    try:
        if cur.execute(f"SELECT * FROM words WHERE  index_=\"1\" AND is_deleted=False ") == None:
            cur.execute('''CREATE TABLE IF NOT EXISTS words
                    (index_,en,fa,pronunciation,example,words_category,description,is_deleted)''')

            f = io.open("a.csv", mode="r", encoding="utf-8")

            print(f)

            words = f.read().split("\n")

            for count, value in enumerate(words):
                temp = ''
                if count != 0:
                    if len(value.split(",")[1]) != 0:
                        for x in value.split(","):
                            if len(x) == 0:
                                temp += "NULL,"
                            if len(x) != 0:
                                temp += "\""+str(x)+"\""+","
                        temp += "NULL,FALSE"
                        cur.execute(f"INSERT INTO words VALUES ({temp})")
                        temp = None
    except:
        cur.execute('''CREATE TABLE IF NOT EXISTS words
                    (index_,en,fa,pronunciation,example,words_category,description,is_deleted)''')

        f = io.open("a.csv", mode="r", encoding="utf-8")

        words = f.read().split("\n")

        for count, value in enumerate(words):
            temp = ''
            if count != 0:
                if len(value.split(",")[1]) != 0:
                    for x in value.split(","):
                        if len(x) == 0:
                            temp += "NULL,"
                        if len(x) != 0:
                            temp += "\""+str(x)+"\""+","
                    temp += "NULL,FALSE"
                    cur.execute(f"INSERT INTO words VALUES ({temp})")
                    temp = None


insert_word_from_csv_to_db()


def sender_(resualt):
    if resualt == None:
        return 'None'
    res = {
        "index_": resualt[0],
        "en": resualt[1],
        "fa": resualt[2],
        "pronunciation": resualt[3],
        "example": resualt[4],
        "words_category": resualt[5],
        "description": resualt[6],
        "is_deleted": resualt[7]
    }
    return json.dumps(res)


def create_(en=None, fa=None, pronunciation=None, example=None, words_category=None, description=None, is_deleted=False):
    index_ = int(len(cur.execute("SELECT *  FROM words").fetchall())) + 1
    cur.execute(
        f"INSERT INTO words VALUES (\"{index_}\",\"{en}\",\"{fa}\",\"{pronunciation}\",\"{example}\",\"{words_category}\",\"{description}\",{is_deleted})")
    return 'True'


# create_(1, 'a', 'a', 'a', 'a', 'a', False)


def read_(column_name, column_value):
    res = cur.execute(
        f"SELECT * FROM words WHERE  {column_name}=\"{column_value}\" AND is_deleted=False ")
    return sender_(res.fetchone())


# print(read_('index_', '410'))

# print(
#     json.loads(read_('index_', '410'))['fa']
#     )
# read_('en', 'cook')

def readAll_():
    temp = {}
    res = cur.execute(
        f"SELECT * FROM words WHERE is_deleted=False ")
    for count, value in enumerate(res):
        temp[count+1] = sender_(value)
    return json.dumps(temp)


# print(readAll_())
# readAll_()


def update_(index_, column_name, new_value):
    if read_('index_', index_) == 'None':
        return 'None'
    cur.execute(
        f"UPDATE words SET {column_name}=\"{new_value}\" WHERE index_=\"{index_}\" AND is_deleted=False ")
    return 'True'


# print(update_('410', 'description', None))


def delete_(index_):
    if read_('index_', index_) == None:
        return 'None'
    cur.execute(
        f"UPDATE words SET is_deleted=TRUE WHERE index_=\"{index_}\"")
    return 'True'

# delete_("417")


# print(readAll_())


# print(cur.execute("SELECT *  FROM words").fetchall())
# print(len(cur.execute("SELECT *  FROM words").fetchall()))


con.commit()

# con.close()
