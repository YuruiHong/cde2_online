from django.shortcuts import render, redirect
from . import models
from .forms import FileUploadForm, FileUploadModelForm, allowed_ext
import os
import uuid
import subprocess
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat
from file_project import settings

# Create your views here.


# Show file list
def file_list(request):
    files = models.File.objects.all().order_by("-id")
    return render(request, 'file_upload/file_list.html', {'files': files})


# Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            new_file = models.File()
            new_file.file = handle_uploaded_file(form.cleaned_data.get("file"))
            new_file.description = form.cleaned_data.get("description")
            new_file.contributor = form.cleaned_data.get("contributor")
            new_file.save()
            return redirect("/file/")
    else:
        form = FileUploadForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with Regular Form'})


def handle_uploaded_file(file):
    while True:
        dir_name = uuid.uuid4().hex[:10]
        dir_path = os.path.join(settings.MEDIA_ROOT, 'files', dir_name)
        if not os.exists(dir_path):
            os.makedirs(dir_path)
            file_path = os.path.join('files', dir_name, file.name)
            absolute_file_path = os.path.join(dir_path, file.name)
            with open(absolute_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            return file_path


# Upload File with ModelForm
def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/file/")
    else:
        form = FileUploadModelForm()

    return render(request, 'file_upload/upload_form.html', {'form': form,
                                                            'heading': 'Upload files with ModelForm'})


# Upload File with ModelForm
def ajax_form_upload(request):
    form = FileUploadModelForm()
    return render(request, 'file_upload/ajax_upload_form.html',
                  {'form': form, 'heading': 'Upload Your File'})


# handling AJAX requests
def ajax_upload(request):
    if request.method == "POST":
        # 1. Regular save method
        # upload_method = request.POST.get("upload_method")
        # raw_file = request.FILES.get("file")
        # new_file = File()
        # new_file.file = handle_uploaded_file(raw_file)
        # new_file.upload_method = upload_method
        # new_file.save()

        # 2. Use ModelForm als ok.
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Obtain the latest file list
            files = models.File.objects.all().order_by('-id')
            data = []
            for file in files:
                data.append({
                    "url": file.file.url,
                    "description": file.description,
                    "size": filesizeformat(file.file.size),
                    "contributor": file.contributor,
                    })
            subprocess.call(["xdg-open", settings.BASE_DIR+file.file.url])
            return JsonResponse(data, safe=False)
        else:
            data = {'error_msg': "Only these file formats are allowed: " + ", ".join(allowed_ext) + "."}
            return JsonResponse(data)
    return JsonResponse({'error_msg': 'only POST method accpeted.'})
