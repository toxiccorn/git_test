class Student:

    def __init__(self, full_name, score):
        self.full_name = full_name
        self.score = score
        self.a_marks = []
        self.b_marks = []
        self.a_marks_right = 0          # Правильные ответы в части А
        self.b_marks_right = 0          # Правильные ответы в части Б
        self.a_partial = 0              # Частичные ответы в части А
        self.b_partial = 0              # Частичные ответы в части Б
        self.a_partial_score = 0        # Суммарный бал частичных ответов A
        self.b_partial_score = 0        # Суммарный бал частичных ответов Б
        self.a_partial_sum = 0          # Первичный балл суммы частичных ответов А
        self.b_partial_sum = 0          # Первичный балл суммы частичных ответов Б
        self.a_secondary_score = 0      # Общий балл части А (с учётом частично-правильных ответов)
        self.b_secondary_score = 0      # Общий балл части Б (с учётом частично-правильных ответов)
        self.sum_secondary_score = 0    # Общий балл за тест
        self.autocorrect_attemps = 0

    # Чистит оценки от минусов и форматирует их во float
    def clear_marks(self):
        for index, mark in enumerate(self.a_marks):
            if mark == '-':
                self.a_marks[index] = 0.0
            else:
                self.a_marks[index] = float(self.a_marks[index].replace(',', '.'))

        for index, mark in enumerate(self.b_marks):
            if mark == '-':
                self.b_marks[index] = 0.0
            else:
                self.b_marks[index] = float(self.b_marks[index].replace(',', '.'))

    # Рассчитывает количество правильных ответов по частям
    def calculate_primary_score(self, current_mark_complete):
        for a_mark in self.a_marks:
            if a_mark == current_mark_complete:
                self.a_marks_right += 1
            elif a_mark != 0 and a_mark < current_mark_complete:
                self.a_partial += 1
                self.a_partial_score += a_mark

        self.a_partial_sum = int(self.a_partial_score/current_mark_complete)
        self.a_marks_right += self.a_partial_sum

        for b_mark in self.b_marks:
            if b_mark == current_mark_complete:
                self.b_marks_right += 1
            elif b_mark != 0 and b_mark < current_mark_complete:
                self.b_partial += 1
                self.b_partial_score += b_mark

        self.b_partial_sum = int(self.b_partial_score / current_mark_complete)
        self.b_marks_right += self.b_partial_sum

    def calculate_secondary_score(self, a_table, b_table):
        for a_marks_right, a_score in a_table.items():
            if self.a_marks_right == a_marks_right:
                self.a_secondary_score = a_score
                break

        for b_marks_right, b_score in b_table.items():
            if self.b_marks_right == b_marks_right:
                self.b_secondary_score = b_score
                break

        self.sum_secondary_score = self.a_secondary_score + self.b_secondary_score

    def autoscore(self, min_score, attempts_number, question_complete_mark, a_scores_table, b_scores_table):
        success_flag = False

        # Для отката
        hold_a_marks_right = self.a_marks_right
        hold_b_marks_right = self.b_marks_right

        # Попытка увеличить балл за счёт части А
        while self.autocorrect_attemps <= attempts_number:
            if self.a_marks_right - 1 >= 0:
                self.autocorrect_attemps += 1
                self.a_marks_right -= 1
                self.b_marks_right += 1
                self.calculate_secondary_score(a_scores_table, b_scores_table)
                if self.sum_secondary_score >= min_score:
                    success_flag = True
                    return 'success'
            else:
                break

        # Проверка на успех и откат изменений
        if success_flag is False:
            self.a_marks_right = hold_a_marks_right
            self.b_marks_right = hold_b_marks_right

        # Попытка увеличить балл за счёт части Б
        self.autocorrect_attemps = 0
        while self.autocorrect_attemps <= attempts_number:
            if self.b_marks_right - 1 >= 0:
                self.autocorrect_attemps += 1
                self.a_marks_right += 1
                self.b_marks_right -= 1
                self.calculate_secondary_score(a_scores_table, b_scores_table)
                if self.sum_secondary_score >= min_score:
                    success_flag = True
                    return 'success'
            else:
                break

        # Проверка на успех и откат изменений
        if success_flag is False:
            self.a_marks_right = hold_a_marks_right
            self.b_marks_right = hold_b_marks_right
            return 'dibil'
