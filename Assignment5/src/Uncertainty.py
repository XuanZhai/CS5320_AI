import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
import io  
import random
import copy
from nltk.corpus import stopwords  
from nltk.tokenize import word_tokenize  
import string
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('english')



def readfile(Trainingset, Testingset):
    total = []
    stop_words = set(stopwords.words('english'))        # Use the nltk stopwords
    stop_words.add('u')                                 # Add two more 
    stop_words.add('i')
    punct = set(string.punctuation)                         # Punctuations and numbers need to be removed 
    number = ['1','2','3','4','5','6','7','8','9','0']
    with open("smsspamcollection/SMSSpamCollection", encoding='gb18030', errors='ignore') as f:
        while True:                             
            line = f.readline()
            if not line:                                # If reaching the end of line, stop
                break
            tokens = nltk.word_tokenize(line)           # Tokenize the line 
            newline = [] 
        
            for word in tokens:                     # First removing the stop words, then stem and remove punc/numbers
                if not word in stop_words:
                    for d in word:
                        if d in punct or d in number:
                            word = word.replace(d, "")
                    newword = stemmer.stem(word)        # Use nltk snowball for stemming 
                    if not newword in stop_words and len(newword) > 0:      # remove stop words again before inserting into the list
                        newline.append(newword)   
            total.append(newline)
    
    trainingindex = random.randint(0,len(total)-1)
    trainingsize = int(len(total)*0.8)
    for i in range(trainingsize):                       # Randomly choose 80% of total lines and put them into trainingset
        Trainingset.append(total[trainingindex])
        total.pop(trainingindex)
        trainingindex = random.randint(0,len(total)-1)
    
    for line in total:
        Testingset.append(line)                     # Else go to the testingset

def analyzeDataset(Trainingset, Testingset, vis):
    wordlist = {}                           # Use a hash table to store words
    for line in Trainingset:
        for i in range(len(line)):
            if(i != 0):
                if line[i] in wordlist:
                    wordlist[line[i]] = wordlist[line[i]] + 1       # The value in the hash table is the total number of words
                else:
                    wordlist[line[i]] = 1
    

    for line in Testingset:
        for i in range(len(line)):
            if(i != 0):
                if line[i] in wordlist:
                    wordlist[line[i]] = wordlist[line[i]] + 1       # The value in the hash table is the total number of words
                else:
                    wordlist[line[i]] = 1
    
    newlist = sorted(wordlist.items(), key=lambda x: x[1], reverse=True) # Sort the hash table by keys to get the top/last words
    
    if vis is True:
        print("Printing the top 20 frequent words:")
        for i in range(20):
            print("top", i+1, "are", newlist[i])
    
        print("\nPrinting the last 20 frequent words:")
        for j in range(20):
            print("last",j+1, "are", newlist[len(newlist)-j-1])
    


def analyzeTraining(Trainingset, prior, dataset, vis): # The keys in the dataset are words, values are a list [P(word|spam), P(word|ham)]
    wordlist = {}                   # A training wordlist keys are words, values are a list of spam or ham it has (so that we can know
    nspam = 0                       # the number of spam/ham emails it appears)
    nham = 0
    
    for currentline in Trainingset:
        currentstatus = currentline[0]              # Record whether it's ham or spam
        
        for j in range(len(currentline)):
            if(j != 0):       
                if currentline[j] in wordlist:
                    wordlist[currentline[j]].append(currentstatus)
                else:
                    wordlist[currentline[j]] = []
                    wordlist[currentline[j]].append(currentstatus)
                    
        if (currentstatus == "spam"):
            nspam = nspam + 1
        else:
            nham = nham + 1

    spamwordlist = {}       # A word list with P(word|spam) only
    hamwordlist = {}        # A word list with P(word|ham) only

    for word in wordlist.keys():            # Analyze the probability based on the Bayes model
        resultlist = wordlist[word]
        cnspam = 0
        cnham = 0
        
        for result in resultlist:
            if(result == "spam"):
                cnspam = cnspam + 1
            else:
                cnham = cnham + 1

        pnspam = (cnspam + 1) / (nspam + 2)         # The Bayes model with Laplacian smoothing 
        pnham = (cnham + 1) / (nham + 2)

        if vis is True:
            spamwordlist[word] = pnspam
            hamwordlist[word] = pnham
        dataset[word] = [pnspam, pnham]         # Insert those conditional probability into tables
      
    prior.append(nspam / len(Trainingset))  
    prior.append(nham / len(Trainingset))
    
    if vis is True:
        newspamlist = sorted(spamwordlist.items(), key=lambda x: x[1], reverse=True)
        newhamlist = sorted(hamwordlist.items(), key=lambda x: x[1], reverse=True)

        print("Printing the 20 words with the greatest conditional probability of spam:")
        for i in range(20):
            print("top", i+1, "are", newspamlist[i])
    
        print("\nPrinting the 20 words with the greatest conditional probability of ham:")
        for j in range(20):
            print("top",j+1, "are", newhamlist[j])

        
def analyzeTesting(Testingset, prior, dataset, vis):
    correctsize = 0
    
    for currentline in Testingset:
    
        currentps = prior[0]
        currentph = prior[1]
        answer = currentline[0]
            
        for j in range(1,len(currentline)):
            currenword = currentline[j]
            if currenword in dataset:
                currentps = currentps * dataset[currenword][0]           # Use equation to find the probability of [spam|message]
                currentph = currentph * dataset[currenword][1]      # Use equation to find the probability of [ham|message]
        
        
        if(currentps > currentph and answer == "spam"):                 # Check whether it is correct
            correctsize = correctsize + 1
            
        elif(currentps <= currentph and answer == "ham"):
            correctsize = correctsize + 1
        else:
            if(vis == True and answer == "ham"):
                print(currentline,"Should be", answer, "actually got spam")
            elif(vis == True and answer == "spam"):
                print(currentline,"Should be", answer, "actually got ham")
    return correctsize/len(Testingset) * 100      
                
           
        
def analyzeTesting_improve1(Testingset, prior, dataset, c, vis):
    correctsize = 0
    
    for currentline in Testingset:
    
        currentps = prior[0]
        currentph = prior[1]
        answer = currentline[0]
            
        for j in range(1,len(currentline)):
            currenword = currentline[j]
            if currenword in dataset:
                currentps = currentps * dataset[currenword][0]           # Use equation to find the probability of [spam|message]
                currentph = c * currentph * dataset[currenword][1]      # Use equation to find the probability of [ham|message]
        
        
        if(currentps > currentph and answer == "spam"):                 # Check whether it is correct
            correctsize = correctsize + 1
            
        elif(currentps <= currentph and answer == "ham"):
            correctsize = correctsize + 1
        else:
            if(vis == True and answer == "ham"):
                print(currentline,"Should be", answer, "actually got spam")
            elif(vis == True and answer == "spam"):
                print(currentline,"Should be", answer, "actually got ham")
    return correctsize/len(Testingset) * 100              
    
    



