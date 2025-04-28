import frappe
from frappe.model.document import Document

class Student(Document):
    pass

@frappe.whitelist()
def get_students():
    """API to fetch all students"""
    return frappe.get_all("Student", fields=["student_id", "student_name", "gender", "class_name"])

@frappe.whitelist()
def get_student(student_id):
    """API to fetch details of a specific student by student_id"""
    student = frappe.get_all("Student", filters={"student_id": student_id}, fields=["student_id", "student_name", "gender", "class_name"])
    if student:
        return {"message": student[0]}  # Return the first matching student
    else:
        return {"error": "Student not found"}

@frappe.whitelist()
def update_student(student_id, student_name=None, gender=None, class_name=None):
    """API to update an existing student"""
    doc = frappe.get_doc("Student", student_id)
    if student_name:
        doc.student_name = student_name
    if gender:
        doc.gender = gender
    if class_name:
        doc.class_name = class_name
    doc.save()
    return {"message": "Student updated successfully"}

@frappe.whitelist()
def add_student(student_id, student_name, gender, class_name):
    """API to add a new student"""
    doc = frappe.get_doc({
        "doctype": "Student",
        "student_id": student_id,
        "student_name": student_name,
        "gender": gender,
        "class_name": class_name
    })
    doc.insert()
    frappe.db.commit()
    return {"message": "Student added successfully"}