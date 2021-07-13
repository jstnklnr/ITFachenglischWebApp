from API import database_interface as dbi

db = dbi.Database("database")
books = db.query_dict("SELECT * FROM books")
topics = db.query_dict("SELECT * FROM topics")
words = {}

with open("") as f:
    rowNumber = 0
    
    for row in f:
        rowNumber += 1

        if rowNumber == 1:
            continue

        data = row.split(";")
        book_id = get_book_id(data[0])

        if not book_id:
            continue

        result = db.query_dict("SELECT * FROM units JOIN books ON books.id = units.book WHERE units.number = ? AND books.book = ?", tuple([int(data[1].split("-")[0].replace(" ", "")), data[0]]))
        
        if not result or len(result) <= 0:
            continue

        topic_id = get_topic_id(data[2])
        german_words = data[3].split(",")
        english_word = data[4]

        translation_id = -1

        if english_word in words:
            translation_id = words[english_word].translation
        else:
            db.query_dict("INSERT INTO translations")
            translation_id = db.query_dict("SELECT * FROM translations ORDER BY DESC LIMIT 1", one = True).id

        for word in german_words:
            word = word.strip()

            db.insert("vocabulary", {"book": book_id, "unit": unit_id, "topic": topic_id, })


def get_book_id(book):
    for b in books:
        if b.book == book:
            return b.id

    return None

def get_topic_id(topic):
    for t in topics:
        if t.topic == topic:
            return t.id

    return None