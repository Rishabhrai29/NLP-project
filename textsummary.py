import spacy
import heapq
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

text=""" Software development is a complex and dynamic field that encompasses the design creation testing and maintenance of software applications and systems. It involves a variety of stages including requirement analysis where the needs and goals of the software are defined, and design, where the architecture and interface of the software are planned. The actual coding phase follows, where developers write the source code using programming languages suited to the project's requirements. This is often accompanied by rigorous testing to identify and fix bugs ensuring the software functions as intended. Post-development the software undergoes deployment, making it available for users, and continuous maintenance to update and improve its performance fix issues, and adapt to changing user needs or environments. Agile methodologies, such as Scrum and Kanban are commonly employed to manage the development process, promoting iterative progress collaboration and flexibility. """

def summarizer(rawdocs): 
    stopwords=list(STOP_WORDS);
    #print(stopwords);
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)
    tokens=[token.text for token in doc]
    #print(tokens)
    word_freq={}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text]=1
            else:
                word_freq[word.text] +=1

    #print(word_freq)

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word]=word_freq[word]/max_freq

    #print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    #print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text]

    #print(sent_scores) 
    select_len = int(len(sent_tokens) * 0.3)
    #print(select_len)

    summary =heapq.nlargest(select_len,sent_scores,key = sent_scores.get)
    #print(summary)

    final_summary=[word.text for word in summary]
    summary =' '.join(final_summary)
    #print(summary)

    #print("length of the original String : ",len(text.split(' ')))
    # print("length of the Updated String : ",len(summary.split(' ')))
    return summary,doc,len(rawdocs.split(' ')),len(summary.split(' '))
