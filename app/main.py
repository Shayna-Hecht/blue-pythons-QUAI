# Run by typing python3 main.py

# **IMPORTANT:** only collaborators on the project where you run
# this can access this web server!

"""
    Bonus points if you want to have internship at AI Camp
    1. How can we save what user built? And if we can save them, like allow them to publish, can we load the saved results back on the home page? 
    cookies
    2. Can you add a button for each generated item at the frontend to just allow that item to be added to the story that the user is building? 
    yes
    3. What other features you'd like to develop to help AI write better with a user? 
    use github copilot
    4. How to speed up the model run? Quantize the model? Using a GPU to run the model? 
    use a gpu + download more ram
"""

# import basics
import os

# import stuff for our web server
from flask import Flask, request, redirect, url_for, render_template, session
#from utils import get_base_url
# import stuff for our models
from aitextgen import aitextgen

import json
import os

def get_base_url(port:int) -> str:
    '''
    Returns the base URL to the webserver if available.
    
    i.e. if the webserver is running on coding.ai-camp.org port 12345, then the base url is '/<your project id>/port/12345/'
    
    Inputs: port (int) - the port number of the webserver
    Outputs: base_url (str) - the base url to the webserver
    '''
    
    try:
        info = json.load(open(os.path.join(os.environ['HOME'], '.smc', 'info.json'), 'r'))
        project_id = info['project_id']
        base_url = f'/{project_id}/port/{port}/'
    except Exception as e:
        print(f'Server is probably running in production, so a base url does not apply: \n{e}')
        base_url = '/'
    return base_url
    
    
#function to add correct and or comma
def and_syntax(alist):
    if len(alist) == 1:
        alist = "".join(alist)
        return alist
    elif len(alist) == 2:
        alist = " and ".join(alist)
        return alist
    elif len(alist) > 2:
        alist[-1] = "and " + alist[-1]
        alist = ", ".join(alist)
        return alist
    else:
        return

# load up a model from memory. Note you may not need all of these options.
# ai = aitextgen(model_folder="model/",
#                tokenizer_file="model/aitextgen.tokenizer.json", to_gpu=False)

ai = aitextgen(model_folder="model/", to_gpu=False)

# setup the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)


# if the base url is not empty, then the server is running in development, and we need to specify the static folder so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url+'static')

app.secret_key = os.urandom(64)

# set up the routes and logic for the webserver


@app.route(f'{base_url}')
def home():
    return render_template('/cashews-website/index.html', generated=" ")

@app.route(f'{base_url}/about/')
def about():
    return render_template('/cashews-website/about.html', generated=None)

@app.route(f'{base_url}/faq/')
def faq():
    return render_template('/cashews-website/faq.html', generated=None)

@app.route(f'{base_url}/blog-home/')
def blog_home():
    return render_template('/cashews-website/blog-home.html', generated=None)

@app.route(f'{base_url}/blog-post/')
def blog_post():
    return render_template('/cashews-website/blog-post.html', generated=None)

@app.route(f'{base_url}/pricing/')
def pricing():
    return render_template('/cashews-website/pricing.html', generated=None)

@app.route(f'{base_url}/contact/')
def contact():
    return render_template('/cashews-website/contact.html', generated=None)

@app.route(f'{base_url}/portfolio-overview/')
def portfolio_overview():
    return render_template('/cashews-website/portfolio-overview.html', generated=None)

@app.route(f'{base_url}/portfolio-item/')
def portfolio_item():
    return render_template('/cashews-website/portfolio-item.html', generated=None)

@app.route(f'{base_url}', methods=['POST'])
def home_post():
    return redirect(url_for('results'))


@app.route(f'{base_url}/results/')
def results():
    if 'data' in session:
        data = session['data']
        splitted = data.split("<!@#$>")
        query, generated = splitted[0], splitted[1]
        if "?" in generated:
            generated = generated.split("?")[0] + "?"
        print(data)
        print(generated)
        return render_template('/cashews-website/index.html', query = query, generated=generated)
    else:
        return render_template('/cashews-website/index.html', query = " ", generated=" ")


@app.route(f'{base_url}/generate_text/', methods=["POST"])
def generate_text():
    """
    view function that will return json response for generated text. 
    """

    prompt = request.form['prompt']
    if prompt is not None:
        generated = ai.generate(
            n=1,
            batch_size=1,
            prompt=str(prompt) + " <!@#$> ",
            max_length=30,
            temperature=0.9,
            return_as_list=True
        )

    data = {'generated_ls': generated}
    session['data'] = generated[0]
    return redirect(url_for('results'))


if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'cocalc23.ai-camp.dev'

    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
