from django.shortcuts import render
from .models import Bookmark, PersonalBookmark
from .forms import BookmarkForm
from django.http import Http404


# Create your views here.
def index(request):
    # import pdb; pdb.set_trace()

    if request.method == 'POST':
        form = BookmarkForm(request.POST)
        if form.is_valid():
            # TODO check for request.user to allow for personal bookmarks
            form.save()
        else:
            # Http404(str(form.errors)) to show errors,
            # or make a context and print it
            raise Http404('Error saving bookmark')

    context = {}

    pbid = PersonalBookmark.objects.values_list('id')
    context['bookmarks'] = Bookmark.objects.exclude(id__in=pbid)

    if request.user.is_anonymous:
        context['personal_bookmarks'] = PersonalBookmark.objects.none()
    else:
        context['personal_bookmarks'] = PersonalBookmark.objects.filter(
            user=request.user)  # noqa E501

    context['form'] = BookmarkForm

    return render(request, 'bookmark/index.html', context)
