from django.test import TestCase
from django.urls import reverse
from .models import Note


class NoteModelTest(TestCase):
    """Tests for the Note model."""

    def setUp(self):
        """Create a sample note for testing."""
        self.note = Note.objects.create(
            title="Test Note",
            content="This is a test note."
        )

    def test_note_title(self):
        """A note should store the correct title."""
        self.assertEqual(self.note.title, "Test Note")

    def test_note_content(self):
        """A note should store the correct content."""
        self.assertEqual(self.note.content, "This is a test note.")


class NoteViewTest(TestCase):
    """Tests for the notes app views."""

    def setUp(self):
        """Create a sample note for view tests."""
        self.note = Note.objects.create(
            title="Existing Note",
            content="Existing content"
        )

    def test_note_list_view(self):
        """The note list page should load and show notes."""
        response = self.client.get(reverse("note_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Note")

    def test_note_detail_view(self):
        """The note detail page should load and show the note."""
        response = self.client.get(reverse("note_detail", args=[self.note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Note")
        self.assertContains(response, "Existing content")

    def test_note_create_view_get(self):
        """The create note page should load (GET)."""
        response = self.client.get(reverse("note_create"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Create")

    def test_note_create_view_post(self):
        """Submitting the create form should create a new note (POST)."""
        response = self.client.post(
            reverse("note_create"),
            {"title": "New Note", "content": "New content"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Note.objects.filter(title="New Note").exists())

    def test_note_update_view_get(self):
        """The update note page should load (GET)."""
        response = self.client.get(reverse("note_update", args=[self.note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Update")

    def test_note_update_view_post(self):
        """Submitting the update form should update the note (POST)."""
        response = self.client.post(
            reverse("note_update", args=[self.note.pk]),
            {"title": "Updated Title", "content": "Updated content"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, "Updated Title")
        self.assertEqual(self.note.content, "Updated content")

    def test_note_delete_view_get(self):
        """The delete confirmation page should load (GET)."""
        response = self.client.get(reverse("note_delete", args=[self.note.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Delete")

    def test_note_delete_view_post(self):
        """Posting to delete should remove the note (POST)."""
        response = self.client.post(
            reverse("note_delete", args=[self.note.pk]),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Note.objects.filter(pk=self.note.pk).exists())
