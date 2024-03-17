from django.shortcuts import render
from django.http import JsonResponse
from django.apps import apps
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .models import BackgroundTasks,Response
import datetime , random
import subprocess

# Create your views here.
current_date = datetime.date.today()


def check_database():
    try:
        #print(custom_condition())
        # if custom_condition():    
            with apps.app_context():
                subprocess.Popen(["python3", "apollo-flow-final.py"])
    except Exception as e:
        print(e)



def home(request):
    return render(request, "home.html")

@csrf_exempt  # Use this decorator for testing purposes only

def process_form(request):
    if request.method == "POST":
        domain_input = request.POST.get('domain')
        keyword = request.POST.get("keyword")

        existing_record = get_response_record(domain_input, keyword)
        if len(existing_record) > 1:  
            print(existing_record)
            task_id = existing_record["background_task_id"]
            return redirect("downloadData", task_id=task_id)
            #  return render_template('show-results.html',msg='exists',data=existing_record)
        else:
            # also need to assign a batch
            domains_list = domain_input.replace(',',' ').split()
            domains_list = [domain.split("//")[-1] for domain in domains_list]
            #print(len(domains_list))
            
            #below is for a multiple domain 
            if len(domains_list) > 1:
                print("Adding multiple domains")
                batch_id = random.randint(0,99999)
                for domain in domains_list:
                    print("list of domains in the new code")
                    print(domain)
                    try:
                        background_task = BackgroundTasks(domain_name=domain,keyword=keyword,state='test',date=current_date)
                        background_task.save()
                        print(batch_id,": batch id")
                        print("domain")
                    except Exception as e:
                        print(f"Error in inseting into database: {str(e)}")
                        #msg = "error"
            else:
                try:
                    print("added a single domain ")
                    domain = domains_list[0]
                    print(domain)
                    background_task = BackgroundTasks(domain_name=domain,keyword=keyword,state='test',date=current_date)
                    background_task.save()
                except Exception as e:
                    print(e)
             
            return redirect("/")

    
def get_response_record(domain,keyword):
    try:
        responses = Response.objects.filter(Q(keyword='') & Q(domain_name=''))
        print(responses)
    except Exception as e:
        return e
    return responses