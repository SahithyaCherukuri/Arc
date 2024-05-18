from . import data_types

# TODO: Add offsets and data option


class dia_matrix:

    def __init__(self, size, shape=None, dtype=None, other=None):
        self.size = size
        self.shape = shape
        self.dtype = dtype
        self.other = other

        if shape is None:
            shape = size
        else:
            if dtype is not None:
                # speed up with creation
                self.matrix = [[0] * shape] * size
            else:
                self.matrix = [[0] * shape for _ in range(size)]

    def __call__(self):
        return self

    def __str__(self):

        if self.dtype is not None:
            dtype_str = self.dtype.__name__
            matrix_str = "\n".join(
                ["[" + ", ".join(map(str, row)) + "]" for row in self.matrix])
            matrix_str = matrix_str + ", dtype=" + dtype_str
        else:
            matrix_str = "\n".join(
                ["[" + ", ".join(map(str, row)) + "]" for row in self.matrix])

        return matrix_str

    def __getitem__(self, index):
        if isinstance(index, tuple):
            row, col = index
            if isinstance(row, int) and isinstance(col, slice):
                if row < 0 and row >= self.size:
                    raise IndexError("Index out of bounds")
            return self.matrix[row][col]
        raise IndexError("Unsupported index type")

    def __repr__(self):
        if self.matrix is None:
            return "None"
        return str(self)

    def set_element(self, row, col, value):

        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            raise ValueError("Index out of range")
            # support left to right and right to left
        if row == col or row + col == self.size - 1:
            self.matrix[row][col] = value
        else:
            raise ValueError("Can only set elements on diagonal")

    def get_shape(self):
        return self.shape

    def get_size(self):
        return self.size

    def multiply(self, other):

        if self.size != other.size:
            raise ValueError(
                "Matrices must be of the same size for multiplication")

        if self.size != other.shape:
            raise ValueError(
                "Number of columns in the first matrix does not equal to the number of rows in the second matrix")

        result = dia_matrix(self.size)
        result.matrix = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                for k in range(self.size):
                    result.matrix[i][j] += self.matrix[i][k] * \
                        other.matrix[k][j]
        return result

    def add(self, other):

        if self.size != other.size:
            raise ValueError(
                "Matrices must be of the same size for addition")

        if self.size != other.shape:
            raise ValueError(
                "Number of columns in the first matrix does not equal to the number of rows in the second matrix")

        result = dia_matrix(self.size)
        result.matrix = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                result.matrix[i][j] = self.matrix[i][j] + \
                    other.matrix[i][j]
        return result

    def subtract(self, other):

        if self.size != other.size:
            raise ValueError(
                "Matrices must be of the same size for subtraction")

        for i in range(self.size):
            if self.matrix[i][i] < 0 or other.matrix[i][i] < 0:
                raise ValueError(
                    "Positive definite matrix cannot have negative diagonal elements")

        result = dia_matrix(self.size)
        result.matrix = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                result.matrix[i][j] = self.matrix[i][j] - other.matrix[i][j]
        return result

    # TODO: Needs more work
    def divide(self, other):

        if self.size != other.size:
            raise ValueError(
                "Matrices must be of the same size for division")

        if self.size != other.shape:
            raise ValueError(
                "Number of columns in the first matrix does not equal to the number of rows in the second matrix")

        result = dia_matrix(self.size)
        result.matrix = [[0] * self.size for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if other.matrix[i][j] == 0:
                    raise ValueError("Division by zeros encountered")
                result.matrix[i][j] = self.matrix[i][j] // other.matrix[i][j]
        return result

# TODO: Fix format

    def toarray(self):

        array = self.matrix[:]
        if self.dtype is not None:
            dtype_str = self.dtype.__name__
            return [row[:] for row in array], dtype_str
        else:
            return [row[:] for row in array]