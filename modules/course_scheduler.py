from collections import deque

class CourseScheduler:
    def __init__(self):
        self.courses = {}  # course_name → {capacity, queue, enrolled}

    def add_course(self, course_name, capacity):
        self.courses[course_name] = {
            "capacity": capacity,
            "queue": deque(),
            "enrolled": []
        }

    def register_student(self, course_name, student):
        if course_name not in self.courses:
            return "Course not found"

        self.courses[course_name]["queue"].append(student)
        return "Student added to queue"

    def allocate(self, course_name):
        if course_name not in self.courses:
            return "Course not found"

        course = self.courses[course_name]

        while course["queue"] and len(course["enrolled"]) < course["capacity"]:
            student = course["queue"].popleft()
            course["enrolled"].append(student)

        return course["enrolled"]

    def get_course(self, course_name):
        return self.courses.get(course_name, "Course not found")