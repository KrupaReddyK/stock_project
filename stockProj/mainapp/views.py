from django.shortcuts import render,HttpResponse,redirect
from yahoo_fin.stock_info import *
import queue
from threading import Thread
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# Create your views here.
def register(request):
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Login')
    else:
        form = UserCreationForm()
    return render(request, 'mainapp/register.html', {'form':form})



@login_required   
def stockPicker(request):
    stock_picker = tickers_nifty50()
    return render(request,'mainapp/stockpicker.html',{'stockpicker':stock_picker})

@login_required   
def profile(request):
    return render(request, 'mainapp/profile.html') 
def stockTracker(request):
    stockpicker= request.GET.getlist('stockpicker')
    data = {}
    available_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")
        
    n_threads = len(stockpicker)
    thread_list= []
    que = queue.Queue()
    
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}),args = (que,stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()
        
    while not que.empty():
        result = que.get()
        data.update(result)
        
       
    return render(request,'mainapp/stocktracker.html', {'data': data})