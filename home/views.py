from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.core import serializers
import re
import openai
import os
from django.core.files.base import ContentFile
import requests
import itertools
from django.contrib.auth.decorators import login_required


def read_data(data):
    data = data.decode('utf-8')
    header = re.findall(r'@.+', data)
    output_dict = {
        'Header': header
    }

    lines = data.splitlines()
    key = ""
    value = ""

    for index, element in enumerate(lines):
        if element:
            if element[0] != "@":
                if element[0] == "#":
                    key = element
                else:
                    value += element+"\n"
                    if index == len(lines) - 1:
                        output_dict[key] = [value]
                        key = ""
                        value = ""
                    else:
                        if lines[index+1] != "":
                            if lines[index+1] == "#":
                                output_dict[key] = [value]
                                key = ""
                                value = ""
                        else:
                            try:
                                if lines[index+2][0] == "#":
                                    output_dict[key] = [value]
                                    key = ""
                                    value = ""
                            except IndexError:
                                output_dict[key] = [value]
                                key = ""
                                value = ""
    return output_dict


def chat_with_gpt(prompt, api_key):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=prompt,
        api_key=api_key
    )
    return response['choices']


def search_phrases(content, api_key, n):
    prompt = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt.append({"role": "user", "content": f" {content} For the provided section of text, what illustrative scene or symbolic image best captures a central theme or emotional undertone? Return your answer as a four-word search phrase. Avoid names of conditions and brands. A couple of good examples are 'boy sits at desk' and 'plate of healthy food':"})
    if n > 1:
        res = ""
        for i in range(n):
            res += f'({chat_with_gpt(prompt,api_key)[0]["message"]["content"][1:-1]})\t'
        return [res+"\n"]
    return [(f'({chat_with_gpt(prompt,api_key)[0]["message"]["content"][1:-1]})\n')]


def bold_word(content, api_key):
    prompt = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt.append({"role": "user", "content": f" {content} Please check the given paraghraph and bold up only 1 word which is most important. The original paraghraph will be provided with the bold keywords for easy identification."})
    response = chat_with_gpt(prompt, api_key)[0]["message"]["content"]
    return response


def quote_word(content, api_key):
    prompt = [{"role": "system", "content": "You are a helpful assistant."}]
    prompt.append({"role": "user", "content": f" {content} Please check the given paragraph and quote only one word. Please do not quote word which is already bold. Then provide me only the entire paragraph with the quoted word."})
    response = chat_with_gpt(prompt, api_key)[0]["message"]["content"]  
    return response


