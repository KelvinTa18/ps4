from django.db import models

# Create your models here.


class Predict(models.Model):
    class Meta:
        # Definisikan kombinasi unik dari tabel_a dan tabel_b untuk mencegah duplikat
        permissions = (
            ('predict_one', 'can predict one student'),
            ('predict_all', 'can predict all student'),
        )
