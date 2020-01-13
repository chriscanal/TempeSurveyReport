import os
import pandas as pd
from sqlalchemy import create_engine
from utils import get_clean_df
from sqlalchemy.orm import sessionmaker, relationship
from database import (
    Survey,
    Section,
    Question,
    PossibleResponse,
    Responder,
    Answer,
    base,
)
from question_data import sections, full_question_names, section_possible_answers
from sqlalchemy.ext.declarative import declarative_base

project_dir = os.environ["TEMPE_SURVEY_PROJECT_DIR"]
user = os.environ["TEMPE_SURVEY_DB_USER"]
password = os.environ["TEMPE_SURVEY_DB_PASS"]
host = os.environ["TEMPE_SURVEY_DB_HOST"]
port = os.environ["TEMPE_SURVEY_DB_PORT"]
dbname = os.environ["TEMPE_SURVEY_DB_NAME"]

survey_2016 = project_dir + "tempe_survey_data_2016.csv"
df16 = get_clean_df(survey_2016)

connection_string = "postgresql://%s:%s@%s:%s/%s" % (user, password, host, port, dbname)
# connection_string = "sqlite:///:memory:"


db = create_engine(connection_string, echo=True)

# psql "host=$TEMPE_SURVEY_DB_HOST port=$TEMPE_SURVEY_DB_PORT sslmode=verify-full sslrootcert=$AWS_CERT_PATH dbname=tempesurvey user=$TEMPE_SURVEY_DB_USER"


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

tempe_survey = Survey(
    id=1,
    survey_name="Tempe Employee Satisfaction Survey",
    company="City of Tempe",
    year=2016,
)
session.add(tempe_survey)

users = {_id: None for _id in df16.index}
section_responses_objects = {}
question_id_counter = 1
response_id_counter = 1
answer_id_counter = 1
for section_id, data in enumerate(sections.items()):
    section_responses_objects[section_id] = {}
    section, question_numbers = data
    section_obj = Section(id=section_id, section_name=section, survey=tempe_survey)
    session.add(section_obj)
    section_reponses = section_possible_answers[section]
    for numeric_value, text in section_reponses:
        possible_response_obj = PossibleResponse(
            id=response_id_counter,
            possible_response_text=text,
            possible_response_number=numeric_value,
            section=section_obj,
        )
        section_responses_objects[section_id][numeric_value] = possible_response_obj
        response_id_counter += 1
        session.add(possible_response_obj)
    for question_number in question_numbers:
        question_obj = Question(
            id=question_id_counter,
            question_survey_number=question_number,
            question_text=full_question_names[question_number],
            survey=tempe_survey,
            section=section_obj,
        )
        question_id_counter += 1
        session.add(question_obj)
        for user_id, user in users.items():
            if user is None:
                user = Responder(id=user_id)
                session.add(user)
                users[user_id] = user
            answer_value = df16.loc[user_id, question_number]
            response_chosen = section_responses_objects[section_id][answer_value]
            answer_obj = Answer(
                id=answer_id_counter,
                survey=tempe_survey,
                responder=user,
                question=question_obj,
                response=response_chosen,
            )
            session.add(answer_obj)
            answer_id_counter += 1
        print("ADDING ANSWERS FOR %s" % full_question_names[question_number])
        session.commit()
