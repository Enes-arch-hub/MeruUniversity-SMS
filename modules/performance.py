import heapq

class Performance:
    def __init__(self):
        self.heap = []

    def add_score(self, student, score):
        # Use negative score to simulate max heap
        heapq.heappush(self.heap, (-score, student))

    def get_top_student(self):
        if not self.heap:
            return "No data"

        score, student = heapq.heappop(self.heap)
        return {"student": student, "score": -score}

    def get_all_students(self):
        temp = self.heap.copy()
        result = []

        while temp:
            score, student = heapq.heappop(temp)
            result.append({"student": student, "score": -score})

        return result