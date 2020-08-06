import math


class Matrix:

    def __init__(self, array):
        self.array = array

    @staticmethod  # Turn method into one that is independent of the class
    def array(ar):
        return Matrix(ar)

    @staticmethod
    def add(vec1, vec2):
        assert (len(vec1) == len(vec2)) and (len(vec1[0]) == len(vec2[0]))
        if len(vec1) >= 1 and type(vec1[0]) is list:
            for row in range(len(vec1)):
                for col in range(len(vec1[0])):
                    vec1[row][col] += vec2[row][col]
        else:
            for i in range(len(vec1)):
                vec1[i] += vec2[i]
        return Matrix(vec1)

    @staticmethod
    def matmul(A, B):
        assert len(A[0]) == len(B)
        n = len(A)
        p = len(B[0])
        m = len(B)
        result = []
        for i in range(n):
            result.append([])
            for j in range(p):
                result[i].append(0)
        for i1 in range(n):
            for i2 in range(p):
                for i3 in range(m):
                    result[i1][i2] += A[i1][i3] * B[i3][i2]
        result = Matrix(result)
        if result.shape == (1, 1):
            return result[0][0]
        else:
            return result

    @staticmethod
    def subtract(vec1, vec2):
        assert (len(vec1) == len(vec2)) and (len(vec1[0]) == len(vec2[0]))
        if len(vec1) >= 1 and type(vec1[0]) is list:
            for row in range(len(vec1)):
                for col in range(len(vec1[0])):
                    vec1[row][col] -= vec2[row][col]
        else:
            for i in range(len(vec1)):
                vec1[i] -= vec2[i]
        return Matrix(vec1)

    @staticmethod
    def special(row, col):
        mat = []
        for r in range(row):
            mat.append([])
            for c in range(col):
                mat[r].append(1)
        return Matrix(mat)

    def tolist(self):
        lst = []
        for i in range(self.shape[1]):
            for j in range(self.shape[0]):
                lst.append(self.array[j][i])
        return lst

    @property
    def T(self):
        new = []
        for i in range(self.shape[1]):
            new.append([])
            for j in range(self.shape[0]):
                new[i].append(self.array[j][i])
        return Matrix(new)

    @property  # Turn method into an attribute
    def shape(self):
        if type(self.array[0]) is not int or float:
            return len(self.array), len(self.array[0])
        else:
            return len(self.array), 1

    def __add__(self, obj):
        return self.add(self.array, obj.array)

    def __sub__(self, obj):
        return self.subtract(self.array, obj.array)

    def __mul__(self, obj):
        return self.matmul(self.array, obj.array)

    def __str__(self):
        strng = ''
        for r in range(self.shape[0]):
            strng += str(self.array[r]) + '\n'
        return strng

    def __getitem__(self, r):
        return self.array[r]

