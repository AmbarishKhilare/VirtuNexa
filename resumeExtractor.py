import os
import pdfplumber
import spacy
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


nltk.download("stopwords")


nlp = spacy.load("en_core_web_sm")


SKILLS = {"python", "java", "c++", "sql", "machine learning", "deep learning", "nlp", 
          "data analysis", "tensorflow", "pytorch", "html", "css", "javascript"}

def extract_text_from_pdf(pdf_path):
    
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def clean_text(text):
    stop_words = set(stopwords.words("english"))
    doc = nlp(text.lower())  # Convert to lowercase
    cleaned_tokens = [token.lemma_ for token in doc if token.text not in stop_words and token.is_alpha]
    return " ".join(cleaned_tokens)

def extract_skills(text):
    extracted_skills = set()
    for token in nlp(text):
        if token.text in SKILLS:
            extracted_skills.add(token.text)
    return extracted_skills

def compute_similarity(resume_text, job_desc):
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc])
    similarity_score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    return similarity_score[0][0]

def main():
    resume_path = input("Enter the path to the resume (PDF): ").strip()
    
    if not os.path.exists(resume_path):
        print("File not found. Please enter a valid path.")
        return

    job_desc = input("Enter the job description: ").strip()
    
    
    resume_text = extract_text_from_pdf(resume_path)
    cleaned_resume_text = clean_text(resume_text)
    
    
    extracted_skills = extract_skills(cleaned_resume_text)
    print("\nExtracted Skills:", extracted_skills)

    
    similarity_score = compute_similarity(cleaned_resume_text, job_desc)
    print(f"\nResume-Job Match Score: {similarity_score:.2f}")

if __name__ == "__main__":
    main()
