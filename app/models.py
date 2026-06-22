from sqlalchemy import*
from app.database import Base
from datetime import datetime

class Ticket(Base):
    __tablename__ = "ticket"

    id = Column(Integer,primary_key=True,index=True)
    ticket_number = Column(String,unique=True)
    client_name = Column(String,unique=True)
    mobile = Column(String)
    email = Column(String)

    company = Column(String)
    issue_title = Column(String)
    issue_description = Column(Text)

    category = Column(String)
    priority = Column(String)

    assigned_to = Column(String)
    status = Column(
        String,
        default="Open"
    )

    created_at = Column(
        DateTime,
        default=datetime.now
    )

    updated_at = Column(
        DateTime,
        default=datetime.now
    )

    resolved_at = Column(DateTime, nullable=True)

    closed_at = Column(DateTime, nullable=True)

    closing_remark = Column(
        Text,
        nullable=True
    )

#ticket remark
class TicketRemark(Base):
    __tablename__ = "ticket_remarks"

    id = Column(Integer, primary_key=True)

    ticket_id = Column(Integer)

    remark = Column(Text)

    added_by = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.now
    )


#ticket history
class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id = Column(Integer, primary_key=True)

    ticket_id = Column(Integer)

    old_status = Column(String)

    new_status = Column(String)

    changed_by = Column(String)

    changed_at = Column(
        DateTime,
        default=datetime.now
    )


#employee 
class Employee(Base):

    __tablename__ = "employees"

    id = Column(Integer,
                primary_key=True)

    name = Column(String)

    email = Column(
        String,
        unique = True
    )    

    password = Column(String)

    role = Column(String)

