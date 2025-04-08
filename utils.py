import os
import math
import re
from collections import Counter, defaultdict
import spacy
from mylog import log

# Загружаем модель spaCy для русского языка
nlp = spacy.load("ru_core_news_sm")

# Токенизация + лемматизация
def tokenize(text):
    text = re.sub(r'[^а-яА-Яa-zA-Z0-9\s]', '', text)
    doc = nlp(text.lower())
    return [token.lemma_ for token in doc if token.is_alpha]

# Получить список файлов
def get_all_filenames(folder_path):
    return sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

# Расчёт TF-IDF для одного файла
def compute_tf_idf_for_file(target_filename, folder_path):
    documents = {}
    df = defaultdict(int)
    total_docs = 0

    # Считываем все документы
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as f:
                tokens = tokenize(f.read())
                documents[filename] = tokens
                total_docs += 1
                for word in set(tokens):
                    df[word] += 1
    log(df, documents)
    # TF для выбранного документа
    target_tokens = documents.get(target_filename, [])
    word_counts = Counter(target_tokens)
    log(word_counts)
    total_words = len(target_tokens)
    log(total_words)
    tf_idf_data = []

    for word, tf in word_counts.items():
        tf = tf / total_words
        idf = math.log(total_docs / df[word])
        tf_idf = tf * idf
        tf_idf_data.append((word, round(tf, 4), round(idf, 4), round(tf_idf, 4)))

    tf_idf_data.sort(key=lambda x: x[3], reverse=True)
    return tf_idf_data[:50]
