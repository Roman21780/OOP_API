from itertools import count


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course].append(grade)
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка: Лектор не прикреплен к курсу или студент не записан на курс.'

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self.get_average_grade()}\n"
                f"Курсы в процессе изучения: {','.join(self.courses_in_progress)}\n"
                f"Завершенные курсы: {','.join(self.finished_courses)}")

    def get_average_grade(self):
        total_grades = sum(sum(grades) for grades in self.grades.values())
        count_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / count_grades if count_grades > 0 else 0

    def __lt__(self, other):
        if isinstance(other, Student):
            return self.get_average_grade() < other.get_average_grade()
        return NotImplemented


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

class Lecturer(Mentor): # Лекторы
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {self.get_average_grade()}")

    def get_average_grade(self):
        total_grades = sum(sum(grades) for grades in self.grades.values())
        count_grades = sum(len(grades) for grades in self.grades.values())
        return total_grades / count_grades if count_grades > 0 else 0

    def __lt__(self, other):
        if isinstance(other, Lecturer):
            return self.get_average_grade() < other.get_average_grade()
        return NotImplemented


class Reviewer(Mentor): # Эксперты, проверяющие домашние задания
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def check_homework(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}")


# Функции для подсчета средней оценки:
def average_grade(students, course):
    total = sum(student.get_average_grade() for student in students if course in student.grades)
    count = sum(1 for student in students if course in student.grades)
    return total / count if count > 0 else 0

def average_lecturer_grade(lecturers, course):
    total = sum(lecturer.get_average_grade() for lecturer in lecturers if course in lecturer.grades)
    count = sum(1 for lecturer in lecturers if course in lecturer.grades)
    return total / count if count > 0 else 0


# Создаем экземпляры классов:
student1 = Student("Roy", "Maccinly", "boy")
student1.courses_in_progress += ['Python', 'Java']
student1.finished_courses += ['DevOps']
student2 = Student("Rina", "Grey", "girl")
student2.courses_in_progress += ['Python', 'C++']
student2.finished_courses += ['Java']

lecturer1 = Lecturer('Mark', 'Twain')
lecturer1.courses_attached += ['Python']
lecturer2 = Lecturer('Alice', 'Wonder')
lecturer2.courses_attached += ['Python']

reviewer1 = Reviewer('Jane', 'Doe')
reviewer1.courses_attached += ['Python']
reviewer2 = Reviewer('John', 'Smith')
reviewer2.courses_attached += ['Python']


# Примеры использования:
# Эксперты проверяют домашние задания
reviewer1.check_homework(student1, 'Python', 9)
reviewer2.check_homework(student1, 'Python', 8)
reviewer1.check_homework(student2, 'Python', 9)

# Студенты выставляют оценки лекторам
student1.rate_lecturer(lecturer1, 'Python', 10)
student2.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer2, 'Python', 7)


# Вывод информации
print(student1)
print("---------------------------")
print(student2)
print("---------------------------")
print(lecturer1)
print("---------------------------")
print(lecturer2)
print("---------------------------")
print(reviewer1)
print("---------------------------")
print(reviewer2)
print("---------------------------")

# Подсчет средней оценки за домашние задания студентов по курсу 'Python'
print(f"Средняя оценка студентов по курсу 'Python': {average_grade([student1, student2], 'Python'):.2f}")

# Подсчет средней оценки за лекции лекторов по курсу 'Python'
print(f"Средняя оценка лекторов по курсу 'Python': {average_lecturer_grade([lecturer1, lecturer2], 'Python'):.2f}")