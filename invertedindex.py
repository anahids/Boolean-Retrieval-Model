import re
import operator

# This function opens and reads the file, also it does a split when finding a line break before an .I
def processFile():
    with open('cran.all.1400','r') as file:
        contents = file.read()
        docs = contents.split('\n.I')
    return docs
#processFile()

# This function deletes the line breaks, upper letters, slash, parenthesis, numbers, commas, dots, etc. and put the documents in a list, each element of the list is a document.         
def cleanDocs():
    alldocs = processFile()
    sinSaltos = ([doc.replace('\n',' ') for doc in alldocs])
    sinMayus = [re.sub('[ITABW]', ' ', doc) for doc in sinSaltos]
    sinSlash = [re.sub('/', '', doc) for doc in sinMayus]
    sinParent1 = ([doc.replace('(','') for doc in sinSlash])
    sinParent2 = ([doc.replace(')','') for doc in sinParent1])
    sinNums = [re.sub(r'\d', '', doc) for doc in sinParent2]
    sinComas = ([doc.replace(',','') for doc in sinNums])
    sinSignos = [re.sub(r'^\w+\.\s?', ' ', doc) for doc in sinComas]
    sinPalabrasComp = ([doc.replace('-',' ') for doc in sinSignos])
    clean = [" ".join(filter(str.isalpha,x.split(" "))) for x in sinPalabrasComp]
    
    return clean   
#cleanDocs()

# This function creates the inverted index, through a dictionary.
def createInvertedIndex():
    docs = cleanDocs() # List of clean documents
    invertedIndex = {} # This dictionary will be our inverted index
    termCount = {} # Dictionary that will contain the frequency of the terms
    for index, doc in enumerate(docs): # iterate over the index(key of a document) and value of an item (text of document) in a list (of clean documents). It means we put an index(key) to every document in the list.
        #print("Index is: %d and value is %s:" % (index, doc))
        for term in doc.split(): # Do an split to each term in the document (Tokenize).
            termCount[term] = termCount.get(term,0)+1 # Tell us how many times each term occurs and put in the termCount dictionary each term with their frequency.
            if invertedIndex.get(term,False): # If the invertedIndex (inverted index) has a term(key) but not a value (posting list)
                if index not in invertedIndex[term]: # If the index(key of the document) is not in the posting list
                    invertedIndex[term].append(index) # Add the index(key of the document) to the posting list
            else: # If the term or key has a value (a document, posting list)
                invertedIndex[term] = [index] # The posting list will be the index (key of the document)
    return invertedIndex

# This function searchs the posting list of the term in the inverted index.
def searchTerms(term):
    invertedIndex = createInvertedIndex()
    if term in invertedIndex: # If the term is in the invertedIndex...
        # invertedIndex.get(term)
        for key in invertedIndex: # For each key of the invertedIndex...
            if key == term: # If the key is equal to the term
                #print(key,invertedIndex[key]) # Print the term and the posting list
                return invertedIndex[key] # Return the posting list of the term searched

# This function checks if a term is in the inverted index (invertedIndex).
def checkIfExistTerm(term):
    flag = True
    invertedIndex = createInvertedIndex()
    if term in invertedIndex: 
        flag = True
    else:
        flag = False
    
    return flag

def andOperator(p1,p2):
    set1 = set(p1)
    set2 = set(p2)
    result =  set1.intersection(set2)
    return result

def orOperator(p1,p2):
    set1 = set(p1)
    set2 = set(p2)
    result = set1.union(set2)
    return result 

def notOperator(p1,p2):
    set1 = set(p1)
    set2 = set(p2)
    result = set1.difference(set2)
    return result

def andOROperator(p1,p2,p3):
    resultOR = list(orOperator(p2,p3))
    result = andOperator(p1,resultOR)
    return result

def andNotOperator(p1,p2,p3):
    resultAnd = list(andOperator(p1,p2))
    result = notOperator(resultAnd, p3)
    return result

