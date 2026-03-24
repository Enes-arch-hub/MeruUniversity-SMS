class StudentRegistry:
    def __init__(self):
        self.students = {}  # Hash Table

    def add_student(self, student_id, name):
        self.students[student_id] = name

    def get_student(self, student_id):
        return self.students.get(student_id, "Not Found")

    def remove_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]