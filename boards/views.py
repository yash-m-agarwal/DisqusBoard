from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404
from .models import Board, Topic, Post

# Create your views here.
def home(request):
    all_boards = Board.objects.all()
    return render(request, 'home.html', {'boards': all_boards})

def board_topics(request, pk):
    try:
        boardObj = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404

    return render(request, 'topics.html', {'board': boardObj})

def new_topic(request, pk):
    boardObj = get_object_or_404(Board, pk=pk)

    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']

        user = User.objects.first()

        topic = Topic.objects.create(
            subject=subject,
            board=boardObj,
            starter=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )
        return redirect('board_topics', pk=boardObj.pk)

    return render(request, 'new_topic.html', {'board':boardObj})
