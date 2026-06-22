from fastapi import FastAPI,Request,Form,Depends
from app.database import engine,get_db
from app import models
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse


from sqlalchemy.orm import Session
from datetime import datetime,date
from sqlalchemy import or_
from fastapi.staticfiles import StaticFiles
from app.database import SessionLocal
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()


#DATABAASE
models.Base.metadata.create_all(bind=engine)

#STATIC
app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

#TEMPLATE
templates = Jinja2Templates(directory="app/templates")


app.add_middleware(
    SessionMiddleware,
    secret_key="qualitywebs"
)
#admin 
@app.on_event("startup")
def create_admin():

    db = SessionLocal()

    admin = db.query(
        models.Employee
    ).filter(
        models.Employee.email ==
        "admin@gmail.com"
    ).first()

    if not admin:

        admin = models.Employee(

            name="Admin",

            email="admin@gmail.com",

            password="admin123",

            role="Admin"
        )

        db.add(admin)

        db.commit()

    db.close()   


#login
@app.get("/login")
def loogin_page(
    request : Request
):
    return templates.TemplateResponse(
        "login.html",
        {
        "request": request
        }

    )


@app.post("/login")
def login(
    request:Request,
    email: str = Form(...),
    password: str = Form(...),
    db:Session = Depends(get_db)
):
    user = db.query(
        models.Employee
    ).filter(
        models.Employee.email == email,
        models.Employee.password == password
    ).first()

    if not user:
        return{
            "error":"invalid credentials"
        }
    
    request.session["user_id"] = user.id

    request.session["role"] = user.role

    return RedirectResponse(
        "/",
        status_code=303
    )

#delete employee
@app.get("/employee/delete/{id}")
def delete_employee(

    id: int,

    db: Session = Depends(get_db)

):

    emp = db.query(
        models.Employee
    ).filter(
        models.Employee.id == id
    ).first()

    db.delete(emp)

    db.commit()

    return RedirectResponse(
        "/employees",
        status_code=303
    )


@app.get("/")
def home(
    request : Request,
    db : Session = Depends(get_db)
):
    total = db.query(models.Ticket).count()
    today_count = db.query(
        models.Ticket
        ).filter(
            models.Ticket.created_at >= date.today()
            ).count()

    open_count = db.query(
        models.Ticket
    ).filter(
        models.Ticket.status == "Open"
    ).count()

    progress = db.query(
        models.Ticket
    ).filter(
        models.Ticket.status == "In Progress"
    ).count()

    resolved = db.query(
        models.Ticket
    ).filter(
        models.Ticket.status == "Resolved"
    ).count()

    closed = db.query(
        models.Ticket
    ).filter(
        models.Ticket.status == "Closed"
    ).count()

    critical = db.query(
        models.Ticket
    ).filter(
        models.Ticket.priority == "Critical"
    ).count()

    latest = db.query(
        models.Ticket
    ).order_by(
        models.Ticket.id.desc()
    ).limit(5).all()

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "total": total,
            "open_count": open_count,
            "progress": progress,
            "resolved": resolved,
            "closed": closed,
            "critical": critical,
            "latest": latest,
            "today_count": today_count

        }
    )
#create ticket

def generate_ticket_number(db):

    count = db.query(
        models.Ticket
    ).count()

    return f"QW-TKT-{count+1:04d}"


@app.get("/create-ticket")
def create_ticket_page(
    request: Request,
    db: Session = Depends(get_db)
):

    employees = db.query(
        models.Employee
    ).filter(
        models.Employee.role == "Employee"
    ).all()

    return templates.TemplateResponse(
        "create_ticket.html",
        {
            "request": request,
            "employees": employees
        }
    )


@app.post("/create-ticket")
def create_ticket(
    request: Request,

    client_name: str = Form(...),
    mobile: str = Form(...),
    email: str = Form(""),
    company: str = Form(""),

    issue_title: str = Form(...),
    issue_description: str = Form(...),

    category: str = Form(...),
    priority: str = Form(...),

    assigned_to: str = Form(...),

    db: Session = Depends(get_db)
):
    existing = db.query(
    models.Ticket
    ).filter(
            models.Ticket.mobile == mobile,
 models.Ticket.issue_title == issue_title,
    models.Ticket.status != "Closed"
    ).first()
    

    if existing:
        return {
        "error":
        "Similar active ticket already exists for this client."
    }

    ticket = models.Ticket(

        ticket_number=generate_ticket_number(db),

        client_name=client_name,
        mobile=mobile,
        email=email,

        company=company,

        issue_title=issue_title,
        issue_description=issue_description,

        category=category,
        priority=priority,

        assigned_to=assigned_to,

        status="Open"
    )

    db.add(ticket)
    db.commit()

    return RedirectResponse(
        "/tickets",
        status_code=303
    )


