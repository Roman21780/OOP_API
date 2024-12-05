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


# Примеры использования:
best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']
best_student.finished_courses += ['Java']

cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']

cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)
cool_mentor.rate_hw(best_student, 'Python', 10)

print(best_student.grades)

# Создание лекторов и экспертов
lecturer = Lecturer('Mark', 'Twin')
lecturer.courses_attached += ['Python']

reviewer = Reviewer('Jane', 'Smith')
reviewer.courses_attached += ['Python']

# Эксперт проверяет домашние задания
reviewer.check_homework(best_student, 'Python', 9)

print(best_student.grades)

# Студент выставляет оценку лектору
best_student.rate_lecturer(lecturer, 'Python', 10)
best_student.rate_lecturer(lecturer, 'Python', 8)

print(lecturer.grades)
print("---------------------------")

# Вывод информации о студентах, лекторах и рецензентах
print(best_student)
print("---------------------------")
print(lecturer)
print("---------------------------")
print(reviewer)
print("---------------------------")

# Примеры сравнения
other_student = Student('John', 'Doe', 'your_gender')
other_student.courses_in_progress += ['Python']
other_student.rate_lecturer(lecturer, 'Python', 9)

print(best_student < other_student)  # Сравнение студентов
print(lecturer < Lecturer('Alice', 'Wonderland'))  # Сравнение лекторов (в данном случае без оценок)