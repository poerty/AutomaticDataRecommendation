from collections import Counter
import random


class LDA():
    def __init__(self, x, y, num_label):
        self.documents_topics=[]
        self.document_topic_counts=[]

        onehot = np.zeros((len(y), num_label))
        onehot[np.arange(len(y)), y] = 1
        self.y = onehot
        self.num_data = self.x.shape[0]
        self.num_feature = self.x.shape[1]

        self.num_label = num_label
        self.w = np.zeros((self.num_feature,self.num_label))
    def p_topic_given_document(topic, d, alpha=0.1):
        return ((document_topic_counts[d][topic] + alpha) /
            (document_lengths[d] + K * alpha))

    def p_word_given_topic(word, topic, beta=0.1):
        return ((topic_word_counts[topic][word] + beta) /
                (topic_counts[topic] + V * beta))

    def topic_weight(d, word, k):
        return p_word_given_topic(word, k) * p_topic_given_document(k, d)

    def choose_new_topic(d, word):
        return sample_from([topic_weight(d, word, k) for k in range(K)])

    def sample_from(weights):
        total = sum(weights)
        rnd = total * random.random()
        for i, w in enumerate(weights):
            rnd -= w
            if rnd <= 0:
                return i

    def train_topic(documents,K=4):
        random.seed(0)
        #K=4
        document_topics = [[random.randrange(K) for word in document]
                            for document in documents]
        document_topic_counts = [Counter() for _ in documents]
        topic_word_counts = [Counter() for _ in range(K)]
        topic_counts = [0 for _ in range(K)]
        document_lengths = [len(document) for document in documents]
        distinct_words = set(word for document in documents for word in document)
        V = len(distinct_words)
        D = len(documents)

        for d in range(D):
            for word, topic in zip(documents[d], document_topics[d]):
                document_topic_counts[d][topic] += 1
                topic_word_counts[topic][word] += 1
                topic_counts[topic] += 1

        for iter in range(1000):
            for d in range(D):
                for i, (word, topic) in enumerate(zip(documents[d],
                                                    document_topics[d])):
                    document_topic_counts[d][topic] -= 1
                    topic_word_counts[topic][word] -= 1
                    topic_counts[topic] -= 1
                    document_lengths[d] -= 1
                    new_topic = choose_new_topic(d, word)
                    document_topics[d][i] = new_topic
                    document_topic_counts[d][new_topic] += 1
                    topic_word_counts[new_topic][word] += 1
                    topic_counts[new_topic] += 1
                    document_lengths[d] += 1

lda=LDA()
documents = [["Hadoop", "Big Data", "HBase", "Java", "Spark", "Storm", "Cassandra"],
            ["NoSQL", "MongoDB", "Cassandra", "HBase", "Postgres"],
            ["Python", "scikit-learn", "scipy", "numpy", "statsmodels", "pandas"],
            ["R", "Python", "statistics", "regression", "probability"],
            ["machine learning", "regression", "decision trees", "libsvm"],
            ["Python", "R", "Java", "C++", "Haskell", "programming languages"],
            ["statistics", "probability", "mathematics", "theory"],
            ["machine learning", "scikit-learn", "Mahout", "neural networks"],
            ["neural networks", "deep learning", "Big Data", "artificial intelligence"],
            ["Hadoop", "Java", "MapReduce", "Big Data"],
            ["statistics", "R", "statsmodels"],
            ["C++", "deep learning", "artificial intelligence", "probability"],
            ["pandas", "R", "Python"],
            ["databases", "HBase", "Postgres", "MySQL", "MongoDB"],
            ["libsvm", "regression", "support vector machines"]]
lda.train_topic(documents)