class Rectangle:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    def get_area(self):
        return self.height * self.width

    def get_perimeter(self):
        return self.height * 2 + self.width * 2

    def get_diagonal(self):
        return (self.height**2 + self.width**2) ** 0.5

    def get_picture(self):
        if self.height > 50 or self.width > 50:
            return "Too big for picture."
        picture = ""
        for i in range(self.height):
            picture += "*" * self.width + "\n"
        return picture

    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

    def get_amount_inside(self, shape):
        tmp_height = self.height
        tmp_width = self.width
        count = 0
        while True:
            if tmp_height >= shape.height:
                if tmp_width >= shape.width:
                    count += 1
                    tmp_width -= shape.width
                else:
                    tmp_height -= shape.height
                    tmp_width = self.width
            else:
                return count


class Square(Rectangle):
    def __init__(self, side) -> None:
        super().__init__(side, side)

    def set_side(self, side):
        self.width = side
        self.height = side

    def set_height(self, height):
        super().set_height(height)
        super().set_width(height)

    def set_width(self, height):
        super().set_height(height)
        super().set_width(height)

    def __str__(self) -> str:
        return f"Square(side={self.width})"


r = Rectangle(4, 8)
s = Rectangle(4, 4)
print(r.get_picture())
print(s.get_picture())
print(r.get_amount_inside(s))
