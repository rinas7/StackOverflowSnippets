class QuestionRanker(object):

    def __init__(self, query, questions):
        self.query = query
        self.questions = questions

    def get_sorted_questions(self):
        ranked = []
        max_score = max([q['score'] for q in self.questions])
        is_query_negative = self.contains_negative_words(self.query)
        query_words = self.query.split()
        for question in self.questions:
            score = 0
            score += question['score'] / max_score
            matched_words = 0
            lower_title = question['title'].lower()
            for word in query_words:
                if word in lower_title:
                    matched_words += 1
            score += matched_words / len(query_words)
            if not is_query_negative:
                if self.contains_negative_words(question['title']):
                    score -= 0.4
            ranked.append((score, question))
        return [x[1] for x in sorted(ranked, key=lambda x: x[0], reverse=True)]

    def contains_negative_words(self, text):
        lower_text = text.lower()
        negative_words = (
            'error', 'issue', 'exception', 'fuck', 'problem',
            'not work')
        for word in negative_words:
            if word in lower_text:
                return True
        return False
