import pdfkit
import os
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from .forms import SeatBookingForm

# ✅ Set the correct path for wkhtmltopdf
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def book_seat(request):
    if request.method == "POST":
        form = SeatBookingForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save()
            return generate_receipt(booking)  # Call function to generate & download PDF

    else:
        form = SeatBookingForm()
    
    return render(request, 'book_seat.html', {'form': form})

def generate_receipt(booking):
    """Generate and download a receipt PDF after successful booking."""
    html = render_to_string('receipt.html', {'booking': booking})

    try:
        pdf = pdfkit.from_string(html, False, configuration=config)  # Generate PDF in memory
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {e}", content_type="text/plain")

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{booking.id}.pdf"'  # Force download
    return response