#ticket List
@app.get("/tickets")
def ticket_list(
    request: Request,
    search: str = "",
    db: Session = Depends(get_db)
):

    query = db.query(models.Ticket)
    status = request.query_params.get("status")

    if search:

        query = query.filter(

            or_(

                models.Ticket.ticket_number.contains(search),

                models.Ticket.client_name.contains(search),

                models.Ticket.mobile.contains(search),

                models.Ticket.company.contains(search),

                models.Ticket.issue_title.contains(search)

            )

        )

    if status:
        query = query.filter(
        models.Ticket.status == status
    )



    tickets = query.all()

    return templates.TemplateResponse(
        "ticket_list.html",
        {
            "request": request,
            "tickets": tickets,
            "search": search,
            "status": status
        }
    )

#ADD REMARK
@app.post("/ticket/{ticket_id}/remark")
def add_remark(
    ticket_id: int,
    remark: str = Form(...),
    added_by: str = Form(...),
    db: Session = Depends(get_db)
):

    obj = models.TicketRemark(
        ticket_id=ticket_id,
        remark=remark,
        added_by=added_by
    )

    db.add(obj)
    db.commit()

    return RedirectResponse(
        f"/ticket/{ticket_id}",
        status_code=303
    )

#close ticket
@app.post("/ticket/{ticket_id}/close")
def close_ticket(
    ticket_id: int,

    closing_remark: str = Form(...),

    db: Session = Depends(get_db)
):

    ticket = db.query(
        models.Ticket
    ).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket.status != "Resolved":
        return {
            "error":
            "Ticket must be resolved before closing"
        }

    ticket.status = "Closed"

    ticket.closing_remark = closing_remark

    ticket.closed_at = datetime.now()

    db.commit()

    return RedirectResponse(
        "/tickets",
        status_code=303
    )


@app.get("/ticket/{ticket_id}")
def ticket_detail(
    ticket_id: int,
    request: Request,
    db: Session = Depends(get_db)
):

    ticket = db.query(
        models.Ticket
    ).filter(
        models.Ticket.id == ticket_id
    ).first()

    remarks = db.query(
        models.TicketRemark
    ).filter(
        models.TicketRemark.ticket_id == ticket_id
    ).all()

    history = db.query(
        models.TicketHistory
    ).filter(
        models.TicketHistory.ticket_id == ticket_id
    ).all()

    return templates.TemplateResponse(
        "ticket_detail.html",
        {
            "request": request,
            "ticket": ticket,
            "remarks": remarks,
            "history": history
        }
    )

#status update
@app.post("/ticket/{ticket_id}/status")
def update_status(

    ticket_id: int,

    new_status: str = Form(...),

    db: Session = Depends(get_db)

):
    

    ticket = db.query(
        models.Ticket
    ).filter(
        models.Ticket.id == ticket_id
    ).first()

    if ticket.status == "Closed":
        return {
         "error":
        "Closed ticket cannot be updated."
    }

    old_status = ticket.status

    ticket.status = new_status

    history = models.TicketHistory(
        ticket_id=ticket_id,
        old_status=old_status,
        new_status=new_status,
        changed_by="Admin"
    )

    db.add(history)

    db.commit()

    return RedirectResponse(
        f"/ticket/{ticket_id}",
        status_code=303
    )

#add employee
@app.get("/employees")
def employee_list(
    request: Request,
    db: Session = Depends(get_db)
):

    employees = db.query(
        models.Employee
    ).all()

    return templates.TemplateResponse(
        "employees.html",
        {
            "request": request,
            "employees": employees
        }
    )

@app.post("/employee/add")
def add_employee(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):

    employee = models.Employee(
        name=name,
        email=email,
        password=password,
        role="Employee"
    )

    db.add(employee)
    db.commit()

    return RedirectResponse(
        "/employees",
        status_code=303
    )