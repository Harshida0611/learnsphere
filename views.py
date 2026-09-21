from django.shortcuts import render,redirect
from .models import Announcement
from .forms import AnnouncementForm

def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('announcement_list')  # Redirect to the announcement list after creation
    else:
        form = AnnouncementForm()

    return render(request, 'announcements/create_announcement.html', {'form': form})
def announcement_list(request):
    # Fetch all announcements, ordered by the most recent
    announcements = Announcement.objects.all()
    return render(request, 'announcements/announcement_list.html', {'announcements': announcements})
