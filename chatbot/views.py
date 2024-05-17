from django.shortcuts import render, redirect
from django.http import JsonResponse
from openai import OpenAI, RateLimitError, OpenAIError


from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
# Create your views here.

client = OpenAI(
    api_key ="api_key",
)

def ask_openai(user_input):
    try:
        response = client.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = [
                {
                    "role": "user", "content": user_input,
                }
            ]
        )
        answer = response.choices[0].message.content
        return answer
    except RateLimitError:
        return "Sorry, you have exceeded the API rate limit. Please try again later."
    except OpenAIError as e:
            return f"An error occurred: {e}"
 
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
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password=password)
        if user is not None:
            auth.login(request, user) # log the user in 
            return redirect('chatbot')
        else:
            error_message = 'Username or password invalid'
            return (request, 'login.html',{'error_message': error_message} )

    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username =request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            try:
                user =  User.objects.create_user(username = username, email = email, password = password1)
                user.save()
                auth.login(request, user) # log the user at this point
                return redirect('chatbot')
            except Exception as e:
                error_message = f'Error when creating the account: {str(e)}'
        else:
            error_message = "Passwords don't match"
        return render(request, 'register.html', {'error_message': error_message})
            
    return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

