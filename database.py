from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///:memory:", echo=False)
base = declarative_base()


class QuestionSurveyJoint(base):
    __tablename__ = "question_surveys"
    survey_id = Column(Integer, ForeignKey("surveys.survey_id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.question_id"), primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.section_id"), primary_key=True)


class SectionPossibleResponseJoint(base):
    __tablename__ = "section_possible_response"
    survey_id = Column(Integer, ForeignKey("surveys.survey_id"), primary_key=True)
    question_id = Column(
        Integer, ForeignKey("possible_responses.possible_response_id"), primary_key=True
    )


class AnswersJoint(base):
    __tablename__ = "answers"
    survey_id = Column(Integer, ForeignKey("surveys.survey_id"), primary_key=True)
    responder_id = Column(
        Integer, ForeignKey("responder_id.responder_id"), primary_key=True
    )
    question_id = Column(Integer, ForeignKey("questions.question_id"), primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.section_id"), primary_key=True)
    possible_response_id = Column(
        Integer, ForeignKey("possible_responses.possible_response_id"), primary_key=True
    )


class Survey(base):
    __tablename__ = "surveys"
    survey_id = Column(Integer, primary_key=True)
    survey_name = Column(String)
    company = Column(String)
    year = Column(Integer)


class Question(base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True)
    question_survey_number = Column(String)
    question_text = Column(String)


class Section(base):
    __tablename__ = "sections"
    section_id = Column(Integer, primary_key=True)
    section_name = Column(String)


class PossibleResponse(base):
    __tablename__ = "possible_responses"
    possible_response_id = Column(Integer, primary_key=True)
    possible_response_text = Column(String)
    possible_response_number = Column(Integer)


class Responder(base):
    __tablename__ = "responders"
    responder_id = Column(Integer, primary_key=True)


if __name__ == "__main__":
    Session = sessionmaker(db)
    session = Session()

    base.metadata.create_all(db)

    # Create
    tempe_survey = Survey(
        survey_id=1,
        survey_name="Tempe Employee Satisfaction Survey",
        company="City of Tempe",
        year=2016,
    )
    session.add(tempe_survey)
    session.commit()

    # Read
    surveys = session.query(Survey)
    for s in surveys:
        print(s.survey_name)

    # Update
    tempe_survey.survey_name = "Tempe,AZ Employee Satisfaction Survey"
    session.commit()

    # Delete
    session.delete(tempe_survey)
    session.commit()
