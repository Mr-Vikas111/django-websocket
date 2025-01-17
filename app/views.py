from django.shortcuts import render
from .models import Group, Chat

# Create your views here.


def index(request,group_name):
    """AI is creating summary for index

    Args:
        request ([type]): [description]
    """
    # print("group_name",group_name)
    
    # check group created and listing group wise chat listing
    chat =[]
    if Group.objects.filter(name=group_name).exists():
        chat = Chat.objects.filter(group__name=group_name)
    else:
        Group.objects.create(name=group_name)
    
    return render(request,'app/index.html',{'group_name':group_name,'chats':chat})