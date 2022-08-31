# Generated by Django 4.0.4 on 2022-08-29 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_id', models.BigIntegerField()),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Группу',
                'verbose_name_plural': 'Группы',
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(verbose_name='Вопрос')),
                ('is_anonymous', models.BooleanField(choices=[(True, 'Анонимный'), (False, 'Публичный')], default=False, verbose_name='Анонимный или публоичный')),
                ('type', models.CharField(choices=[('quiz', 'Викторина'), ('regular', 'Опрос')], default='Викторина', max_length=150, verbose_name='Тип вопроса')),
                ('explanation', models.TextField(verbose_name='Подсказка после завершения теста')),
                ('open_period', models.IntegerField(default=10, help_text='0 если не имеет ограничения во времени', verbose_name='Время завершения теста')),
                ('answer', models.TextField(verbose_name='Варианты ответа')),
                ('img', models.FileField(blank=True, null=True, upload_to='File/Image/', verbose_name='Фотография')),
                ('video_gif', models.FileField(blank=True, null=True, upload_to='File/Video_Gif/', verbose_name='Видео или Гиф')),
            ],
            options={
                'verbose_name': 'Вопрос сборнику',
                'verbose_name_plural': '3 Вопросы сборников',
            },
        ),
        migrations.CreateModel(
            name='Poll_type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('beginner', 'Beginner'), ('general_english', 'General-English'), ('pre_ielts', 'Pre-IELTS'), ('ielts', 'IELTS')], max_length=250, verbose_name='Вариант группы')),
            ],
            options={
                'verbose_name': 'Класс учащего',
                'verbose_name_plural': '1 Классы учащихся',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, unique=True)),
                ('username', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.BigIntegerField()),
                ('true_option', models.IntegerField()),
                ('name', models.CharField(max_length=250, null=True)),
                ('poll_id', models.CharField(max_length=250, null=True)),
                ('answer', models.CharField(max_length=250, null=True)),
                ('point', models.IntegerField()),
                ('chat_id', models.CharField(max_length=250)),
            ],
            options={
                'verbose_name': 'Ответ Юзера',
                'verbose_name_plural': 'Ответы Юзеров',
            },
        ),
        migrations.CreateModel(
            name='Poll_class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField(verbose_name='Номер сборника')),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='course', to='main.poll_type')),
            ],
            options={
                'verbose_name': 'Сборник вопроса',
                'verbose_name_plural': '2 Сборники вопросов',
            },
        ),
        migrations.CreateModel(
            name='Poll_answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('options', models.CharField(max_length=250, verbose_name='Вариант ответа (F1,F2)')),
                ('correct_option', models.BooleanField(default=False, help_text='True - правильный\n\nFalse - неправильный', verbose_name='Тип ответа')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quest', to='main.poll', verbose_name='Вопрос')),
            ],
            options={
                'verbose_name': 'Вариант Ответа',
                'verbose_name_plural': '4 Варианты Ответов',
            },
        ),
        migrations.AddField(
            model_name='poll',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='nam', to='main.poll_class', verbose_name='Сборник'),
        ),
    ]
