from django.shortcuts import render, redirect
from django.db.models import Count, Q, Sum
from .models import Participant, Webinar, Ticket, Session
from datetime import datetime, timedelta
# Create your views here.
def home(request):
    return render(request, "home.html")

def import_webinar(request):
    if request.method == "POST":
        if "data" in request.POST:
            data = request.POST.get("data")
            rows = data.split("\n")
            errors = []
            for row in rows:
                try:
                    cell = row.split("\t")
                    attended = cell[0]
                    username = cell[1]
                    first_name = cell[2]
                    last_name = cell[3]
                    email = cell[4]
                    address = cell[5]
                    city = cell[6]
                    country = cell[7]
                    zip_code = cell[8]
                    state_province = cell[9]
                    reg_time = cell[10]
                    try:
                        reg_time = datetime.strptime(reg_time, "%m/%d/%Y %H:%M")
                        reg_time = reg_time + timedelta(hours=8)
                    except:
                        reg_time = None
                    approval_status = cell[11]
                    join_time = cell[12]
                    try:
                        join_time = datetime.strptime(join_time, "%m/%d/%Y %H:%M")
                        join_time = join_time + timedelta(hours=8)
                    except:
                        join_time = None
                    print(email + " " + str(join_time))
                    leave_time = cell[13]
                    try:
                        leave_time = datetime.strptime(leave_time, "%m/%d/%Y %H:%M")
                        leave_time = leave_time + timedelta(hours=8)
                    except:
                        leave_time = None
                    time_session = cell[14]
                    if time_session == "--":
                        time_session = 0
                    hospital_organization = cell[15]
                    region2 = cell[16]
                    city2 = cell[17]
                    role = cell[18]
                    specialty = cell[19]
                    specialty2 = cell[20]
                    learn = cell[21]
                    country2 = cell[22]
                    webinar_no = cell[23]

                    participant = Participant.objects.filter(email=email)
                    if participant.exists():
                        participant = participant.first()
                        participant.first_name = first_name
                        participant.last_name = last_name
                        participant.city = city
                        participant.country = country
                        participant.zip_code = zip_code
                        participant.state_province = state_province
                        participant.hospital_organization = hospital_organization
                        participant.region2 = region2
                        participant.city2 = city2
                        participant.role = role
                        participant.specialty = specialty
                        participant.specialty2 = specialty2
                        participant.learn_event = learn
                        participant.country2 = country2
                        participant.save()
                    else:
                        participant = Participant.objects.create(
                            email=email,first_name=first_name,last_name=last_name,address=address,
                            city=city,country=country,zip_code=zip_code,state_province=state_province,
                            hospital_organization=hospital_organization,region2=region2,city2=city2,
                            role=role,specialty=specialty,specialty2=specialty2,learn_event=learn,country2=country2
                            )

                    webinar = Webinar.objects.filter(number=webinar_no)
                    if webinar.exists():
                        webinar = webinar.first()
                    else:
                        webinar = Webinar.objects.create(number=webinar_no)
                    
                    ticket = Ticket.objects.filter(participant=participant,webinar=webinar)
                    if ticket.exists():
                        ticket = ticket.first()
                    else:
                        ticket = Ticket.objects.create(participant=participant,webinar=webinar,registration_time=reg_time,approval_status=approval_status)
                    
                    session = Session.objects.filter(ticket=ticket,join_time=join_time,leave_time=leave_time)
                    if session.exists():
                        session = session.first()
                    elif join_time != None and leave_time != None:
                        session = Session.objects.create(ticket=ticket,join_time=join_time,leave_time=leave_time,time_in_session=time_session)
                except Exception as e:
                    print(e) 
                    errors.append(row)
            print(errors)
    return redirect("home")

def webinar_no(request, webinar_no):
    try:
        webinar = Webinar.objects.get(number=webinar_no)
    except Exception as e:
        print(e)
        return redirect("home")
    return render(request, "webinar.html", {"webinar": webinar, "tickets": webinar.ticket.all(), "certOnly": False})
    
def webinar_cert(request, webinar_no):
    try:
        webinar = Webinar.objects.get(number=webinar_no)
    except Exception as e:
        print(e)
        return redirect("home")
    return render(request, "webinar.html", {"webinar": webinar, "tickets": webinar.with_cert(), "certOnly": True})

def webinar_cert_time(request, webinar_no, time_for_certificates):
    try:
        webinar = Webinar.objects.get(number=webinar_no)
    except Exception as e:
        print(e)
        return redirect("home")
    try:
        webinar.minutes_for_certificate = time_for_certificates
        webinar.save()
    except Exception as e:
        print(e)
    return redirect("home")
    # return redirect("webinar_no", webinar_no=webinar_no)

def webinar_cert_link(request, webinar_no):
    try:
        webinar = Webinar.objects.get(number=webinar_no)
    except Exception as e:
        print(e)
        return redirect("home")
    if "data" in request.POST:
        data = request.POST.get("data")
        rows = data.split("\n")
        errors = []
        for row in rows:
            try:
                id = row.split("@@")[1].replace("StopCovidDeathsCertificate_","")
                id = id.replace(".pdf", "")
                link = row.split("@@")[0]
                ticket = Ticket.objects.get(pk=id)
                ticket.cert_link = link
                ticket.save()
            except Exception as e:
                print(e)
    return redirect("webinar_cert", webinar_no=webinar_no)

def webinar_new_registrants(request, webinar_no):
    try:
        webinar = Webinar.objects.get(number=webinar_no)
    except Exception as e:
        print(e)
        return redirect("home")
    return render(request, "webinar.html", {"webinar": webinar, "tickets": webinar.new_registrants(), "certOnly": False})
        
def webinar_attendees(request, webinar_no):
    try:
        webinar = Webinar.objects.get(number=webinar_no)
    except Exception as e:
        print(e)
        return redirect("home")
    return render(request, "webinar.html", {"webinar": webinar, "tickets": webinar.attendees(), "certOnly": False})
        
def webinar_new_attendees(request, webinar_no):
    try:
        webinar = Webinar.objects.get(number=webinar_no)
    except Exception as e:
        print(e)
        return redirect("home")
    return render(request, "webinar.html", {"webinar": webinar, "tickets": webinar.new_attendees(), "certOnly": False})

def chart(request):
    participants = Ticket.objects.all()
    participants = participants.values("participant")
    top10byWebinar = participants.annotate(webinars_attended=Count('pk'))
    top10byWebinar = top10byWebinar.order_by("-webinars_attended")
    top10byWebinar = top10byWebinar[:120]

    top10byMinutes = participants.annotate(minutes=Sum("ticket_session__time_in_session"))
    top10byMinutes = top10byMinutes.order_by("-minutes")
    top10byMinutes = top10byMinutes[:10]

    return render(request, "chart.html", {"top10byWebinar":top10byWebinar,"top10byMinutes":top10byMinutes, "webinars": Webinar.objects.all()})

def test(request):
    return render(request, "test.html", {"participants":Participant.objects.all()})

def participant_details(request, email):
    participant = Participant.objects.get(email=email)
    tickets = Ticket.objects.filter(participant=participant)
    return render(request, "participant.html", {"participant": participant, "tickets": tickets})