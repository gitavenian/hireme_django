import os
import pickle
import numpy as np
from django.db.models import Q
import pandas as pd


# Define the directory where the pickle files are located
PICKLE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_pickle(file_name):
    with open(os.path.join(PICKLE_DIR, file_name), 'rb') as file:
        return pickle.load(file)

# Load the models
user_model = load_pickle('user_points.pkl')
label_encoder = load_pickle('label_encoder_user_points.pkl')
convenient_job_model = load_pickle('Convenient_job_model.pkl')
convenient_job_encoder = load_pickle('label_encoder.pkl')

def get_user_points(job_announcement, user):
    main_skill = job_announcement.main_skill
    soft_skill = job_announcement.soft_skill

    user_skills = user.skill_set.all()
    user_skill_names = [skill.skill_name for skill in user_skills]
    user_skill_experiences = {skill.skill_name: skill.experience for skill in user_skills}

    # Remove None values that could occur if no match is found
    user_skill_names = [skill for skill in user_skill_names if skill is not None]
    user_skill_experiences = {skill: exp for skill, exp in user_skill_experiences.items() if skill is not None}

    if not user_skills or main_skill is None or soft_skill is None:
        # User has no valid skills or job announcement skills are not valid
        return 0

    main_skill_experience = user_skill_experiences.get(main_skill, 0)

    feature_vector = []

    if main_skill in user_skill_names and soft_skill in user_skill_names:
        # Both main skill and soft skill match
        feature_vector = [
            main_skill,
            soft_skill,
            main_skill,
            soft_skill,
            int(main_skill_experience)
        ]
    elif main_skill in user_skill_names:
        # Only main skill matches
        highest_other_skill = max(user_skill_experiences.keys() - {main_skill}, key=user_skill_experiences.get, default=None)
        feature_vector = [
            main_skill,
            soft_skill,
            main_skill,
            highest_other_skill,
            int(main_skill_experience)
        ]
    elif soft_skill in user_skill_names:
        # Only soft skill matches
        highest_other_skill = max(user_skill_experiences.keys() - {soft_skill}, key=user_skill_experiences.get, default=None)
        feature_vector = [
            main_skill,
            soft_skill,
            highest_other_skill,
            soft_skill,
            0
        ]
    else:
        # Neither main skill nor soft skill match
        top_two_skills = sorted(user_skill_experiences, key=user_skill_experiences.get, reverse=True)[:2]
        if len(top_two_skills) < 2:
            top_two_skills = (top_two_skills + [None] * 2)[:2] 
        feature_vector = [
            main_skill,
            soft_skill,
            top_two_skills[0],
            top_two_skills[1],
            0
        ]

    feature_vector = [skill if skill is not None else 'none' for skill in feature_vector]

    # Encode categorical features using the same LabelEncoder
    encoded_features = []
    for feature in feature_vector:
        if isinstance(feature, str):
            try:
                encoded_feature = label_encoder.transform([feature])[0]
            except ValueError:
                encoded_feature = label_encoder.transform(['unknown'])[0]  # Replace with a known placeholder
        else:
            encoded_feature = feature
        encoded_features.append(encoded_feature)

    encoded_features = np.array(encoded_features).reshape(1, -1)
    user_point = user_model.predict(encoded_features)[0]

    return user_point



def check_job_suitability(job_announcement, user, skill):
    main_skill = job_announcement.main_skill
    job_experience = job_announcement.experience

    print(f"Evaluating skill: {skill.skill_name} with experience: {skill.experience}")

    # Generate the feature vector
    feature_vector = [
        skill.skill_name,
        skill.experience,
        main_skill,
        job_experience
    ]

    # Encode the feature vector
    encoded_features = []
    for feature in feature_vector:
        if isinstance(feature, str):
            try:
                # Assuming your encoder handles string to integer encoding
                encoded_feature = convenient_job_encoder.transform([feature])[0]
            except ValueError:
                encoded_feature = convenient_job_encoder.transform(['unknown'])[0]
        else:
            encoded_feature = feature
        encoded_features.append(encoded_feature)

    # Create DataFrame for model input
    encoded_features_df = pd.DataFrame([encoded_features], columns=['emp_skill', 'emp_exp', 'required_skill', 'required_exp'])
    print(f"Encoded Features DataFrame:\n{encoded_features_df}")

    # Predict job suitability using the model
    job_suitability = convenient_job_model.predict(encoded_features_df)[0]
    print(f"Job Suitability: {job_suitability}")

    return job_suitability
