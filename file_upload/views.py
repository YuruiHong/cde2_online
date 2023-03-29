import os
import uuid
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat
from django.shortcuts import render, redirect
from .models import File
from .forms import FileUploadForm, FileUploadModelForm, allowed_ext
from file_project import settings
from .worker import worker

# Create your views here.


# Show file list
def file_list(request, page_num=1, page_size=5, paginator_width=4):
    objects = File.objects
    description = request.GET.get('description')
    contributor = request.GET.get('contributor')
    page_num = request.GET.get('page_num') or page_num
    filtered_records = objects.order_by('-id')
    context = {
                'paginator_width': paginator_width,
                'filter_description': description,
                'filter_contributor': contributor,
              }
    if description and description != 'None':
        filtered_records = filtered_records.filter(
            description__icontains=description)
    if contributor and contributor != 'None':
        filtered_records = filtered_records.filter(
            contributor__icontains=contributor)

    # paginator
    context['page_count'] = (filtered_records.count() - 1) // page_size + 1
    context['paginator'] = Paginator(filtered_records, page_size)
    context['page'] = context['paginator'].page(page_num)

    return render(request, 'file_upload/file_list.html', context)


# Regular file upload without using ModelForm
def file_upload(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            new_file = File()
            new_file.file = handle_uploaded_file(form.cleaned_data.get("file"))
            new_file.description = form.cleaned_data.get("description")
            new_file.contributor = form.cleaned_data.get("contributor")
            new_file.save()
            return redirect("/file/")
    else:
        form = FileUploadForm()

    return render(request, 'file_upload/upload_form.html',
                  {'form': form, 'heading': 'Upload files with Regular Form'})


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

    return render(request, 'file_upload/upload_form.html',
                  {'form': form, 'heading': 'Upload files with ModelForm'})


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
            files = File.objects.all().order_by('-uploaded_at')
            worker(settings.BASE_DIR+files[0].file.url)
            data = []
            for file in files:
                data.append({
                    "url": file.file.url,
                    "description": file.description,
                    "attributes": file.attributes,
                    "size": filesizeformat(file.file.size),
                    "contributor": file.contributor,
                    })
            return JsonResponse(data, safe=False)
        else:
            data = {'error_msg': "Only these file formats are allowed: "
                    + ", ".join(allowed_ext) + "."}
            return JsonResponse(data)
    return JsonResponse({'error_msg': 'only POST method accpeted.'})
