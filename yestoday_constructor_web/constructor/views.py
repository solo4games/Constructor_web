from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, JsonResponse
from .functions import *


def index(request: HttpRequest):
    return render(request, 'index.html')


def quiz1(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz1(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def quiz2(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz2(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def quiz3(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz3(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def quiz4(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz4(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def quiz5(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    s = s.split('\n')
    result_all = {"s": """""", "galery_number": galery_number,
                  "global_i": global_i, "global_i_i": global_i_i}
    while len(s) >= 2:
        result = pr_quiz5(
            "\n".join(s[:2]), result_all['galery_number'], result_all["global_i"], result_all["global_i_i"])
        result_all['s'] += result['s']
        result_all['galery_number'] = result['galery_number']
        result_all['global_i'] = result['global_i']
        result_all['global_i_i'] = result['global_i_i']
        for _ in range(2):
            s.pop(0)
    return JsonResponse(result_all)


def quiz6(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz6(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def quiz7(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz7(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def quiz8(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz8(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def quiz9(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiz9(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def audio(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_audio(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def cards(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_cards(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


# , s: str, galery_number: str, global_i: str, global_i_i: str
def quizphoto(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quizphoto(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


# , s: str, galery_number: str, global_i: str, global_i_i: str
def translate(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_translate(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def translate_new(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_translate_new(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)

# , s: str, galery_number: str, global_i: str, global_i_i: str


def audio_tts(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    s = s.split('\n')
    result_all = {"s": """""", "galery_number": galery_number,
                  "global_i": global_i, "global_i_i": global_i_i}
    while len(s) >= 4:
        result = pr_audio_tts(
            "\n".join(s[:4]), result_all['galery_number'], result_all["global_i"], result_all["global_i_i"])
        result_all['s'] += result['s']
        result_all['galery_number'] = result['galery_number']
        result_all['global_i'] = result['global_i']
        result_all['global_i_i'] = result['global_i_i']
        for _ in range(4):
            s.pop(0)
    return JsonResponse(result_all)


def video(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_video(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


# , s: str, galery_number: str, global_i: str, global_i_i: str
def quizOrder(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quizOrder(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def stt(request: HttpRequest):  # , s: str, galery_number: str, global_i: str, global_i_i: str
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_stt(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


# , s: str, galery_number: str, global_i: str, global_i_i: str
def quiztable(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_quiztable(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def audioQuiz5(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    s = s.split('\n')
    result_all = {"s": """""", "galery_number": galery_number,
                  "global_i": global_i, "global_i_i": global_i_i}
    while len(s) >= 6:
        result = pr_audio_tts(
            "\n".join(s[:4]), result_all['galery_number'], result_all["global_i"], result_all["global_i_i"])
        result_all['s'] += result['s']
        result_all['galery_number'] = result['galery_number']
        result_all['global_i'] = result['global_i']
        result_all['global_i_i'] = result['global_i_i']

        for _ in range(4):
            s.pop(0)

        result = pr_quiz5(
            "\n".join(s[:2]), result_all['galery_number'], result_all["global_i"], result_all["global_i_i"])

        result_all['s'] += result['s']
        result_all['galery_number'] = result['galery_number']
        result_all['global_i'] = result['global_i']
        result_all['global_i_i'] = result['global_i_i']

        for _ in range(2):
            s.pop(0)
    s: str = result_all['s']
    s = s.replace('<div class="audio-tts',
                  '<br>\n<div class="audio-tts')
    s = s.replace("<div class='audio-tts",
                  "<br>\n<div class='audio-tts")

    # while "id='task'" in s:
    #     s = srez_v2(s, "id=\'task\'>", "</p>")
    #     s = s.replace("id='task'", "id=\"task\"", 1)

    s = s.replace('<br>\n<div class="audio-tts',
                  '<div class="audio-tts', 1)
    s = s.replace("<br>\n<div class='audio-tts",
                  "<div class='audio-tts", 1)

    result_all['s'] = s
    return JsonResponse(result_all)


def textAudio(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_textAudio(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def dropdownQuiz(request: HttpRequest):
    s = request.GET.get('s').replace("‘", "'").replace("’", "'")
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))

    result = pr_dropdownQuiz(s, galery_number, global_i, global_i_i)
    return JsonResponse(result)


def start_view(request: HttpRequest):  # , galery_number, global_i, global_i_i
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))
    result = start(galery_number, global_i, global_i_i)
    return JsonResponse(result)


def nextslide_view(request: HttpRequest):  # , galery_number, global_i, global_i_i
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))
    result = nextslide(galery_number, global_i, global_i_i)
    return JsonResponse(result)


def end_view(request: HttpRequest):  # , ifNextBtn,  galery_number, global_i, global_i_i
    ifNextBtn = request.GET.get('ifNextBtn')
    galery_number = int(request.GET.get('galery_number'))
    global_i = int(request.GET.get('global_i'))
    global_i_i = int(request.GET.get('global_i_i'))
    result = end(ifNextBtn, galery_number, global_i, global_i_i)
    return JsonResponse(result)
