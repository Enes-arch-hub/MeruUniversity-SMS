class FeeNode:
    def __init__(self, student, amount):
        self.student = student
        self.amount = amount
        self.left = None
        self.right = None


class FeeBST:
    def __init__(self):
        self.root = None

    def insert(self, root, student, amount):
        if root is None:
            return FeeNode(student, amount)

        if amount < root.amount:
            root.left = self.insert(root.left, student, amount)
        else:
            root.right = self.insert(root.right, student, amount)

        return root

    def add_payment(self, student, amount):
        self.root = self.insert(self.root, student, amount)

    def inorder(self, root, result):
        if root:
            self.inorder(root.left, result)
            result.append({"student": root.student, "amount": root.amount})
            self.inorder(root.right, result)

    def get_all_payments(self):
        result = []
        self.inorder(self.root, result)
        return result