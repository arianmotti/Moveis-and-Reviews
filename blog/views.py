from django import forms
from django.shortcuts import render, redirect
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm.translate import translate
from ibm_watson import LanguageTranslatorV3
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import SpeechToTextV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions

from blog.models import Comment, Movie
from tamrin1 import settings

authenticator = IAMAuthenticator('2H1f_ii0-yCICSbDR5sy69Ak8zBTUTeKAJoXQwblve8Y')
speech_to_text = SpeechToTextV1(
    authenticator=authenticator
)

nlu_authenticator = IAMAuthenticator('5hBy5Euj2pSS5qLPW6EzcQ1oIUT2HjAZnI3hAT79TSjb')
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=nlu_authenticator
)

authenticator = IAMAuthenticator('4i2GyTr13_V5E6NcQOM29RvBDpPtUu1gIL-CvqYG8yZt')
language_translator = LanguageTranslatorV3(
    version='2018-05-01',
    authenticator=authenticator
)

natural_language_understanding.set_service_url(
    'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/')
speech_to_text.set_service_url('https://api.au-syd.speech-to-text.watson.cloud.ibm.com/')
language_translator.set_service_url('https://api.au-syd.language-translator.watson.cloud.ibm.com/')


class CommentForm(forms.Form):
    voice = forms.FileField(label='voice')
    author = forms.TextInput()


class GetCommentForm(forms.Form):
    lang = forms.CharField(widget=forms.Select(choices=[('en', "en"), ('ru', "ru"), ('fr', "fr"), ('zh', "zh")]))


def add_comment(request, movie_id):
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            print(form)
            f = request.FILES['voice']
            path = settings.BASE_DIR.joinpath(f.name)
            with open(path, 'wb+') as destination:
                destination.write(f.read())
            item = speech_to_text.recognize(
                audio=request.FILES['voice'],
                content_type='audio/ogg',
                timestamps=True,
                word_confidence=True).get_result()
            text = item['results'][0]['alternatives'][0]['transcript']
            response = natural_language_understanding.analyze(
                text=text,
                features=Features(emotion=EmotionOptions())).get_result()
            anger = response['emotion']['document']['emotion']['anger']
            if anger > 0.5:
                print('stay calm body!')
            else:
                text = f'{text}'
                Comment(voice=request.FILES['voice'], text=text, author='arian',
                        movie=Movie.objects.get(id=movie_id)).save()
            return redirect('/home')
        else:
            return redirect('/home')
    else:
        return {"message": "bad request"}


def home(request):
    movies = Movie.objects.all()
    form = CommentForm()
    comments = GetCommentForm()

    return render(request, 'blog/home.html', {'movies': movies, 'form': form, 'comments': comments})


def get_comments(request, movie_id):
    form = GetCommentForm(request.GET, request.FILES)
    lang = 'en'
    if form.is_valid():
        lang = request.GET["lang"]

    comments = Movie.objects.get(id=movie_id).comments.all()
    if lang != 'en':
        for cm in comments:
            text: str = cm.text
            if text.startswith('WARNING!:'):
                pass
            else:
                translation = language_translator.translate(
                    text=text, source='en', target=lang).get_result()
                print(text, lang, translation)
                cm.text = translation['translations'][0]['translation']
    return render(request, 'blog/comments.html', {
        'comments': comments,
        'form': form,
        'movie': Movie.objects.get(id=movie_id)

    })
