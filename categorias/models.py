from django.db import models

class Categoria(models.Model):
    genero = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.genero
