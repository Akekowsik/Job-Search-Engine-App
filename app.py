from flask import Flask, redirect,render_template,request,url_for,redirect
import requests 
from bs4 import BeautifulSoup
#from gtts import gTTS
from playsound import playsound


app = Flask(__name__)

UPLOAD_FOLDER = 'static'

app.config['UPLOAD_FOLDER'] = 'UPLOAD FOLDER'

#my_text = 'Welcome to Job Search!'
#myobj = gTTS(text = my_text,lang = 'en',slow = False)
#myobj.save("welcome.mp3")

#my_text = 'All Job Offers in your intersted skill are'
#myobj = gTTS(text = my_text,lang = 'en',slow = False)
#myobj.save("offers.mp3")

@app.route('/',methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        sk = request.form['skill']
        playsound('./static/offers.mp3')
        return redirect(url_for('search',req = sk))
    else:
        
        playsound('./static/welcome.mp3')
        return render_template('open.html')

@app.route('/search/<req>',methods=['GET'])

def search(req):

    html_text = requests.get(f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={req}&txtLocation=').text
    soup = BeautifulSoup(html_text ,'lxml')

    jobs = soup.find_all('li',class_='clearfix job-bx wht-shd-bx')
    jobs_data = []

    for job in jobs :
        
        company_name = job.find('h3', class_ ='joblist-comp-name').text.replace('(More Jobs)','')
        job_role = job.find('h2').text.replace(' ','')
        total_skills_required_including_your_skill = job.find('span', class_ = 'srp-skills').text.replace(' ','')
        time_since_posted = job.find('span', class_ = 'sim-posted').text
        more_info = job.header.h2.a['href']

        job_desc = dict()
        job_desc["Company Name"] = company_name.strip()
        job_desc["Job_Role"] = job_role.strip()
        job_desc["Remaining Skills Required"] = ', '.join(list(total_skills_required_including_your_skill.strip().split(',')))
        job_desc["Time Since Posted"] = time_since_posted.strip()
        job_desc["More_Info"] = more_info
        jobs_data.append(job_desc)

    return render_template('stats.html',data = jobs_data)


if __name__ == "__main__" :
    
    app.run()
