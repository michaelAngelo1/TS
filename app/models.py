"""
Definition of models.
"""

from django.db import models

# Create your models here.

class Promo(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    Nama = models.CharField(max_length=250,null=True,blank=True,db_column="Nama")
    Keterangan = models.CharField(max_length=250,null=True,blank=True,db_column="Keterangan")
    
    def __str__(self):
        if self.Nama is not None:
            return self.Nama
        else:
            return ""

    class Meta:
        db_table = "Promo"
        managed = False

class Telemarketing(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    Nama = models.CharField(max_length=250,null=True,blank=True,db_column="Nama")
    
    def __str__(self):
        if self.Nama is not None:
            return self.Nama
        else:
            return ""

    class Meta:
        db_table = "Telemarketing"
        managed = False

class Player(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    Username = models.CharField(max_length=50,db_column="Username")
    Nama = models.CharField(max_length=250,null=True,blank=True,db_column="Nama")
    Phone = models.CharField(max_length=50,null=True,blank=True,db_column="Phone")
    Email = models.CharField(max_length=250,null=True,blank=True,db_column="Email")
    Bank = models.CharField(max_length=50,null=True,blank=True,db_column="Bank")
    NoRekening = models.CharField(max_length=50,null=True,blank=True,db_column="NoRekening")
    Referal = models.ForeignKey('self', db_column="Referal", on_delete=models.SET_NULL, null=True, blank=True)
    Promo = models.ForeignKey(Promo, db_column="Promo", on_delete=models.SET_NULL, null=True, blank=True)
    Telemarketing = models.ForeignKey(Telemarketing, db_column="Telemarketing", on_delete=models.SET_NULL, null=True, blank=True)
    Saldo = models.IntegerField(db_column="Saldo")
    Keterangan = models.TextField(db_column="Keterangan")

    def __str__(self):
        if self.Username is not None:
            return self.Username
        else:
            return ""

    class Meta:
        db_table = "Player"
        managed = False



class Akun(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    NamaAkun = models.CharField(max_length=250,null=True,blank=True,db_column="NamaAkun")
    Saldo = models.IntegerField(db_column="Saldo")
    Keterangan = models.TextField(max_length=250,null=True,blank=True,db_column="Keterangan")
    
    def __str__(self):
        if self.NamaAkun is not None:
            return self.NamaAkun
        else:
            return ""

    class Meta:
        db_table = "Akun"
        managed = False

# Deposit subclass
#class DepositManager(models.Manager):
#    def get_queryset(self, request):
#        return super().get_queryset().filter(CreateBy=request.user.username)

class Deposit(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    Tanggal = models.DateTimeField(db_column="Tanggal",null=True,blank=True)
    Player = models.ForeignKey(Player, db_column="Player", on_delete=models.SET_NULL, null=True, blank=True)
    Bank = models.ForeignKey(Akun, db_column="Bank", on_delete=models.SET_NULL, null=True, blank=True)
    Nominal = models.IntegerField(db_column="Nominal", default=None)
    Referensi = models.CharField(max_length=50,db_column="Referensi")
    Promo = models.ForeignKey(Promo, db_column="Promo", on_delete=models.SET_NULL, null=True, blank=True)
    Charge = models.IntegerField(db_column="Charge", default=None)
    CreateBy = models.CharField(max_length=50, null=True, blank=True, db_column="CreateBy")
    Operator = models.CharField(max_length=50, null=True, blank=True, db_column="Operator")

    def __str__(self):
        if str(self.Kode) is not None:
            return str(self.Kode)
        else:
            return ""

    class Meta:
        db_table = "Deposit"
        managed = False

#    objects = models.Manager
#    createby_objects = DepositManager()


class Withdraw(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    Tanggal = models.DateTimeField(db_column="Tanggal",null=True,blank=True)
    Player = models.ForeignKey(Player, db_column="Player", on_delete=models.SET_NULL, null=True, blank=True)
    Bank = models.ForeignKey(Akun, db_column="Bank", on_delete=models.SET_NULL, null=True, blank=True)
    Nominal = models.IntegerField(db_column="Nominal")
    Referensi = models.CharField(max_length=50,db_column="Referensi")
    Promo = models.ForeignKey(Promo, db_column="Promo", on_delete=models.SET_NULL, null=True, blank=True)
    Charge = models.IntegerField(db_column="Charge")
    
    def __str__(self):
        if self.Kode is not None:
            return str(self.Kode)
        else:
            return ""

    class Meta:
        db_table = "Withdraw"
        managed = False

class TransferAntarAkun(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    Tanggal = models.DateTimeField(db_column="Tanggal",null=True,blank=True)
    AkunAsal = models.ForeignKey(Akun, db_column="AkunAsal", related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
    Nominal = models.IntegerField(db_column="Nominal")
    Charge = models.IntegerField(db_column="Charge")
    AkunTujuan = models.ForeignKey(Akun, db_column="AkunTujuan", related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        if self.Kode is not None:
            return self.Kode
        else:
            return ""

    class Meta:
        db_table = "TransferAntarAkun"
        managed = False

class Bonus(models.Model):
    Kode = models.AutoField(primary_key=True, db_column="Kode")
    Tanggal = models.DateTimeField(db_column="Tanggal",null=True,blank=True)
    Player = models.ForeignKey(Player, db_column="Player", on_delete=models.SET_NULL, null=True, blank=True)
    Nominal = models.IntegerField(db_column="Nominal")
    Promo = models.ForeignKey(Promo, db_column="Promo", on_delete=models.SET_NULL, null=True, blank=True)
    Keterangan = models.CharField(max_length=250,db_column="Keterangan")
    
    def __str__(self):
        if self.Kode is not None:
            return self.Kode
        else:
            return ""

    class Meta:
        db_table = "Bonus"
        managed = False