def orNotOperator(p1,p2,p3):
    resultOR = list(orOperator(p1,p2))
    result = notOperator(resultOR, p3)
    return result

def notAndOrOperator(p1,p2,p3):
    resultOR = list(orOperator(p2,p3))
    result = notOperator(p1,resultOR)
    return result

# This function is for the first three options of the menu, because they only receive two terms.
# Firts ask for the two terms, then checks if both terms are in the invertedIndex.
# If both are in the invertedIndex, then search the posting list for both and depending of the option chose,
# it do a boolean operator.
# If none of the terms or if one of the terms is not in the invertedIndex, then it print the term that is not in it.
def chooseOption1or2or3(option):
    print("Enter the first term: ")
    term1 = input()
    print("Enter the second term:")
    term2 = input()
    
    flag1 = checkIfExistTerm(term1)
    flag2 = checkIfExistTerm(term2)

    if flag1 == True and flag2 == True:
        postingList1 = searchTerms(term1)
        postingList2 = searchTerms(term2)
        if option == '1':
            print(andOperator(postingList1,postingList2))
        elif option == '2':
            print(orOperator(postingList1,postingList2))
        elif option == '3':
            print(notOperator(postingList1,postingList2))
    elif flag1 == True and flag2 == False:
        print(term2 + " is not in the inverted index")
    elif flag1 == False and flag2 == True:
        print(term1 + " is not in the inverted index")
    else:
        print("Both terms are not in the inverted index")

# This function is like the "chooseOption1or2or3()" function but with three terms.
def chooseOption4to7(option):
    print("Enter the first term: ")
    term1 = input()
    print("Enter the second term:")
    term2 = input()
    print("Enter the third term:")
    term3 = input()
    
    flag1 = checkIfExistTerm(term1)
    flag2 = checkIfExistTerm(term2)
    flag3 = checkIfExistTerm(term3)

    if flag1 == True and flag2 == True and flag3 == True:
        postingList1 = searchTerms(term1)
        postingList2 = searchTerms(term2)
        postingList3 = searchTerms(term3)
        if option == '4':
            print(andOROperator(postingList1,postingList2,postingList3))
        
        elif option == '5':
            print(andNotOperator(postingList1, postingList2, postingList3))
        elif option == '6':
            print(orNotOperator(postingList1, postingList2, postingList3))
        elif option == '7':
            print(notAndOrOperator(postingList1, postingList2, postingList3))
    elif flag1 == True and flag2 == False and flag3 == True:
        print(term2 + " is not in the inverted index")
    elif flag1 == False and flag2 == True and flag3 == True:
        print(term1 + " is not in the inverted index")
    elif flag1 == True and flag2 == True and flag3 == False:
        print(term3 + " is not in the inverted index")
    elif flag1 == True and flag2 == False and flag3 == False:
        print("The term2 and term3 are not in the inverted index")
    elif flag1 == False and flag2 == True and flag3 == False:
        print("The term1 and term3 are not in the inverted index")
    elif flag1 == False and flag2 == False and flag3 == True:
        print("The term1 and term2 are not in the inverted index")
    else:
        print("The terms are not in the inverted index")

# This function creates the menu for the user, so he/she can choose a type of boolean query
def createMenuForUser():
    
    print("Choose a type of boolean query:")
    print("1 term1 AND term2")
    print("2 term1 OR term2")
    print("3 term1 AND NOT term2")
    print("4 term1 AND (term2 OR term3)")
    print("5 (term1 AND term2) AND NOT term3")
    print("6 (term1 OR term2) AND NOT (term3)")
    print("7 (term1) AND NOT (term2 OR term3)")

    option = input()

    if option == '1' or option == '2' or option == '3':
        chooseOption1or2or3(option)
    elif option == '4' or option == '5' or option == '6' or option == '7':
        chooseOption4to7(option)
    else: 
        print("Invalid option, choose one of the options")

createMenuForUser()