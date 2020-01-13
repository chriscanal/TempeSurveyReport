from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

base = declarative_base()


class Survey(base):
    __tablename__ = "surveys"
    id = Column(Integer, primary_key=True, unique=True)
    survey_name = Column(String(255))
    company = Column(String(255))
    year = Column(Integer)
    questions = relationship("Question", backref="survey")
    sections = relationship("Section", backref="survey")
    answers = relationship("Answer", backref="survey")


class Section(base):
    __tablename__ = "sections"
    id = Column(Integer, primary_key=True, unique=True)
    section_name = Column(String(255))
    survey_id = Column(Integer, ForeignKey("surveys.id"), primary_key=True)
    questions = relationship("Question", backref="section")
    possible_responses = relationship("PossibleResponse", backref="section")


class Question(base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, unique=True)
    question_survey_number = Column(String(255))
    question_text = Column(String(255))
    survey_id = Column(Integer, ForeignKey("surveys.id"), primary_key=True)
    section_id = Column(Integer, ForeignKey("sections.id"), primary_key=True)
    answers = relationship("Answer", backref="question")


class PossibleResponse(base):
    __tablename__ = "possible_responses"
    id = Column(Integer, primary_key=True, unique=True)
    possible_response_text = Column(String(255))
    possible_response_number = Column(Integer)
    section_id = Column(Integer, ForeignKey("sections.id"), primary_key=True)
    answers = relationship("Answer", backref="response")


class Responder(base):
    __tablename__ = "responders"
    id = Column(Integer, primary_key=True, unique=True)
    answers = relationship("Answer", backref="responder")


class Answer(base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, unique=True)
    survey_id = Column(Integer, ForeignKey("surveys.id"), primary_key=True)
    responder_id = Column(Integer, ForeignKey("responders.id"), primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"), primary_key=True)
    chosen_response_id = Column(
        Integer, ForeignKey("possible_responses.id"), primary_key=True
    )


if __name__ == "__main__":
    db = create_engine("sqlite:///:memory:", echo=True)
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
    session.commit()

    # Read
    surveys = session.query(Survey)
    print(surveys)

    # Update
    tempe_survey.survey_name = "Tempe,AZ Employee Satisfaction Survey"
    session.commit()

    # Delete
    session.delete(tempe_survey)
    session.commit()
