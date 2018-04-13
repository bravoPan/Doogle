from django.shortcuts import render
from django.http import HttpResponse
from .models import Questions
from django.template import loader
from sqlite3 import connect, dbapi2
from search_engine.models import PageInfo, WordList
from django.shortcuts import render, redirect
import time


# Create your views here.

def index(request):
    lastest_question_list = Questions.objects.order_by('-pub_data')[:5]
    # out_put = ', '.join([q.question_text for q in lastest_question_list])
    template = loader.get_template("search_page.html")
    context = {
        'latest_question_list': lastest_question_list,
    }
    return render(request, "search_page.html", context)


def display(request, key_words):
    context = {}
    try:
        keywords = key_words.split()
        word = []
        start = time.time()
        for i in keywords:
            word += WordList.objects.filter(word=i)
        end = time.time()
        context["time"] = end - start
        page_info = set([i.url_location_id for i in word])
        context["result_number"] = len(page_info)
        context["pages_info"] = page_info
        return render(request, "display_search_item.html", context)
    except:
        return render(request, "display_search_item.html", None)


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting %s." % question_id)
