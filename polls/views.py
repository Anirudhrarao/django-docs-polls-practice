from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from polls.models import Questions,Choice
from django.http import Http404
from django.urls import reverse
from django.views import generic

# def index(request):
#     latest_questions = Questions.objects.order_by('-pub_date')
#     context = {
#         'latest_questions' : latest_questions
#     }
#     return render(request,'index.html',context)
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_questions'

    def get_queryset(self):
        return Questions.objects.order_by('-pub_date')

def detail(request, question_id):
    # try:
    #     question = Questions.objects.get(pk=question_id)
    # except Questions.DoesNotExist:
    #     raise Http404('Question does not exist.')
    question = get_object_or_404(Questions,pk=question_id)
    return render(request,'detail.html',{'question':question})

def results(request,question_id):
    question = get_object_or_404(Questions,pk=question_id)
    return render(request,'result.html', {'question':question})
def vote(request,question_id):
    question = get_object_or_404(Questions,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request,'detail.html',{'question':question,'error_message':"you did'nt select choice."})

    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result',args=(question.id,)))