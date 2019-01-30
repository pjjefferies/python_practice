def censor(text, word):
    word_replace = "*" * len(word)
    for i in range(len(text)):
        print (i, text[i], word[0])
        if text[i] == word[0]:
            for j in range(len(word)):
                print (i, j, text[i+j], word[j])
                if text[i+j] != word[j]:
                    break
            else:
                print (text, word, word_replace)
                text = text.replace(word, word_replace)
    return text

print (censor("Now is the time for all good men to come to the aid of their country", "to"))
