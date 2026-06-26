from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match_score(candidate_skills, job_description):

    if not candidate_skills:
        return 0

    candidate_text = " ".join(candidate_skills)

    documents = [
        candidate_text,
        job_description
    ]

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    score = round(similarity * 100)

    if score > 100:
        score = 100

    return score