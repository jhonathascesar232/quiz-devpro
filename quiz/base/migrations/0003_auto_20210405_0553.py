# Generated by Django 3.1.7 on 2021-04-05 08:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20210328_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pontos', models.IntegerField()),
                ('respondida_em', models.DateTimeField()),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.aluno')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.pergunta')),
            ],
        ),
        migrations.AddConstraint(
            model_name='resposta',
            constraint=models.UniqueConstraint(fields=('aluno', 'pergunta'), name='resposta_unica'),
        ),
    ]