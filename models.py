from django.db import models

class DayModel (models.Model):
    #todo_list = models.ForeignKey(ListModel, on_delete=models.CASCADE)
    day = models.IntegerField()
    date = models.DateField(blank = False)
    name = models.CharField(max_length = 30, blank = True)

    def __str__(self):
        return str(self.date)