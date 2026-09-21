from django.contrib import admin

# Register your models here.
# admin.py
from django.contrib import admin
from .models import Assignment

class AssignmentAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('title', 'due_date', 'is_completed', 'pdf_file_link')

    # Fields to filter in the admin interface
    list_filter = ('is_completed', 'due_date')

    # Fields to search in the admin interface
    search_fields = ('title', 'description')

    # Ordering the assignments in the admin
    ordering = ('due_date',)

    # Custom method to display PDF link in the admin
    def pdf_file_link(self, obj):
        if obj.pdf_file:
            return f'<a href="{obj.pdf_file.url}" target="_blank">View PDF</a>'
        return 'No PDF'

    pdf_file_link.allow_tags = True  # Enable HTML rendering (allow <a> tags)
    pdf_file_link.short_description = 'PDF File'  # Column title for the PDF field

    # Optional: Custom form for displaying fields
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'due_date', 'is_completed', 'pdf_file')
        }),
    )

# Register the model with the custom admin class
admin.site.register(Assignment, AssignmentAdmin)
