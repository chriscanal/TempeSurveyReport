import pandas as pd
from sqlalchemy import create_engine
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

survey_2016 = "/Users/chris/Code/tempe_survey_data_2016.csv"
df16 = pd.read_csv(survey_2016)

db = create_engine("sqlite:///:memory:", echo=False)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

# Create
tempe_survey = Survey(
    id=1,
    survey_name="Tempe Employee Satisfaction Survey",
    company="City of Tempe",
    year=2016,
)
session.add(tempe_survey)

question_id_counter = 1
response_id_counter = 1
for section_id, data in enumerate(sections.items()):
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
        response_id_counter += 1
        session.add(possible_response_obj)
    for question_number in question_numbers:
        question_obj = Question(
            id=question_id_counter,
            question_survey_number=question_number,
            question_text="FILL THIS IN",
            survey=tempe_survey,
            section=section_obj,
        )
        question_id_counter += 1
        session.add(question_obj)
session.commit()
#
# # Read
# surveys = session.query(Survey)
#
# # Update
# tempe_survey.survey_name = "Tempe,AZ Employee Satisfaction Survey"
# session.commit()
#
# # Delete
# session.delete(tempe_survey)
# session.commit()
