from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import SignUpForm,LoginForm,ContactForm
from busbookapp.form1 import DriverForm,CustomerForm,BusForm
from django.contrib.auth import authenticate, login
# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from busbookapp.models import Driver,Customer,User,MyModel,Bus
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from .forms import ContactForm
from django.contrib import messages
def index(request):
    return render(request, 'busbookapp/index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request,"Email already exists")
                return redirect("register")
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            user = form.save()
            message = f" Hi {username}!\n Welcome to Bus Reservation System\n You Successfully registered with us ! \nlink: http://127.0.0.1:8000/login/"
            email_msg = EmailMessage(
                subject="Booking Details",
                body=message,
                from_email='soorya@market-intellect.com',
                to=[email],
                reply_to=[email])
            email_msg.send()
            return redirect('login')

        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'busbookapp/register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password,)
            if user is not None and user.is_admin:
                login(request, user)
                return redirect('adminwelcome')
            elif user is not None and user.is_customer:
                login(request, user)
                return redirect('consumerwelcome')
            elif user is not None and user.is_employee:
                login(request, user)
                return redirect('drwelcome/')
            else:
                msg= 'incorrect username or password'
        else:
            msg = 'error validating form'
    return render(request, 'busbookapp/login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'busbookapp/admin.html')


def customer(request):
    return render(request,'busbookapp/customer.html')


def employee(request):
    return render(request,'busbookapp/employee.html')






# @login_required(login_url='signin')
# @admin_only
def empDetails(request):
    emp_data=Driver.objects.all()
    emp_dict = {"emp_list":emp_data}
    return render(request, "busbookapp/index1.html", context =emp_dict)
    #return HttpResponse("<h1 this is my application <h1>")
# @login_required(login_url='signin')
# @allowed_users(allowed_roles=['admin','Driver'])
def driverDetails(request):
    emp_data=Driver.objects.all()
    emp_dict = {"emp_list":emp_data}
    return render(request, "busbookapp/driver.html", context =emp_dict)
#u
def create_view(request):
    form=DriverForm()
    if request.method =="POST":
        form = DriverForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    return render(request,"busbookapp/create.html",{"form":form})


def delete_view(request,id):
    emp_data=Driver.objects.get(id=id)
    emp_data.delete()
    return redirect("/home")

def update_view(request,id):
    emp_data=Driver.objects.get(id=id)
    # emp_data={"emp_data":emp_data}
    # return render(request, "busapp1/update.html", context=emp_data)
    if request.method == "POST":
        drivername=request.POST["drivername"]
        age=request.POST["age"]
        contact_no=request.POST["contact_no"]
        bus_no=request.POST["bus_no"]
        emp_data.drivername = drivername
        emp_data.age=age
        emp_data.contact_no=contact_no
        emp_data.bus_no=bus_no
        emp_data.save()
        return redirect("/home")
    return render(request, "busbookapp/update.html",{"emp_data":emp_data})

def homepage(request):
    return render(request,"busbookapp/homepage.html")

def signout(request):
    context = {}
    logout(request)
    context['error'] = "You have been logged out"
    return render(request, 'busbookapp/login.html', context)



def consumerdisplay_view(request):
    info=Customer.objects.all()
    return render(request,"busbookapp/consumerdisplay.html",{"info":info})


def consumer_view(request):
    form1=CustomerForm()
    if request.method =='POST':
        form1=CustomerForm(request.POST)
        if form1.is_valid():
            form1.save()
            return redirect('/consumerdisplay')

    return render(request,'busbookapp/consumeradd.html',{'form1':form1})

def deleteconsumer_view(request ,id):
    info =Customer.objects.get(id=id)
    info.delete()
    return redirect('/consumerdisplay')

def updateconsumer_view(request, id):
        consumer_data = Customer.objects.get(id=id)
        if request.method == ('POST'):
            name = request.POST["name"]
            age= request.POST["age"]
            address=request.POST['address']
            phone=request.POST['phone']
            start = request.POST["start"]
            end = request.POST["end"]
            date = request.POST["date"]
            time = request.POST["time"]
            consumer_data.name = name
            consumer_data.age = age
            consumer_data.address = address
            consumer_data.phone = phone
            consumer_data.start= start
            consumer_data.end = end
            consumer_data.date = date
            consumer_data.time = time
            consumer_data.save()
            return redirect('/consumerdisplay')
        return render(request, 'busbookapp/consumerupdate.html', {"consumer_data": consumer_data})

def customerview(request):
    info = Customer.objects.all()
    return render(request, "busbookapp/customerview.html", {"info": info})


def foreignkey(request):
    grpdata=MyModel.objects.all()
    grpdata = {"grpdata":grpdata}
    return render(request, "busbookapp/foreignkey.html", context =grpdata)


def selectionfeild(request):
    selfield=User.objects.all()
    selfield={"selfield":selfield}
    return render(request, "busbookapp/register.html", context=selfield)

def busseat(request):
    return render(request,"busbookapp/busseat.html")

def seat(request):
    return render(request,"busbookapp/seat.html")

def consumerwelcome(request):
    return render(request,"busbookapp/consumerwelcome.html")


def adminwelcome(request):
    return render(request,"busbookapp/adminwelcome.html")

# from django.core.mail import send_mail
# from django.core.mail import EmailMessage
# from django.shortcuts import render,redirect
# from django.template.loader import render_to_string
# from .forms import ContactForm

def mail(request):
    if request.method=='POST':
        form=ContactForm(request.POST)

        if form.is_valid():
            name=form.cleaned_data['name']
            age=form.cleaned_data['age']
            email=form.cleaned_data['email']
            address = form.cleaned_data['address']
            contact_no = form.cleaned_data['contact_no']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            date = form.cleaned_data['date']
            time = form.cleaned_data['time']
            content = form.cleaned_data['content']

            html=render_to_string('busbookapp/email.html',{
                'name':name,
                'age':age,
                'email':email,
                'address': address,
                'contact_no':contact_no,
                'start':start,
                'end':end,
                'date':date,
                'time':time,
                'content': content,
            })
            message=f"name: {name}\nemail: {email}\naddress: {address}\nphone: {contact_no}\nstart: {start}\nend: {end}\ndate: {date}\ntime: {time}\nmessage: {content}\n link: "
            email_msg=EmailMessage(
                subject="Booking Details",
                body=message,
                from_email='sanjaikumar@market-intellect.com',
                to=[email],
                reply_to=[email])
            email_msg.send()

            # send_mail('Booking Details', 'This is the message', 'sanjaikumar@market-intellect.com',
            #           ['janavinoth2000@gmail.com'], html_message=html)
            return redirect("/thank")

    else:
        form = ContactForm()
        return render(request, 'busbookapp/mail.html', {'form': form})




def thank(request):
    return render(request,"busbookapp/thank.html")
def drwelcome(request):
    return render(request,"busbookapp/driverwelcome.html")

def conseat(request):
    return render(request,"busbookapp/consumerseat.html")
def Busdisplay(request):
    ticket1 = Bus.objects.all()
    return render(request, "busbookapp/busdisplay.html", {"ticket1": ticket1})


def Busadd(request):
    form = BusForm()
    if request.method == 'POST':
        form = BusForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/busdisplay')

    return render(request, 'busbookapp/busadd.html', {'form': form})


def Busupdate(request, id):
    bus_data = Bus.objects.get(id=id)
    if request.method == 'POST':
        bus_name = request.POST["bus_name"]
        bus_num = request.POST["bus_num"]
        start = request.POST["start"]
        end = request.POST["end"]
        seats = request.POST["seats"]
        amount = request.POST["amount"]
        date = request.POST["date"]
        time = request.POST["time"]
        bus_data.bus_name = bus_name
        bus_data.bus_num = bus_num
        bus_data.start = start
        bus_data.end = end
        bus_data.seats = seats
        bus_data.amount = amount
        bus_data.date = date
        bus_data.time = time
        bus_data.save()

        return redirect('/busdisplay')
    return render(request, 'busbookapp/busupdate.html', {"bus_data": bus_data})


def Busdelete(request, id):
    bus_data = Bus.objects.get(id=id)
    bus_data.delete()
    return redirect('/busdisplay')