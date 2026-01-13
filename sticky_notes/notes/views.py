from django.shortcuts import render, get_object_or_404, redirect
from .models import Note
from .forms import NoteForm


def note_list(request):
    """
    Displays a list of all sticky notes ordered by creation date.
    """
    notes = Note.objects.order_by("-created_at")
    return render(request, "notes/note_list.html", {"notes": notes})


def note_detail(request, pk):
    """
    Displays the details of a single sticky note.
    """
    note = get_object_or_404(Note, pk=pk)
    return render(request, "notes/note_detail.html", {"note": note})


def note_create(request):
    """
    Handles the creation of a new sticky note.
    """
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("note_list")
    else:
        form = NoteForm()

    return render(
        request,
        "notes/note_form.html",
        {"form": form, "mode": "Create"},
    )


def note_update(request, pk):
    """
    Handles updating an existing sticky note.
    """
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect("note_detail", pk=note.pk)
    else:
        form = NoteForm(instance=note)

    return render(
        request,
        "notes/note_form.html",
        {"form": form, "mode": "Update"},
    )


def note_delete(request, pk):
    """
    Handles deletion of a sticky note after confirmation.
    """
    note = get_object_or_404(Note, pk=pk)

    if request.method == "POST":
        note.delete()
        return redirect("note_list")

    return render(
        request,
        "notes/note_confirm_delete.html",
        {"note": note},
    )
