
from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
from .utils import convert_pdf_to_text
from .api import get_data

from django.conf import settings


qstn1='''convert this text into json file exactly in the given format dont change the format 
{
  "personal_info": {
    "name": "Sandeepkumar Ulaganathan",
    "profession": "Associate Software Engineer",
    "email":"9sandeepsheenu@gmail.com",
    "mobile":"9092221669"

  },
  "skills": [
    "Python",
    "Apex",
    "Aura component",
    "SOQL/SOSL",
    "HTML",
    "CSS",
    "Agile",
    "Microsoft Office",
    "Adaptability",
    "Time management"
  ],
  "total_experience_in_years": " give total number of experience here only in numbers "
}"  '''
def upload_documents(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_files = request.FILES.getlist('uploaded_files')
            for uploaded_file in uploaded_files:
                # Process one document at a time
                text_content = convert_pdf_to_text(uploaded_file)
                json_data = get_data(qstn1,text_content)
                
                # Create a new Document instance for each uploaded document
                document = Document()
                document.uploaded_file = uploaded_file
                document.text_content = text_content
                document.json_data = json_data
                document.save()
                
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'parse/upload_documents.html', {'form': form})


def ret(request):
    return render(request, 'uploads/')
    

from django.shortcuts import render
from .models import Document
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token.lower() not in stop_words]
    return ' '.join(tokens)

def compare_texts(text1, text2):
    vectorizer = TfidfVectorizer()
    vector1 = vectorizer.fit_transform([text1])
    vector2 = vectorizer.transform([text2])
    similarity = cosine_similarity(vector1, vector2)
    return similarity[0][0]

def compare_text_with_jd(provided_text, jd_texts):
    provided_text = preprocess_text(provided_text)

    similarities = []

    for key, jd_text in jd_texts.items():
        jd_text = preprocess_text(jd_text)
        similarity = compare_texts(jd_text, provided_text)
        similarities.append((key, similarity))

    # Sort the similarities in descending order
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities

def document_list(request):
    all_documents = Document.objects.all()
    text_content_dict = {}
    
    # Populate the dictionary with primary key-text content pairs
    for document in all_documents:
        text_content_dict[document.pk] = document.text_content
    
    provided_text = """YJob Title: Senior Software QA Engineer

Job Description:
Cricut is seeking an experienced and versatile Senior Software QA Engineer who will be responsible for testing and qualifying Web, Mobile app, API and Hardware for product releases. You will be responsible for testing new hardware products & applications and communicating with development teams. You should be able to represent QA concerns in cross-functional team meetings and also provide valuable end-user feedback to improve the customer experience.
This position requires deep understanding of the software development life-cycle, experience with a variety of testing techniques, experience in running automation test suites and strong written and organizational skills. 

The successful candidate should be able to develop and execute an organized test plan to release high quality products to market on schedule.


Required Skills:

•	8+ years of experience in software testing.
•	Experience in testing user stories / features, API and doing regression testing.
•	Expert level knowledge and hands-on experience in creating test plans and writing test cases.
•	Hands on experience in executing automation test suites in Selenium or other automation tools and analyzing results.
•	Hands on experience with testing, analyzing and troubleshooting communication between front-end and API / Web Services.
•	Experience in analyzing logs and debugging using browser debugging tools.
•	Experience with testing web-based software.
•	Experience in testing IOS and Android applications.
•	Thorough understanding of QA methodology and best practices

Good to have skills:
•	Experience in leading QA teams is a plus
•	Experience in testing Software interacting with hardware
•	Experience in Testing and Qualifying Consumer Electronics Products

Qualification:
•	This position requires a Bachelor's degree in Engineering or equivalent.
•	8+ Years Product/Software testing 

"""  # Replace with your provided text

    # Calculate similarities
    similarities = compare_text_with_jd(provided_text, text_content_dict)
    #print(similarities)

    #return render(request, 'parse/document_list.html', {'documents': text_content_dict, 'similarities': similarities})
# Retrieve documents based on the primary keys in the similarity result
    similar_documents = []
    for pk, similarity_score in similarities:
        document = Document.objects.get(pk=pk)
        document.url = settings.MEDIA_URL + document.uploaded_file.name
        print(document.url)
        similar_documents.append(document)
    print(similar_documents,similarities)    

    combined_data = zip(similar_documents, similarities)
    
    return render(request, 'parse/document_list.html', {'combined_data': combined_data})






# def document_list(request):
   
#     #documents = Document.objects.all()
#     all_documents = Document.objects.all()
#     text_content_dict = {}
    
#     # Populate the dictionary with primary key-text content pairs
#     for document in all_documents:
#         text_content_dict[document.pk] = document.text_content
    
#     print(text_content_dict)    
#     return render(request, 'parse/document_list.html', {'documents': text_content_dict})













\

# def document_list(request):
#     # Query all Document objects and retrieve only the text_content field
#     text_contents = Document.objects.values_list('text_content', flat=True)
#     print(text_contents)
    
#     return render(request, 'parse/document_list.html', {'text_contents': text_contents})


