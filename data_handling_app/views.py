from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CandidateForm
from django.contrib import messages
import requests, os, gspread, datetime, csv
from io import BytesIO
from oauth2client.service_account import ServiceAccountCredentials
from .models import candidates

def candidate_data_process(candidate):
    cand_data_dict = {}
    cand_data_dict["timestamp"] = datetime.datetime.strptime(candidate[0], "%d/%m/%Y %H:%M:%S")
    cand_data_dict["email"] = candidate[1]
    cand_data_dict["name"] = candidate[2]
    cand_data_dict["city"] = candidate[3]
    cand_data_dict["contact_no"] = int(candidate[4])
    cand_data_dict["age"] = int(candidate[5])
    cand_data_dict["recent_company"] = candidate[6]
    cand_data_dict["job"] = candidate[7]
    cand_data_dict["current_ctc"] = candidate[8]
    cand_data_dict["fixed_component_in_ctc"] = candidate[9]
    cand_data_dict["work_experience_in_months"] = candidate[10]
    cand_data_dict["work_6_days_a_week"] = candidate[11]
    cand_data_dict["willing_to_relocate_mumbai"] = candidate[12]
    cand_data_dict["verbal_eng_skill_rate"] = int(candidate[13])
    cand_data_dict["skills_you_have_worked"] = candidate[14]
    cand_data_dict["industry_you_have_worked"] = candidate[15]
    cand_data_dict["profile_you_like_to_work"] = candidate[16]
    cand_data_dict["matters_most_while_selecting_job"] = candidate[17]
    cand_data_dict["latest_resume"] = datetime.datetime.strptime(candidate[18], "%d/%m/%Y") 
    return cand_data_dict

def check_candidate_already_exists(email_id, contact_number):
    exist_cand = candidates.objects.filter(email=email_id, contact_no=contact_number)
    return exist_cand

def home(request):
    if request.method == "POST":
        try:
            excel_file_url = "https://docs.google.com/spreadsheets/d/1TzDXLdhjrUjHo4Jj5CY5RNd-mxh1kjksuXVeQqhk3i0/edit?usp=sharing"
            scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
            DIRNAME = os.path.dirname(__file__)
            creds = ServiceAccountCredentials.from_json_keyfile_name(os.path.join(DIRNAME, "creds.json"), scope)
            client = gspread.authorize(creds)
            spread_sheet = client.open_by_url(excel_file_url)
            work_sheet = spread_sheet.get_worksheet(0) #first sheet of the spredsheet
            candidates_data = work_sheet.get_all_values()
            del candidates_data[0] #first row is a headers
            candidates_data.reverse() #reverse help to access new data first
            for candidate in candidates_data:
                cand_data_dict = candidate_data_process(candidate)
                cand_exist_or_not = check_candidate_already_exists(cand_data_dict["email"], cand_data_dict["contact_no"])
                if len(cand_exist_or_not) == 0:
                    form =  CandidateForm(cand_data_dict)
                    if form.is_valid():
                        form.save()
                else:
                    # break and skip rest of the data because there is no new updates
                    break
            messages.success(request, "SyncUP successfull!", extra_tags="home")
        except:
            messages.error(request, "Something wrong try later!", extra_tags="home")
    queryset = candidates.objects.all()
    return render(request, "home.html", {'table': queryset})


def candidates_form(request):
    if request.method == "POST":
        form = CandidateForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Details Added Successfully.", extra_tags="candidates_form")
            return redirect("candidates_form")
        else:
            messages.error(request, "Not added! Check the details.", extra_tags="candidates_form")
            return render(request, "candidates_form.html", {"form": form})
    else:
        form = CandidateForm(request.POST or None)
        return render(request, "candidates_form.html", {"form": form})
    return render(request, "candidates_form.html", {"form" : form})


def process_csv(request):
    if request.method == "GET":
        return render(request, "upload_csv.html", {})
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith(".csv"):
            messages.error(request,"This is not a .CSV file!", extra_tags="process_csv")
            return HttpResponseRedirect(reverse("upload_csv"))
        candidate_data = csv_file.read().decode("utf-8").splitlines()
        all_lines = csv.reader(candidate_data)
        next(all_lines) #first row is a headers
        for line in all_lines:
            cand_data_dict = candidate_data_process(line)
            cand_exist_or_not = check_candidate_already_exists(cand_data_dict["email"], cand_data_dict["contact_no"])
            if len(cand_exist_or_not) == 0:
                form =  CandidateForm(cand_data_dict)
                if form.is_valid():
                    form.save()
        messages.success(request,"File successfully processed !", extra_tags="process_csv")
    except:
        messages.error(request,"Something wrong try another file!", extra_tags="process_csv")
    return HttpResponseRedirect(reverse("upload_csv"))
