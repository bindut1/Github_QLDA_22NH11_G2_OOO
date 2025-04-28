import frappe
from frappe.model.document import Document

class Student(Document):
	pass

@frappe.whitelist()
def get_student_details(student_id):
    """
    Lấy thông tin chi tiết của sinh viên theo student_id
    """
    try:
        if not student_id:
            return {"error": "Mã sinh viên không được để trống"}
        
        student = frappe.get_doc("Student", {"student_id": student_id})
        return {
            "student_id": student.student_id,
            "student_name": student.student_name,
            "gender": student.gender,
            "class": student.class_name if hasattr(student, "class_name") else student.get("class", "")
        }
    except frappe.DoesNotExistError:
        return {"error": f"Không tìm thấy sinh viên với mã: {student_id}"}
    except Exception as e:
        frappe.log_error(f"Lỗi khi lấy thông tin sinh viên: {str(e)}")
        return {"error": f"Lỗi: {str(e)}"}

@frappe.whitelist()
def delete_student(student_id):
    """
    Xóa sinh viên từ cơ sở dữ liệu dựa trên student_id
    """
    try:
        frappe.db.delete("Student", {"student_id": student_id})
        frappe.db.commit()
        return {"message": "Xóa sinh viên thành công", "success": True}
    except Exception as e:
        frappe.db.rollback()
        return {"message": f"Lỗi khi xóa sinh viên: {str(e)}", "success": False}