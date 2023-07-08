from django.views.generic import TemplateView, ListView
from .models import AnnouncedPuResults, Lga, PollingUnit
from django.shortcuts import render, redirect
from .forms import PollingUnitForm
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("api_key")
api_url = "https://ipgeolocation.abstractapi.com/v1/?api_key=" + api_key


class PuResult(ListView):
    model = AnnouncedPuResults
    template_name = "pu_result.html"


def result_list(request):
    results = AnnouncedPuResults.objects.all()
    return render(
        request,
        "pu_result.html",
        {
            "results": results,
        },
    )


def lga_result_list(request, id=1):
    lga = Lga.objects.get(lga_id=id)
    lga_list = Lga.objects.all()
    pus = PollingUnit.objects.filter(lga_id=id)
    results = AnnouncedPuResults.objects.all().order_by("party_abbreviation")

    return render(
        request,
        "lga_result.html",
        {
            "results": results,
            "pus": pus,
            "lga": lga,
            "lga_list": lga_list,
        },
    )


class PuDoneView(TemplateView):
    template_name = "pu_create_done.html"


def get_ip_geolocation_data(ip_address):
    # not using the incoming IP address for testing
    print(ip_address)
    response = requests.get(api_url)
    return response.content


def pu_create_view(request):
    form = PollingUnitForm(data=request.POST)

    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")

    geolocation_json = get_ip_geolocation_data(ip)
    geolocation_data = json.loads(geolocation_json)

    if form.is_valid():
        pu = form.save(commit=False)
        pu.user_ip_address = ip
        pu.lat = geolocation_data["latitude"]
        pu.long = geolocation_data["longitude"]
        pu.save()
        return redirect("pu_create_done")
    else:
        form = PollingUnitForm()

    return render(request, "pu_create.html", {"form": form})
