from django.db import models

class Universitas(models.Model):
    nama_univ = models.CharField(max_length=255)
    url_univ = models.CharField(max_length=255)
    total_sitasi = models.IntegerField(default=0, blank=True, null=True)  # Menambah field untuk total sitasi
    def __str__(self):
        return self.nama_univ

class Detail_cited(models.Model):
    afiiliation = models.CharField(max_length=255)
    nama_dosen = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    cited_by = models.IntegerField(null=True)
    urldosen = models.URLField(null=True)
    fk_url_univ = models.ForeignKey(Universitas, on_delete=models.CASCADE, null=True)

    def save(self, *args, **kwargs):
        # Mengupdate total sitasi pada Univeristas ketika objek Detail_cited dibuat atau diupdate
        super().save(*args, **kwargs)
        if self.fk_url_univ:
            total_sitasi = Detail_cited.objects.filter(fk_url_univ=self.fk_url_univ).aggregate(total_sitasi=models.Sum('cited_by'))['total_sitasi']
            self.fk_url_univ.total_sitasi = total_sitasi or 0
            self.fk_url_univ.save()
