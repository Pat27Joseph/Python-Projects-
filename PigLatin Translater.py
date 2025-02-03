def pig_latin_translator(word):
    vowels = 'aeiou'
    word = word.lower()

    # Handle words that start with a vowel 
    if word[0] in vowels:
        return word + 'ay'
    
    # Handle word that start with "qu"
    if word.startswith('qu'):
        return word[2:] + 'quay'
    
    # Handle words that start with a consonant or consonant cluster 
    for i in range(len(word)):
        if word[i] in vowels:
            return word[i:] + word [:i] + 'ay'
    
    # Handle words no vowels
    return word + 'ay'

    # Example usage
words = input("Enter a word or sentence to translate to Pig Latin: ").split()
translated_words = [pig_latin_translator(word) for word in words]
print(" ".join(translated_words))
    