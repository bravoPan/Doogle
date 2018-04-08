from django.shortcuts import render
from django.http import HttpResponse
from .models import Questions
from django.template import loader


# Create your views here.

def index(request):
    lastest_question_list = Questions.objects.order_by('-pub_data')[:5]
    # out_put = ', '.join([q.question_text for q in lastest_question_list])
    template = loader.get_template("search/index.html")
    context = {
        'latest_question_list': lastest_question_list,
    }
    return HttpResponse(template.render(context, request))


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting %s." % question_id)
