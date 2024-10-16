from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.repositories.db_model import School, Student, Admission, Payment, UserAccount
from utils.databse import get_db  

crud_router = APIRouter()


# CRUD Operations for Schools


# Create School
@crud_router.post("/schools/", response_model=School)
def create_school(school: School, db: Session = Depends(get_db)):
    db.add(school)
    db.commit()
    db.refresh(school)
    return school

# Read School
@crud_router.get("/schools/{school_id}", response_model=School)
def read_school(school_id: str, db: Session = Depends(get_db)):
    school = db.query(School).filter(School.id == school_id).first()
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school

# Update School
@crud_router.put("/schools/{school_id}", response_model=School)
def update_school(school_id: str, school: School, db: Session = Depends(get_db)):
    db_school = db.query(School).filter(School.id == school_id).first()
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")

    for key, value in school.dict().items():
        setattr(db_school, key, value)

    db.commit()
    db.refresh(db_school)
    return db_school

# Delete School
@crud_router.delete("/schools/{school_id}", status_code=204)
def delete_school(school_id: str, db: Session = Depends(get_db)):
    db_school = db.query(School).filter(School.id == school_id).first()
    if not db_school:
        raise HTTPException(status_code=404, detail="School not found")

    db.delete(db_school)
    db.commit()
    return None


# CRUD Operations for Students


# Create Student
@crud_router.post("/students/", response_model=Student)
def create_student(student: Student, db: Session = Depends(get_db)):
    db.add(student)
    db.commit()
    db.refresh(student)
    return student

# Read Student
@crud_router.get("/students/{student_id}", response_model=Student)
def read_student(student_id: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Update Student
@crud_router.put("/students/{student_id}", response_model=Student)
def update_student(student_id: str, student: Student, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    for key, value in student.dict().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student

# Delete Student
@crud_router.delete("/students/{student_id}", status_code=204)
def delete_student(student_id: str, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")

    db.delete(db_student)
    db.commit()
    return None


# CRUD Operations for Admissions


# Create Admission
@crud_router.post("/admissions/", response_model=Admission)
def create_admission(admission: Admission, db: Session = Depends(get_db)):
    db.add(admission)
    db.commit()
    db.refresh(admission)
    return admission

# Read Admission
@crud_router.get("/admissions/{admission_id}", response_model=Admission)
def read_admission(admission_id: str, db: Session = Depends(get_db)):
    admission = db.query(Admission).filter(Admission.id == admission_id).first()
    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    return admission

# Update Admission
@crud_router.put("/admissions/{admission_id}", response_model=Admission)
def update_admission(admission_id: str, admission: Admission, db: Session = Depends(get_db)):
    db_admission = db.query(Admission).filter(Admission.id == admission_id).first()
    if not db_admission:
        raise HTTPException(status_code=404, detail="Admission not found")

    for key, value in admission.dict().items():
        setattr(db_admission, key, value)

    db.commit()
    db.refresh(db_admission)
    return db_admission

# Delete Admission
@crud_router.delete("/admissions/{admission_id}", status_code=204)
def delete_admission(admission_id: str, db: Session = Depends(get_db)):
    db_admission = db.query(Admission).filter(Admission.id == admission_id).first()
    if not db_admission:
        raise HTTPException(status_code=404, detail="Admission not found")

    db.delete(db_admission)
    db.commit()
    return None


# CRUD Operations for Payments


# Create Payment
@crud_router.post("/payments/", response_model=Payment)
def create_payment(payment: Payment, db: Session = Depends(get_db)):
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

# Read Payment
@crud_router.get("/payments/{payment_id}", response_model=Payment)
def read_payment(payment_id: str, db: Session = Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# Update Payment
@crud_router.put("/payments/{payment_id}", response_model=Payment)
def update_payment(payment_id: str, payment: Payment, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    for key, value in payment.dict().items():
        setattr(db_payment, key, value)

    db.commit()
    db.refresh(db_payment)
    return db_payment

# Delete Payment
@crud_router.delete("/payments/{payment_id}", status_code=204)
def delete_payment(payment_id: str, db: Session = Depends(get_db)):
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")

    db.delete(db_payment)
    db.commit()
    return None


#CRUD Operations for User Accounts


# Create User Account
@crud_router.post("/user_accounts/", response_model=UserAccount)
def create_user_account(user_account: UserAccount, db: Session = Depends(get_db)):
    db.add(user_account)
    db.commit()
    db.refresh(user_account)
    return user_account

# Read User Account
@crud_router.get("/user_accounts/{user_id}", response_model=UserAccount)
def read_user_account(user_id: str, db: Session = Depends(get_db)):
    user_account = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not user_account:
        raise HTTPException(status_code=404, detail="User account not found")
    return user_account

# Update User Account
@crud_router.put("/user_accounts/{user_id}", response_model=UserAccount)
def update_user_account(user_id: str, user_account: UserAccount, db: Session = Depends(get_db)):
    db_user_account = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not db_user_account:
        raise HTTPException(status_code=404, detail="User account not found")

    for key, value in user_account.dict().items():
        setattr(db_user_account, key, value)

    db.commit()
    db.refresh(db_user_account)
    return db_user_account

# Delete User Account
@crud_router.delete("/user_accounts/{user_id}", status_code=204)
def delete_user_account(user_id: str, db: Session = Depends(get_db)):
    db_user_account = db.query(UserAccount).filter(UserAccount.id == user_id).first()
    if not db_user_account:
        raise HTTPException(status_code=404, detail="User account not found")

    db.delete(db_user_account)
    db.commit()
    return None
