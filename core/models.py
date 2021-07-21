from django.db import models
from datetime import datetime
# Create your models here.
class Participant(models.Model):
    email = models.CharField(max_length=128,blank=True,null=False)
    first_name = models.CharField(max_length=128,blank=True,null=False)
    last_name = models.CharField(max_length=128,blank=True,null=False)
    address = models.CharField(max_length=256,blank=True,null=False)
    city = models.CharField(max_length=128,blank=True,null=False)
    country = models.CharField(max_length=128,blank=True,null=False)
    zip_code = models.CharField(max_length=128,blank=True,null=False)
    state_province = models.CharField(max_length=128,blank=True,null=False)
    hospital_organization = models.CharField(max_length=128,blank=True,null=False)
    region2 = models.CharField(max_length=128,blank=True,null=False)
    city2 = models.CharField(max_length=128,blank=True,null=False)
    role = models.CharField(max_length=128,blank=True,null=False)
    specialty = models.CharField(max_length=128,blank=True,null=False)
    specialty2 = models.CharField(max_length=128,blank=True,null=False)
    learn_event = models.CharField(max_length=128,blank=True,null=False)
    country2 = models.CharField(max_length=128,blank=True,null=False)

    def __str__(self):
        return self.first_name + " " + self.last_name + " <"+self.email+">"

    def get_webinars_attended_by_name(self):
        return Ticket.objects.filter(participant__first_name=self.first_name,participant__last_name=self.last_name).values("webinar").distinct()


class Webinar(models.Model):
    number = models.IntegerField(null=False,default=0)
    minutes_for_certificate = models.IntegerField(null=False,default=0)

    def __str__(self):
        return str(self.number)

    def attendees(self):
        ticket_ids = []
        tickets = Ticket.objects.filter(webinar=self)
        for ticket in tickets:
            if ticket.total_time() > 0:
                ticket_ids.append(ticket.id)
        return Ticket.objects.filter(id__in=ticket_ids)
    
    def with_cert(self):
        ticket_ids = []
        tickets = Ticket.objects.filter(webinar=self)
        for ticket in tickets:
            if ticket.total_time() >= self.minutes_for_certificate:
                ticket_ids.append(ticket.id)
        return Ticket.objects.filter(id__in=ticket_ids)

    def new_registrants(self):
        return Ticket.objects.filter(webinar=self).exclude(participant__in=Ticket.objects.filter(webinar__number__lt=self.number).values("participant"))

    def new_attendees(self):
        ticket_ids = []
        tickets = self.new_registrants()
        for ticket in tickets:
            if ticket.total_time() > 0:
                ticket_ids.append(ticket.id)
        return Ticket.objects.filter(id__in=ticket_ids)
                
        

class Ticket(models.Model):
    participant = models.ForeignKey(Participant,on_delete=models.CASCADE,related_name="ticket")
    webinar = models.ForeignKey(Webinar,on_delete=models.CASCADE,related_name="ticket")
    registration_time = models.DateTimeField(default=datetime.now,null=False)
    approval_status = models.CharField(max_length=128,blank=True,null=False)
    cert_link = models.CharField(max_length=256,blank=True,null=False)
    def total_time(self):
        sessions = Session.objects.filter(ticket=self)
        total = 0
        for session in sessions:
            total += session.time_in_session
        return total
    def get_link_id(self):
        try:
            return self.cert_link.split("/")[5]
        except:
            return ""

class Session(models.Model):
    ticket = models.ForeignKey(Ticket,on_delete=models.CASCADE,related_name="ticket_session")
    join_time = models.DateTimeField(default=datetime.now,null=True)
    leave_time = models.DateTimeField(default=datetime.now,null=True)
    time_in_session = models.IntegerField(null=False,default=0)