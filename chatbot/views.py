from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.contrib import auth


# Create your views here.

#openai.api_key = "sk-"
messages = [{"role": "system", "content": "You are a chatGPT"}]

def ask_openai(user_input):
    messages.append({"role": "user", "content": user_input})

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    answer = response.choices[0].message.content
    return answer


    #return ChatGPT_reply
    #print(response) 
    # strip to remove all formatting of text and just return the txt



def chatbot(request):
    if request.method == 'POST': # the original method is GET but if we send something, in js file , we have POST
        message = request.POST.get('message')
        response = ask_openai(message)

        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')


def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)












