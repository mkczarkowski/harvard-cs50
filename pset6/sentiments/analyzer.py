import nltk
from tokenize import tokenize

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        
        """Load all words to given member without comments and whitespaces"""
        def load_data_to_set(set_name, set_path):
            with open(set_path) as lines:
                for line in lines:
                    if not line.startswith(";"):
                        set_name.add(line.strip())
        
        
        self.tokenizer = nltk.tokenize.casual.TweetTokenizer()
        self.positives = set()
        self.negatives = set()
        load_data_to_set(self.positives, positives)
        load_data_to_set(self.negatives, negatives)
    

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        score = 0
        tokens = self.tokenizer.tokenize(text)
        
        for token in tokens:
            token = token.lower()
            if token in self.positives:
                score += 1.0
            elif token in self.negatives:
                score -= 1.0
            else:
                score += 0.0
        
        return score