def phrase_to_image(api_key, search_phrase):
    # Define the endpoint URL and query parameters
    endpoint = f'https://api.pexels.com/v1/search'
    per_page = 1

    # Define headers with your Pexels API key
    headers = {
        'Authorization': api_key,
    }

    # Define the query parameters as a dictionary
    params = {
        'query': search_phrase,
        'per_page': per_page,
    }

    try:
        # Send a GET request with the headers and parameters
        response = requests.get(endpoint, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()  # Parse the JSON response
            for i in data['photos']:
                search_phrase = search_phrase[0].strip("[]'\n")
                return [(f'<center><img src={i["src"]["original"]} alt="{search_phrase[1:-1]}" width="766"></center>\n')]

        else:
            print(f'Error: {response.status_code}')
    except Exception as e:
        print(f'Error: {str(e)}')

@login_required
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

@login_required
def create_project(request):
    """create project"""
    if request.method == "POST":
        name = request.POST['project_name']
        url = request.POST['project_url']
        image_folder = request.FILES.getlist('image_folder[]')
        image_website = request.POST.get('image_website')

        proj_obj = Project.objects.create(
            created_by=request.user,
            name=name,
            url=url,
            image_website=image_website
        )

        for i in image_folder:
            ProjectImages.objects.create(
                parent_model=proj_obj,
                image=i
            )

    projects_data = Project.objects.filter(created_by=request.user)
    return render(request, "project_manager.html", {"project_data": projects_data})

@login_required
def projects(request):
    """get projects"""
    projects_data = Project.objects.filter(created_by=request.user)
    return render(request, "project_manager.html", {"project_data": projects_data})

@login_required
def select_project(request, pk):
    """select projects"""
    if Project.objects.filter(id=int(pk)).exists():
        project_obj = Project.objects.get(id=int(pk))
        result = serializers.serialize('python', [project_obj,])[0]['fields']
        # print(type(result))
        # result['images'] = serializers.serialize('python', [project_obj.get_images()])[0]['fields']
        # print(type(result), result)
        return JsonResponse(result, safe=False)
    return JsonResponse({"error": "Something went wrong!"})

@login_required
def delete_project(request, pk):
    """delete projects"""
    if Project.objects.filter(id=int(pk)).exists():
        project_obj = Project.objects.get(id=int(pk))
        project_obj.delete()
    return redirect("projects")

@login_required
def articles(request):
    """get articles"""
    articles_data = Article.objects.filter(created_by=request.user).order_by('-pk')
    return render(request, "articles.html", {"articles_data": articles_data})

@login_required
def upload_batch(request, pk):
    """upload batch"""
    if request.method == "POST":
        name = request.POST['batch_name']
        batch_folder = request.FILES.getlist('batch_folder[]')

        setting_obj = Settings.objects.get(created_by=request.user)
        openai_key = setting_obj.openai_key
        no_of_bold_words = getattr(setting_obj, 'bolded_quote_per_article')
        no_of_quote_words = getattr(setting_obj, 'block_quote_per_article')

        if Project.objects.filter(pk=pk).exists():
            project_obj = Project.objects.get(pk=pk)
        else:
            return JsonResponse({"error": "Something went wrong!"})

        batch_obj = Batch.objects.create(
            created_by=request.user,
            name=name,
            project=project_obj
        )

        for i in batch_folder:
            article_obj = Article.objects.create(
                created_by=request.user,
                project=project_obj,
                batch=batch_obj,
                old_article=i
            )

            # Read the file data once and avoid reading it again in the loop
            file_data = article_obj.old_article.read()
            article_obj.set_old_json(read_data(file_data))
            article_obj.save()

            temp_dict = dict()
            c = 0
            bold_count = 0
            quote_count = 0
            for i, j in article_obj.get_old_json().items():
                print("--------------->>",i,j)

                if re.match(r'^##[^#]', i):
                    if quote_count < no_of_bold_words:
                        result_value = bold_word(j[0], openai_key)
                        j[0] = result_value+"\n"
                        quote_count += 1
                    if bold_count < no_of_quote_words:
                        result_value = quote_word(j[0], openai_key)
                        j[0] = result_value+"\n"
                        bold_count += 1
                    temp_dict[i] = j
                    search_phrases_data = search_phrases(
                        j[0], openai_key, setting_obj.search_tags)
                    image_data = phrase_to_image(setting_obj.envato_key, search_phrases_data)
                    temp_dict[f"search_phrase-{c}"] = image_data
                else:
                    temp_dict[i] = j
                c += 1
            article_obj.set_new_json(temp_dict)
            article_obj.save()

            # Use os.path.join to construct the file path
            file_path = os.path.join('media', 'old_articles', f'new_file-{i}.txt')

            h2_count = setting_obj.h2_start_from
            temp_count = 1
            with open(file_path, 'w') as f:
                header_values = article_obj.get_new_json().pop("Header")
                for value in header_values:
                    f.write(value + '\n')

                items_iterable = article_obj.get_new_json().items()
                for key, values in itertools.islice(items_iterable, 1, None):
                    if re.match(r'^##[^#]', key):
                        if "search_phrase-" not in key:
                            f.write(key + '\n')
                        for value in values:
                            f.write(value + '\n')
                        temp_count += 1
                    else:
                        if h2_count < temp_count:
                            if "search_phrase-" not in key:
                                f.write(key + '\n')
                            for value in values:
                                f.write(value + '\n')
                        else:
                            if "search_phrase-" in key:
                                pass
                            else:
                                f.write(key + '\n')
                                for value in values:
                                    f.write(value + '\n')

            with open(file_path, 'r') as f:
                article_obj.new_article.save(
                    f'new_file-{i}.txt', ContentFile(f.read()))
            article_obj.save()
            
            file_path = os.path.join('media', f'{article_obj.new_article}')

        return redirect("articles")

    projects_data = Project.objects.filter(created_by=request.user)
    return render(request, "project_manager.html", {"project_data": projects_data})

@login_required
def specific_article(request):
    id = request.GET.get('id')
    if id:
        article = Article.objects.get(pk=id)
    else:
        article = Article.objects.filter(created_by=request.user).last()

    with article.new_article.open('r') as file:
        content = file.read()
    return render(request, 'specific_article.html', {'text_file': article.new_article, 'content': content})