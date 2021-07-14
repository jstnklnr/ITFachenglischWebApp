import database_interface as dbi
import os

db = dbi.Database(f"{os.path.dirname(__file__)}/../Database/database.db")
books = db.query_dict("SELECT * FROM books")
topics = db.query_dict("SELECT * FROM topics")
vocabulary = db.query_dict("SELECT * FROM vocabulary")
languages = db.query_dict("SELECT * FROM languages")
words = {}

for word in vocabulary:
    words[word["word"]] = {"book": word["book"], "unit": word["unit"], "topic": word["topic"], "translation": word["translation"]}

def get_book_id(book):
    for b in books:
        if b["book"] == book:
            return b["id"]

    return None

def get_topic_id(topic):
    for t in topics:
        if t["topic"] == topic:
            return t["id"]

    return None

def get_language_id(language):
    for l in languages:
        if l["language"] == language:
            return l["id"]

    return None

def migrate_vocabulary():
    with open(f"{os.path.dirname(__file__)}/vocabulary.csv", "r") as f:
        rowNumber = 0
        
        for row in f:
            rowNumber += 1

            if rowNumber == 1:
                continue

            data = row.split(";")
            book_id = get_book_id(data[0])

            if not book_id:
                print(f"no book: {data[0]} - {book_id} - {data[1]}")
                continue

            result = db.query_dict("SELECT units.id FROM units JOIN books ON books.id = units.book WHERE units.number = ? AND books.book = ?", tuple([int(data[1].split("-")[0].replace(" ", "")), data[0]]), True)
            
            if not result:
                print(f"no unit: {data[0]} - {book_id} - {data[1]}")
                continue

            unit_id = result["id"]
            topic_id = get_topic_id(data[2])
            german_words = data[3].replace("\n", "").split(",")
            english_word = data[4].replace("\n", "").strip()

            translation_id = -1

            if not topic_id:
                continue

            if english_word in words:
                translation_id = words[english_word]["translation"]
            else:
                db.query_dict("INSERT INTO translations DEFAULT VALUES")
                translation_id = db.query_dict("SELECT * FROM translations ORDER BY id DESC LIMIT 1", one = True)["id"]

                db.insert("vocabulary", {"book": book_id, "unit": unit_id, "topic": topic_id, "language": get_language_id("English"), "word": english_word, "translation": translation_id})
                words[english_word] = {"book": book_id, "unit": unit_id, "topic": topic_id, "translation": translation_id}

            for word in german_words:
                word = word.strip()

                db.insert("vocabulary", {"book": book_id, "unit": unit_id, "topic": topic_id, "language": get_language_id("German"), "word": word, "translation": translation_id})
                words[word] = {"book": book_id, "unit": unit_id, "topic": topic_id, "translation": translation_id}

def migrate_phrases():
    with open(f"{os.path.dirname(__file__)}/phrases.csv", "r") as f:
        rowNumber = 0
        
        for row in f:
            rowNumber += 1

            if rowNumber == 1:
                continue

            data = row.split(";")
            db.query_dict("INSERT INTO translations DEFAULT VALUES")
            translation_id = db.query_dict("SELECT * FROM translations ORDER BY id DESC LIMIT 1", one = True)["id"]

            db.insert("phrases", {"language": get_language_id("English"), "phrase": data[0], "audio": data[2], "translation": translation_id})
            db.insert("phrases", {"language": get_language_id("German"), "phrase": data[1], "audio": None, "translation": translation_id})

migrate_phrases()
db.close()
print("Finished migrating")