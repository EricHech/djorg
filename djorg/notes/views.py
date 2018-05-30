from django.shortcuts import render
from .models import Note
from .forms import NotesForm
from django.http import Http404


# Create your views here.
def index(request):
    # import pdb; pdb.set_trace()

    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            raise Http404('Error saving note')

    nid = Note.objects.values_list('id')

    context = {}
    context['notes'] = Note.objects.all()
    context['form'] = NotesForm

    return render(request, 'notes/index.html', context)
