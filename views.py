from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Contact
from django import forms
from .forms import contactform2  , contactform3
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm 




# Create your views here.
def controleform1(request):
    if request.method == 'POST':
        f = request.POST['firstname']
        l = request.POST['lastname']
        e = request.POST['email']
        m = request.POST['message']
        
        # Create the Contact object
        contact = Contact.objects.create(firstname=f, lastname=l, email=e, message=m)
        #contact=Contact(firstname=f,lastname=l,Email=e,msg=m)

        # contact.save()  # This line is not necessary since create() already saves it

        return HttpResponse('<h2> Data has been submitted </h2>')

    return render(request, "myform1.html")  # Return the form if not a POST request






def controleform3(request):
    if request.method == 'POST':  # If it's a POST request
        form = contactform3(request.POST)  # We get the data
        if form.is_valid():  # We check if the data is valid
            form.save()  # Save the form data to the database
            return HttpResponse('<h2>Data has been submitted</h2>')  # Success message
    else:  # If not POST, create an empty form
        form = contactform3()  # Create an empty form
    
    return render(request, "myform3.html", {'mycontactform3': form})  # Render the form

def contactView(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            email_list = []
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            to_email = form.cleaned_data['to_email']
            email_list.append(to_email)

            try:
                send_mail(subject, message, from_email, email_list)
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "email.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')
