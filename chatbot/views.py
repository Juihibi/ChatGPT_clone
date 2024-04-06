from django.shortcuts import render
from django.http import JsonResponse
import openai
# Create your views here.




openai.api_key = ""
messages = [{"role": "system", "content": "You are a financial experts that specializes in real estate investment and negotiation"}]

def ask_openai(messages):
    messages.append({"role": "user", "content": messages})
    response = openai.Completion.create(
        model = "gpt-3.5-turbo",
        messages = messages,
        
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    #return ChatGPT_reply
    print(ChatGPT_reply) 
    



def chatbot(request):
    if request.method == 'POST': # the original method is GET but if we send something, in js file , we have POST
        message = request.POST.get('message')
        response = ask_openai(message)

        return JsonResponse({'message': message, 'response': response})
    return render(request, 'chatbot.html')
