import string
import re
from config.json_file import *
from config.constant import *
from collections import Counter
from underthesea import sent_tokenize, word_tokenize


def create_relevance():
    train = JSONFile(TRAIN_QUESTION_ANSWER)
    test = JSONFile(PUBLIC_TEST_QUESTION)

    num_labels = []

    for item in train.items:
        num_labels.extend([(i["law_id"], i["article_id"]) for i in item["relevant_articles"]])

    cnt = Counter(num_labels)
    with open(RELEVANT, "w") as f:
        for k, v in sorted(cnt.items(), key=lambda x: x[1]):
            f.write("%s\n" % get_key(k[0], k[1]))


def create_preprocessed():
    corpus = json.load(open(LEGAL_CORPUS))

    laws_id = []
    laws_articles = []
    with open(RELEVANT) as f:
        for line in f:
            l_id, a_id = line.split(" # ")
            laws_id.append(l_id)
            laws_articles.append(line.strip())

    laws = [law for law in corpus if law["law_id"] in set(laws_id)]
    articles = [(get_key(law["law_id"], a["article_id"]), a) for law in laws for a in law["articles"] if
                get_key(law["law_id"], a["article_id"]) in set(laws_articles)]

    with open(INDEX_FILE, "w") as f_index, open(TITLE_FILE, "w") as f_title, open(TEXT_FILE, "w") as f_text:
        for a in articles:
            f_index.write("%s\n" % a[0])
            f_title.write("%s\n" % a[1]["title"])
            f_text.write("%s\n" % preprocess_text(a[1]["text"]))


def get_key(law_id, article_id):
    return law_id + " # " + article_id


def preprocess_text(paragraph):
    sentences = sent_tokenize(paragraph)
    processed = []
    for sent in sentences:
        if len(sent) < MIN_LEN_PER_SENTENCE:
            continue
        sent = re.sub(r"\b\d+.", "", sent)
        processed_sent = str(sent).lower()\
            .translate(str.maketrans('', '', string.punctuation + string.whitespace.replace(" ", "")))
        tokens = word_tokenize(processed_sent)
        processed.extend(tokens)
    return "|".join(processed)


if __name__ == "__main__":
    create_relevance()
    create_preprocessed()

