# External Modules
import spacy
import re
# Project Modules
import constants

# Load spaCy's English language model
nlp = spacy.load("pt_core_news_lg")

# Define lists of possible goals and interests
goals_list = constants.GOALS_OPTIONS
interests_list = constants.INTERESTS_OPTIONS

# Define a function to extract structured information from user_json
def extract_structured_info(user_json):
    print(user_json)
    structured_info = {}

    # Use spaCy to process the user_json text
    doc = nlp(user_json["name"] + " " + str(user_json["goals"]) + " " + str(user_json["interests"]) + " " + user_json["budget"])

    # Extract name
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            structured_info["name"] = ent.text.capitalize()
            break
        else:
            structured_info["name"] = user_json["name"].capitalize()

    # Extract goals
    extracted_goals = []
    for token in doc:
        if any(goal.lower() in token.text.lower() for goal in goals_list):
            extracted_goals.append(token.text.capitalize())

    if extracted_goals:
        structured_info["goals"] = extracted_goals

    # Extract interests
    extracted_interests = []
    for token in doc:
        if any(interest.lower() in token.text.lower() for interest in interests_list):
            extracted_interests.append(token.text.capitalize())

    if extracted_interests:
        structured_info["interests"] = extracted_interests

    # Extract budget
    budget_match = re.search(r"\d+", doc.text)
    if budget_match:
        structured_info["budget"] = int(budget_match.group(0))

    print(structured_info)
    return structured_info