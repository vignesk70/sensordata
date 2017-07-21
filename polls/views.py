# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.db.models import Count
from django.db.models.functions import TruncDay
from .models import Question,Choice,SensorData
from django.shortcuts import get_object_or_404,render
from graphos.sources.model import ModelDataSource
import datetime

from picamera import PiCamera
from time import sleep


# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

		
def dispcam(request):
	myname=''
	camera = PiCamera()
	q = SensorData.objects.all()
	camera.rotation = 180
	#picpath='/home/pi/Desktop/image.jpg'
	picpath='/var/www/media/image.jpg'
	sleep(2)
	camera.capture(picpath)
	camera.close()
	sensor = SensorData.objects.create(sensor_name='Imagecapture',sensor_data='image',create_date=datetime.datetime.now())
	sensor.save()
#	senscount=SensorData.objects.all().annotate(date=TruncDay('create_date')).values("date").annotate(countsens=Count('id')).order_by('create_date')
#	sensorcnt
#charplot	
	queryset = q
	data_source = ModelDataSource(queryset,
                                  fields=['create_date', 'sensor_name'])
	from graphos.renderers import flot
	chart = flot.LineChart(data_source)
	
#chartplot							  
								  
	context ={
		'myname':q, 
		'chart':chart,
	} 
	return render(request,'polls/dispcam.html',context)
	
def simple(request):
    import random
    import django
    import datetime
    
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from matplotlib.dates import DateFormatter

    fig=Figure()
    ax=fig.add_subplot(111)
    x=[]
    y=[]
    now=datetime.datetime.now()
    delta=datetime.timedelta(days=1)
    for i in range(10):
        x.append(now)
        now+=delta
        y.append(random.randint(0, 1000))
    ax.plot_date(x, y, '-')
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    canvas=FigureCanvas(fig)
    response=django.http.HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response
