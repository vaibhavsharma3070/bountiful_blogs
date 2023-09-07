from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.core import serializers

# Create your views here.


def index(request):
    if request.method == "POST":
        openai_key = request.POST.get('openai_key')
        envato_key = request.POST.get('envato_key')
        min_image = request.POST.get('min_image')
        max_size = request.POST.get('max_size')
        search_tags = request.POST.get('search_tags')
        h2_start_from = request.POST.get('h2_start_from')
        api_delay = request.POST.get('api_delay')
        image_width = request.POST.get('image_width')
        block_quote_per_article = request.POST.get('block_quote_per_article')
        bolded_quote_per_article = request.POST.get('bolded_quote_per_article')
        image_prompt = request.POST.get('image_prompt')
        block_quote = request.POST.get('block_quote')

        if Settings.objects.filter(created_by=request.user).exists():
            settings_obj = Settings.objects.get(created_by=request.user)
            if openai_key != settings_obj.openai_key:
                settings_obj.openai_key = openai_key
            if envato_key != settings_obj.envato_key:
                settings_obj.envato_key = envato_key
            if min_image != settings_obj.min_image:
                settings_obj.min_image = min_image
            if max_size != settings_obj.max_size:
                settings_obj.max_size = max_size
            if search_tags != settings_obj.search_tags:
                settings_obj.search_tags = search_tags
            if h2_start_from != settings_obj.h2_start_from:
                settings_obj.h2_start_from = h2_start_from
            if api_delay != settings_obj.api_delay:
                settings_obj.api_delay = api_delay
            if image_width != settings_obj.image_width:
                settings_obj.image_width = image_width
            if block_quote_per_article != settings_obj.block_quote_per_article:
                settings_obj.block_quote_per_article = block_quote_per_article
            if bolded_quote_per_article != settings_obj.bolded_quote_per_article:
                settings_obj.bolded_quote_per_article = bolded_quote_per_article
            if image_prompt != settings_obj.image_prompt:
                settings_obj.image_prompt = image_prompt
            if block_quote != settings_obj.block_quote:
                settings_obj.block_quote = block_quote
            settings_obj.save()
        else:
            Settings.objects.create(
                created_by=request.user,
                openai_key=openai_key,
                envato_key=envato_key,
                min_image=min_image,
                max_size=max_size,
                search_tags=search_tags,
                h2_start_from=h2_start_from,
                api_delay=api_delay,
                image_width=image_width,
                block_quote_per_article=block_quote_per_article,
                bolded_quote_per_article=bolded_quote_per_article,
                image_prompt=image_prompt,
                block_quote=block_quote,
            )
    try:
        settings_data = Settings.objects.get(created_by=request.user)
    except Exception as err:
        print(err)
        settings_data = None
    return render(request, "settings.html", {'settings_data': settings_data})


def create_project(request):
    """create project"""
    if request.method == "POST":
        print("yess--------------->")
        name = request.POST['project_name']
        url = request.POST['project_url']
        image_folder = request.POST.get('image_folder')
        image_website = request.POST.get('image_website')

        Project.objects.create(
            created_by=request.user,
            name=name,
            url=url,
            image_folder=image_folder,
            image_website=image_website
        )

    projects_data = Project.objects.filter(created_by=request.user)
    return render(request, "project_manager.html", {"project_data": projects_data})


def projects(request):
    """get projects"""
    projects_data = Project.objects.filter(created_by=request.user)
    return render(request, "project_manager.html", {"project_data": projects_data})


def select_project(request, pk):
    """select projects"""
    if Project.objects.filter(id=int(pk)).exists():
        project_obj = Project.objects.get(id=int(pk))
        return JsonResponse(serializers.serialize('python', [project_obj,])[0]['fields'], safe=False)
    return JsonResponse({"error": "Something went wrong!"})


def delete_project(request, pk):
    """delete projects"""
    if Project.objects.filter(id=int(pk)).exists():
        project_obj = Project.objects.get(id=int(pk))
        project_obj.delete()
    return redirect("projects")


def articles(request):
    """get articles"""
    articles_data = Article.objects.filter(created_by=request.user)
    return render(request, "articles.html", {"articles_data": articles_data})
