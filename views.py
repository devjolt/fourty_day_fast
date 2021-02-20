from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import DayModel
import re

def home(request):
    if request.method == 'POST':
        for key,value in request.POST.items():
            if key == 'delete':#if user wants to delete their name...
                del_number, del_name = request.COOKIES['selected'].split(',')#get their cookie, containing their chosen day number and name
                DayModel.objects.filter(day=del_number).update(name='')#model object with matching day number: name field to ''
                response = HttpResponseRedirect('/fast')#delete cookie and redirect to same page
                response.delete_cookie('selected')
                return response
            elif key == 'name':#if user wants to add their name...
                number = request.POST['number']#assign post number
                up_name = request.POST['name']#assign post name
                DayModel.objects.filter(day=number).update(name=up_name)#update model object with post number with post name
                up_name_dashes = re.sub(' ', '-', up_name)#convert any spaces in name to dashes for cookie storage
                response = HttpResponseRedirect('/fast')
                response.set_cookie('selected', ','.join([number, up_name_dashes]), None)#make 'day_number,name-with-spaces' string and add this to cookie
                return response
    else:
        context = {'days':[]}#create context dict which will contain list of other dicts
        if 'selected' in request.COOKIES.keys():
            del_number, del_name = request.COOKIES['selected'].split(',')#get their cookie, containing their chosen day number and name
            model_list = DayModel.objects.order_by('-day')[::-1]
                
            for item in model_list:
                
                if item.day == int(del_number):#should only be one of these, with permission to delete, but not to add
                    context['days'].append({'day':item, 'allow_delete': True, 'allow_add':False})
                else:#all others, no delete, no add
                    context['days'].append({'day':item, 'allow_delete': False, 'allow_add':False})
    
        else:#no preexisting cookie named select SO all available days able to be added
            #note, if name exists, we will not allow add form, but will provide delete button
            model_list = DayModel.objects.order_by('-day')[::-1]
            for item in model_list:
                context['days'].append({'day':item, 'allow_delete': None, 'allow_add':True})
    print(context)
    return render(request, 'fourty_day_fast/fourty.html', context)

'''template:
Display card for each day

Each card:
If card has a name associated with it, disallow form

Has a form allowing entry of a name
When form submitted, add cookie to client browser
If cookie added:
disallow submitting another form
highlight current selection and allow deselection
deselection removes name from database and removes cookie
'''
