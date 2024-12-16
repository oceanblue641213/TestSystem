from django.db import models

class GWP(models.Model):
    #region 資料庫Schema
    class Meta:
        db_table = 'GWP'
        managed = True

    # 欄位（Fields）
    Year = models.IntegerField()
    IPCC = models.CharField(max_length=45)
    co2 = models.FloatField()
    ch4 = models.FloatField()
    n2o = models.FloatField()
    sf6 = models.FloatField()
    nf3 = models.FloatField()

    #endregion

    # 建構子（__init__ 方法）
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)