import re

def preprocess_text(text):
    """
    Preprocess Turkish text for sentiment analysis
    """
    # Convert to lowercase
    text = text.lower()
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def get_sample_texts():
    """
    Return a dictionary of sample Turkish texts for testing
    """
    return {
        "Pozitif Örnek 1": "Bu film gerçekten harikaydı! Oyuncular çok başarılıydı ve senaryo muhteşemdi.",
        "Pozitif Örnek 2": "Yemekler çok lezzetliydi, servis hızlıydı. Kesinlikle tekrar geleceğim.",
        "Negatif Örnek 1": "Hiç beğenmedim, zaman kaybından başka bir şey değildi.",
        "Negatif Örnek 2": "Çok kötü bir deneyimdi. Bir daha asla tercih etmem."
    }
