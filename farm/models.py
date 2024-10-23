from django.db import models
from core.models import BaseModel
from account.models import User


class Farm(BaseModel):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name


class Property(BaseModel):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    ownerfirst = models.CharField(max_length=200)
    ownerlast = models.CharField(max_length=200)
    siteaddres = models.CharField(max_length=200)
    sitestate = models.CharField(max_length=200, null=True, blank=True)
    sitecity = models.CharField(max_length=200, null=True, blank=True)
    sitezip = models.CharField(max_length=200, null=True, blank=True)
    mailaddres = models.CharField(max_length=200, null=True, blank=True)
    mailcity = models.CharField(max_length=200, null=True, blank=True)
    mailstate = models.CharField(max_length=200, null=True, blank=True)
    mzipandzip = models.CharField(max_length=200, null=True, blank=True)
    bedrooms = models.CharField(max_length=200, null=True, blank=True)
    bathtot = models.CharField(max_length=200, null=True, blank=True)
    totalsf = models.CharField(max_length=200, null=True, blank=True)
    lotsqft = models.CharField(max_length=200, null=True, blank=True)
    landuse = models.CharField(max_length=200, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.ownerfirst} {self.ownerlast}"
