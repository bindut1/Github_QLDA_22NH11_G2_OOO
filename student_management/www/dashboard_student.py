import frappe

def get_context(context):
    """Fetch students and pass them to the template"""
    context.students = frappe.get_all(
        "Student",
        fields=["student_id", "student_name", "gender", "class_name"]
    )