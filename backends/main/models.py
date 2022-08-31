from django.db import models


class User(models.Model):
    name = models.CharField(max_length=150, null=True, unique=True)
    username = models.CharField(max_length=150, null=True)


class Poll_type(models.Model):
    type = models.CharField(max_length=250, verbose_name='Предмет',unique=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = '1 Предметы'


class Poll_class(models.Model):
    type = models.ForeignKey(Poll_type, on_delete=models.CASCADE, related_name='course')
    name = models.IntegerField(verbose_name='Номер сборника')

    def __str__(self):
        return f'{self.type} | {self.name}'

    class Meta:
        verbose_name = 'Сборник вопроса'
        verbose_name_plural = '2 Сборники вопросов'


class Poll(models.Model):
    poll_type = ((True, 'Анонимный'),
                 (False, 'Публичный')
                 )
    question_type = (('quiz', 'Викторина'),
                     ('regular', 'Опрос')
                     )
    name = models.ForeignKey(Poll_class, on_delete=models.CASCADE, related_name='nam', verbose_name='Сборник')
    question = models.TextField(verbose_name='Вопрос')
    is_anonymous = models.BooleanField(default=False, choices=poll_type, verbose_name="Анонимный или публоичный")
    type = models.CharField(max_length=150, choices=question_type, verbose_name='Тип вопроса', default='Викторина')
    explanation = models.TextField(verbose_name='Подсказка после завершения теста')
    open_period = models.IntegerField(default=30, verbose_name='Время завершения теста',
                                      help_text='0 если не имеет ограничения во времени')
    answer = models.TextField(verbose_name='Варианты ответа')
    img = models.FileField(upload_to='File/Image/', verbose_name='Фотография', null=True, blank=True)
    video_gif = models.FileField(upload_to='File/Video_Gif/', verbose_name="Видео или Гиф", null=True, blank=True)

    def __str__(self):
        return f'{self.question} | {self.name}'

    class Meta:
        verbose_name = 'Вопрос сборнику'
        verbose_name_plural = '3 Вопросы сборников'


class Poll_answer(models.Model):
    question = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='quest', verbose_name='Вопрос')
    options = models.CharField(max_length=250, verbose_name='Вариант ответа (F1,F2)')
    correct_option = models.BooleanField(default=False, verbose_name='Тип ответа',
                                         help_text='True - правильный\n\nFalse - неправильный')

    def __str__(self):
        return f'{self.options} | {self.question}'

    class Meta:
        verbose_name = 'Вариант Ответа'
        verbose_name_plural = '4 Варианты Ответов'


class User_answer(models.Model):
    tg_id = models.BigIntegerField()
    true_option = models.IntegerField()
    name = models.CharField(max_length=250, null=True)
    poll_id = models.CharField(max_length=250, null=True)
    answer = models.CharField(max_length=250, null=True)
    point = models.IntegerField()
    chat_id = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Ответ Юзера'
        verbose_name_plural = 'Ответы Юзеров'


class Group(models.Model):
    group_id = models.BigIntegerField()
    name = models.CharField(max_length=250)

    class Meta:
        verbose_name = 'Группу'
        verbose_name_plural = 'Группы'
