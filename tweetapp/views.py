from django.shortcuts import render, redirect
from . import models, forms
from django.urls import reverse, reverse_lazy
from tweetapp.forms import AddTweetFOrm, AddTweetModelForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm #class based views
from django.views.generic import CreateView




def listtweet(request):
    all_tweets = models.Tweet.objects.all()
    #python manage.py createsuperuser
    tweet_dict = {"tweets": all_tweets}
    return render(request, 'tweetapp/listtweet.html',context=tweet_dict)
#<QueryDict: {'csrfmiddlewaretoken': ['hNHMGIryV1YZ66HrwjVBxPPTJCWtYeeHc5I2vNezJ2U34Vtyh6d1Xwd9ieycbRgy']}>
    #Bununla birlikte input'taki bilgilerin de gelmesini istiyorsak ilgili html elementlerine name
    #attribute'unu vermemiz gerekmektedir.
    
@login_required(login_url="/login")
def addtweet(request):   #NORMAL FORMLAR!!!!!!!!!!!
    # if request.POST:
    #     print(request.POST["nickname"])
    #     print(request.POST["message"])
    if request.POST:
        # nickname = request.POST["nickname"]
        message = request.POST["message"]
        # tweet = models.Tweet(nickname, message)
        # tweet.save()
        models.Tweet.objects.create(username=request.user, message=message)
        return redirect(reverse('tweetapp:listtweet'))
    else:
        return render(request, 'tweetapp/addtweet.html')
    

def addtweetbyform(request): #DJANGO'NUN KENDİ FORMLARI !!!!!!!!!!!
    if request.method == "POST":
        #print(request.POST)
        form = AddTweetFOrm(request.POST)
        if form.is_valid(): #Form geçerli ise
            #print(form.cleaned_data)
            nickname = form.cleaned_data["nickname_input"]
            message = form.cleaned_data["message_input"]
            models.Tweet.objects.create(nickname = nickname, message = message)
            return redirect(reverse("tweetapp:listtweet"))
        else:
            print("error in form")
            return render(request, "tweetapp/addtweetbyform.html", context={"form":form})
    else:
        form = AddTweetFOrm()
        return render(request, "tweetapp/addtweetbyform.html", context={"form":form})
    

def addtweetbymodelform(request):
    if request.method == "POST":
        #print(request.POST)
        form = AddTweetModelForm(request.POST)
        if form.is_valid(): #Form geçerli ise
            #print(form.cleaned_data)
            nickname = form.cleaned_data["nickname"]
            message = form.cleaned_data["message"]
            models.Tweet.objects.create(nickname = nickname, message = message)
            return redirect(reverse("tweetapp:listtweet"))
        else:
            print("error in form")
            return render(request, "tweetapp/addtweetbymodelform.html", context={"form":form})
    else:
        form = AddTweetModelForm()
        return render(request, "tweetapp/addtweetbymodelform.html", context={"form":form})
    
@login_required
def deletetweet(request, id):
    tweet = models.Tweet.objects.get(pk = id)
    if request.user == tweet.username:
        models.Tweet.objects.filter(id=id).delete()
        return redirect('tweetapp:listtweet')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login") #Her uygulamayı çalıştırdığımızda reverse'lere bakılır, böyle bir yer var mı gibisinden. Halbuki
    #bir kere kullanılcak bir view. Fakat biz bunu her reverse yaptığımızda çalışıcak. O yüzden reverse demek yerine reverse lazy kullanılır.
    template_name = "registration/signup.html"
    
    
