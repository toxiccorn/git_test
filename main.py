import csv
import os
import vars

from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from Student import Student

# Поиск и выбор файла
file_list = []
for file in os.listdir():
    if file.endswith('.csv'):
        file_list.append(file)

for index, file in enumerate(file_list):
    print(str(index) + ' ' + file)

user_file_pick = int(input('выберите номер файла'))
filename = file_list[user_file_pick]

temp_file = 'temp_' + filename
encode = 'utf-8'

# Ищем тест и его параметры
for index, subject in enumerate(vars.subjects):
    print(str(index) + ' ' + subject['name'])
subject_index = int(input('выберете предмет'))
subject = vars.subjects[subject_index]

subject_name = subject['name']
min_score = subject['min_score']
question_complete_mark = subject['question_complete_mark']
a_scores_table = subject['custom_a_table']
b_scores_table = subject['custom_b_table']
a_start = subject['a_questions_start_col']
a_end = subject['a_questions_end_col']
b_start = subject['b_questions_start_col']
b_end = subject['b_questions_end_col']
test_date_col = subject['test_date_col']
b_questions = len(subject['custom_b_table'].items()) - 1

date_user_string = input('Введите дату экзамена в формате dd.mm.yyyy')

# Перевариваем дату для поиска по таблице
date_splited_strings = date_user_string.split('.')
test_day = date_splited_strings[0]
test_day_int = int(test_day)
test_month = date_splited_strings[1]
test_month_search_string = vars.months[int(test_month) - 1]
test_year = date_splited_strings[2]
search_date_string = str(test_day_int) + ' ' + test_month_search_string + ' ' + test_year

# Открывает файл и чичстит его от лишних кавычек
with open(filename, encoding=encode) as file:
    data = file.readlines()
    del data[-1]
    for line in data:
        line.replace('"', '')

# Пишет во временный файл читаемые данные
with open(temp_file, 'w', encoding=encode) as tfile:
    for line in data:
        tfile.write(line)

# Открывает временный файл
with open(temp_file, 'r', encoding=encode) as tfile:
    students = []
    csvdata = csv.reader(tfile)
    header_row = next(csvdata)

    # Cчитывает данные о необходимых студентах
    for row in csvdata:
        if search_date_string in row[test_date_col]:
            current_student = Student(row[0] + ' ' + row[1], row[9])

            for a_list in range(a_start, a_end + 1):
                current_student.a_marks.append(row[a_list])
            for b_list in range(b_start, b_end + 1):
                current_student.b_marks.append(row[b_list])

            current_student.clear_marks()
            current_student.calculate_primary_score(question_complete_mark)
            current_student.calculate_secondary_score(a_scores_table, b_scores_table)

            if current_student.sum_secondary_score < min_score:
                result = current_student.autoscore(min_score, b_questions, question_complete_mark, a_scores_table,
                                                   b_scores_table)
                if result == 'success':
                    print(current_student.full_name + ' autocorrected ' + str(current_student.autocorrect_attemps) +
                          ' times')
                else:
                    print(current_student.full_name + ' is dibil')

            students.append(current_student)

# Вывод информации в консоль
for student in students:
    print(student.full_name + ' - ' + str(student.sum_secondary_score))

# Удаляет временный файл
os.remove(temp_file)

# Создаем файл ведомости
document = Document()
section = document.sections[0]
section.top_margin = Cm(2)
section.bottom_margin = Cm(2)
section.left_margin = Cm(3)
section.right_margin = Cm(1)

doc_rsreu_head = document.add_paragraph()
doc_rsreu_head.add_run("ФГБОУ ВО «Рязанский государственный радиотехнический университет им. В.Ф. Уткина»").bold = True
paragraph_format = doc_rsreu_head.paragraph_format
paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

doc_name = document.add_paragraph()
doc_name.add_run('Экзаменационная ведомость').bold = True
paragraph_format = doc_name.paragraph_format
paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

doc_exam_name = document.add_paragraph()
paragraph_format = doc_exam_name.paragraph_format
paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
doc_exam_name.add_run(subject_name.title()).bold = True

doc_exam_date = document.add_paragraph()
doc_exam_date.add_run(date_user_string).bold = True
doc_exam_date.add_run('Дата: ').bold = True
paragraph_format = doc_exam_date.paragraph_format
paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

table = document.add_table(rows=len(students), cols=3)
document.save('demo.docx')
