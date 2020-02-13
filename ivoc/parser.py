import re
import string

statuses = {'U': 'unknown', 'Y': 'known', 'N': 'name', 'W': 'not-word', '?': 'unknown'}

replacemap = [["who's", "who is"], ["'l", " will"], ["'re", " are"], ["don't", "do not"], ["it's", "it is"],
              ["haven't", "have not"], ["didn't", "did not"], ["i'm", "i am"], ["i'd", "i would"],
              ["should've", "should have"], ["that's", "that is"], ["doesn't", "does not"],
              ["hadn't", "had not"], ["wasn't", "was not"], ["i've", "i have"], ["'cause", "because"],
              ["could've", "could have"], ["you've", "you have"], ["isn't", "is not"],
              ["why'd", "why would"], ["'s", ""], ["'ve", " have"], ["won't", "would not"],
              ["can't", "can not"], ["n't", " not"], ["you'd", "you would"], ["'d", " would"]]

def get_class(word, db):
    if word.lower() in db.keys():
        return statuses.get(db[word.lower()]['status'], '')
    else:
        return 'new'

def append_word(buffer, word, db):
    span_class = get_class(word, db)
    return buffer + '<span class="word" data-status="%s" data-word="%s">%s</span>' % \
           (span_class, word.lower(), word)

def prepare(data, db):

    buffer = data

    for r in replacemap:
        buffer = buffer.replace(r[0], r[1])
        buffer = buffer.replace(r[0].capitalize(), r[1].capitalize())

    result = ''
    current_word = ''
    status = 'searching_word'

    for char in buffer:
        if status == 'searching_word' and char in string.ascii_letters:
            status = 'reading_word'
            current_word = char
        elif status == 'searching_word' and char not in string.ascii_letters:
            result = result + char
        elif status == 'reading_word' and char in string.ascii_letters:
            current_word = current_word + char
        elif status == 'reading_word' and char not in string.ascii_letters:
            result = append_word(result, current_word, db) + char
            current_word = ''
            status = 'searching_word'

    if current_word != '':
        result = append_word(result, current_word, db)

    result = '<p>%s</p>' % re.sub('\n\n', '</p><p>', result)
    result = '\n'.join(['<span class="line">%s</span>' % i for i in result.split('\n')])

    return result
