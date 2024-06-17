from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from joblib import load

from .models import Person, Contact_info, History
from .data_conversion import conversion


covid_model = load('./main/Models/Covid.joblib')
heart_disease_model=load('./main/Models/Heart-Disease.joblib')
diabetes_model=load('./main/Models/Diabetes.joblib')
breast_cancer_model=load('./main/Models/Breast-Cancer.joblib')
low_end_model = load('./main/Models/Low_End.joblib')

def intro(request):
    return render(request, 'introduction.html')

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    user = request.user
    hist = History.objects.filter(person=user).values()
    return render(request, 'dashboard.html', conversion(hist))

def handlesignup(request):
    if request.method=='POST':
        fname=request.POST.get('fname')
        lname=request.POST.get('lname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        myuser=User.objects.create_user(username, email, pass1)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.save()
        profile=Person(username=username, email=email)
        profile.save()
        messages.success(request, "Your account has been created successfully")
        user=authenticate(username=username,password=pass1)
        if user is not None:
            login(request, user)
            # print("user is logged in")
            messages.success(request, "Logged In!")
            return redirect("intro")
        else:
            messages.error(request, "Invalid Credentials, please try again")
            return redirect("login")
    return render(request, 'signup.html')

def userlogin(request):
    if request.method=='POST':
        loginusername=request.POST['loginusername']
        loginpass=request.POST['loginpass']
        print(loginusername)
        user=authenticate(username=loginusername,password=loginpass)
        if user is not None:
            login(request, user)
            # print("user is logged in")
            messages.success(request, "Logged In!")
            return redirect("intro")
        else:
            messages.error(request, "Invalid Credentials, please try again")
            return redirect("login")
    # print("not posted in")
    return render(request, 'login.html')

def userlogout(request):
    user=request.user
    # print(f"{user} logged in is logged out")
    logout(request)
    # print("oioiiooioioio")
    messages.success(request, "Successfully logged out!")
    return redirect("intro")

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        query = request.POST['query']
        ins = Contact_info(name= name, email= email, Query= query)
        ins.save()
    return render(request, 'contact.html')

def covid(request):
    return render(request, 'covid.html')

def heart(request):
    return render(request, 'heart_disease.html')

def diabetes(request):
    return render(request, 'diabetes.html')

def Breast_cancer(request):
    return render(request, 'cancer.html')

def diabetes_result(request):
    disease = ''
    if request.method=='POST':
        gender = request.POST['gender']
        age = int(request.POST['age'])/100
        hypertension = request.POST['hypertension']
        heart_disease = request.POST['heart_disease']
        smoking = request.POST['smoking']
        current=0
        ever=0
        former=0
        never=0
        noinfo=0
        if smoking==1:
            current=1
        elif smoking==2:
            former=1
        elif smoking==0:
            never=1
        bmi = request.POST['bmi']
        hba = request.POST['hba']
        glucose = request.POST['glucose']
        features=[gender,age,hypertension, heart_disease,bmi, hba, glucose, current, ever, former, never, noinfo]
        y_pred = diabetes_model.predict([features])[0]
        diabetes_prob=diabetes_model.predict_proba([features])[0]
        prob = 0
        if y_pred==0:
            result_diabetes="You have Diabetes"
            prob = round(diabetes_prob[0]*100, 2)
            if prob>80:
                disease="We advice you to consult a doctor and get yourself checked immediately"
        
        else:
            result_diabetes="You don't have Diabetes"
            prob = round(diabetes_prob[1]*100, 2)
            if prob>80:
                disease="Congratulations! You're safe and healthy"
        resu = ''
        if(y_pred==0):
            resu = 'positive'
        else:
            resu = 'negative'
        user = request.user
        ins = History(app= "MedPred", disease="diabetes", result= resu, probability = prob, person=user)
        ins.save()
        return render(request, 'result.html',{'result':result_diabetes, 'probability': prob, 'disea':disease})

def heart_result(request):
    disease = ''
    if request.method=='POST':
        age = request.POST['age']
        age=int(age)/100
        gender=request.POST['Gender']
        chestpain = request.POST['chestpain']
        Blood_Pressure = request.POST['Blood-Pressure']
        cholesterol = request.POST['cholesterol']
        heart_rate = request.POST['heart-rate']
        angina = request.POST['angina']
        st = request.POST['st']
        thal = request.POST['thal']
        vessels = request.POST['vessels']
        array=[age, gender,chestpain, Blood_Pressure, cholesterol,0,0, heart_rate, angina, st,0, vessels,thal]
        y_pred = heart_disease_model.predict([array])[0]
        heart_prob = heart_disease_model.predict_proba([array])[0]
        prob = 0
        if y_pred==0:
            result_heart="You don't have Heart Disease"
            prob = round(heart_prob[0]*100, 2)
            if prob>80:
                disease="Congratulations! You're safe and healthy"        
        else:
            result_heart="You have Heart Disease"
            prob = round(heart_prob[1]*100, 2)
            if prob>80:
                disease="We advice you to consult a doctor and get yourself checked immediately"

        resu = ''
        if(y_pred==0):
            resu = 'positive'
        else:
            resu = 'negative'
        user = request.user
        ins = History(app= "MedPred", disease="Covid", result= resu, probability = prob, person=user)
        ins.save()
        return render(request, 'result.html',{'result':result_heart, 'probability': prob, 'disea': disease})

def cancer_result(request):
    disease = ''
    if request.method=='POST':
        texture_mean = request.POST['texture_mean']
        cell_compactness = request.POST['cell_compactness']
        worst_cell_texture_rate = request.POST['worst_cell_texture_rate']
        worst_cell_area_rate = request.POST['worst_cell_area_rate']
        worst_cell_smooth_rate=request.POST['worst_cell_smooth_rate']
        worst_cell_concavity = request.POST['worst_cell_concavity']
        worst_concave_points = request.POST['worst_concave_points']
        mean_cell_area_rate = request.POST['mean_cell_area_rate']
        predictors = [0,texture_mean,0, 0, 0, 0,0,0,0,0,0,0,0,mean_cell_area_rate,0, cell_compactness,0,0,0,0,0,0, worst_cell_texture_rate,0, worst_cell_area_rate, worst_cell_smooth_rate,0, worst_cell_concavity, worst_concave_points,0]
        y_pred = breast_cancer_model.predict([predictors])[0]
        cancer_prob = breast_cancer_model.predict_proba([predictors])[0]
        prob = 0
        if y_pred == 0:
            result_cancer="You don't have Breast Cancer"
            prob=round(cancer_prob[0]*100, 2)
            if prob>80:
                disease="Congratulations! You're safe and healthy"        
        else:
            result_cancer = "You have Breast-Cancer"
            prob = round(cancer_prob[1]*100, 2)
            if prob>80:
                disease="We advice you to consult a doctor and get yourself checked immediately"

        resu = ''
        if(y_pred==0):
            resu = 'positive'
        else:
            resu = 'negative'
        user = request.user
        ins = History(app= "MedPred", disease="Covid", result= resu, probability = prob, person=user)
        ins.save()
        return render(request, 'result.html',{'result': result_cancer, "probability": prob, 'disea':disease})

def covid_result(request):
    disease = ''
    if request.method=='POST':
        Gender = request.POST['Gender']
        age = request.POST['age']
        age = int(age)/100
        fever = request.POST['fever']
        cough = request.POST['cough']
        runnynose = request.POST['runnynose']
        musclesore = request.POST['musclesore']
        Pneumonia = request.POST['Pneumonia']
        Diarrhea = request.POST['Diarrhea']
        Lung = request.POST['Lung']
        travel = request.POST['travel']
        features =[Gender, age, fever, cough, runnynose, musclesore, Pneumonia, Diarrhea, Lung, travel,0]
        y_pred = covid_model.predict([features])[0]
        covid_prob=covid_model.predict_proba([features])[0]
        prob = 0
        if y_pred == 0:
            result_covid = "You don't have Covid-19 disease"
            prob = round(covid_prob[0]*100, 2)
            if prob>80:
                disease="Congratulations! You're safe and healthy"
        else:   
            result_covid = "You have Covid-19 disease"
            prob = round(covid_prob[1]*100, 2)
            if prob>80:
                disease="We advice you to consult a doctor and get yourself checked immediately"
        resu = ''
        if(y_pred==0):
            resu = 'positive'
        else:
            resu = 'negative'
        user = request.user
        ins = History(app= "MedPred", disease="Covid", result= resu, probability = prob, person=user)
        ins.save()
        return render(request, 'result.html', {'result' : result_covid, 'probability':prob, 'disea':disease})
    

def medscentry(request):
    return render(request, 'medScan_low.html')

def medscresults(request):
    print("ijkj")
    diseases_str = ''
    symptoms_str = ''
    treatments_str = ''

    features = [0]*132
    d = {'itching': 0, 'skin_rash': 1, 'continuous_sneezing': 3, 'shivering': 4, 'chills': 5, 'joint_pain': 6, 'vomiting': 11, 'cough': 24, 'breathlessness': 27, 'sweating': 28, 'headache': 31, 'nausea': 34, 'diarrhoea': 40, 'chest_pain': 56, 'muscle_pain': 97}

    # Disease list
    diseases = ['Fungal infection', 'Allergy', 'Drug Reaction', 'AIDS', 'Migraine',
        'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'Hepatitis A',
        'Hepatitis B', 'Common Cold', 'Pneumonia', 'Arthritis', 'Acne',
        'Impetigo', 'hepatitis A']

# Symptoms list
    symptoms = [
        ['Itchy rash', 'redness', 'peeling skin', 'burning sensation'],
        ['Sneezing', 'itching', 'watery eyes', 'nasal congestion', 'coughing'],
        ['Skin rash', 'fever', 'joint pain', 'swelling', 'shortness of breath'],
        ['Fatigue', 'weight loss', 'recurrent infections', 'night sweats', 'swollen lymph nodes'],
        ['Severe headache', 'nausea', 'sensitivity to light and sound', 'visual disturbances'],
        ['Fever', 'chills', 'sweats', 'fatigue', 'headache', 'nausea'],
        ['Rash', 'itching', 'fever', 'headache', 'loss of appetite'],
        ['High fever', 'severe headache', 'joint and muscle pain', 'rash', 'bleeding'],
        ['High fever', 'abdominal pain', 'weakness', 'headache', 'diarrhea'],
        ['Fatigue', 'nausea', 'jaundice', 'abdominal pain', 'dark urine'],
        ['Fatigue', 'abdominal pain', 'jaundice', 'joint pain', 'nausea'],
        ['Sneezing', 'runny nose', 'sore throat', 'cough', 'fatigue'],
        ['Cough', 'fever', 'difficulty breathing', 'chest pain', 'fatigue'],
        ['Joint pain', 'swelling', 'stiffness', 'redness', 'reduced range of motion'],
        ['Pimples', 'blackheads', 'whiteheads', 'redness', 'inflammation'],
        ['Red sores', 'blisters', 'itching', 'fluid-filled blisters', 'honey-colored crusts'],
        ['','','']
    ]

# Treatment list
    treatments = [
        ['Antifungal medications', 'good hygiene', 'topical creams'],
        ['Antihistamines', 'decongestants', 'allergy shots'],
        ['Discontinuation of the offending drug', 'supportive care', 'antihistamines'],
        ['Antiretroviral therapy (ART)', 'opportunistic infection treatment', 'supportive care'],
        ['Pain relievers', 'triptans', 'preventive medications', 'lifestyle changes'],
        ['Antimalarial medications', 'supportive care', 'bed rest'],
        ['Antiviral medications', 'symptomatic relief', 'calamine lotion'],
        ['Supportive care', 'fluid replacement', 'pain relievers'],
        ['Antibiotics', 'supportive care', 'rehydration therapy'],
        ['Rest', 'fluids', 'symptomatic relief', 'vaccination'],
        ['Antiviral medications', 'vaccination', 'supportive care'],
        ['Rest', 'fluids', 'symptomatic relief', 'over-the-counter medications'],
        ['Antibiotics', 'rest', 'oxygen therapy', 'supportive care'],
        ['Medications', 'physical therapy', 'lifestyle changes', 'joint injections'],
        ['Topical and oral medications', 'skincare', 'lifestyle changes'],
        ['Antibiotics', 'good hygiene', 'topical antiseptics'],
        ['','','']]

    if request.method=='POST':
        your_list = request.POST.get('symptoms')
        print(your_list)
        itching = 0
        skin_rash = 0
        continuous_sneezing=0
        shivering = 0
        joint_pain = 0
        vomiting = 0
        cough = 0
        breathlessness=0
        sweating = 0
        headache = 0
        nausea = 0
        chills = 0
        diarrhoea = 0
        chest_pain = 0
        muscle_pain =0
        stri=''
        parent_count=0
        for symptom in your_list:
            if symptom=='"':
                parent_count+=1
                print(parent_count)
                if parent_count%2==0:

                    print(f"{stri} is the symptom")
                # Set variables based on the keys where the value is 1
                    if stri == 'itching':
                        itching = 1
                    if stri == 'skin_rash':
                        skin_rash = 1
                    if stri == 'continuous_sneezing':
                        continuous_sneezing = 1
                    if stri == 'shivering':
                        shivering = 1
                    if stri == 'joint_pain':
                        joint_pain = 1
                    if stri == 'vomiting':
                        vomiting = 1
                    if stri == 'cough':
                        cough = 1
                    if stri == 'breathlessness':
                        breathlessness = 1
                    if stri == 'sweating':
                        sweating = 1
                    if stri == 'headache':
                        headache = 1
                    if stri == 'nausea':
                        nausea = 1
                    if stri == 'chills':
                        chills = 1
                    if stri == 'diarrhoea':
                        diarrhoea = 1
                    if stri == 'chest_pain':
                        chest_pain = 1
                    if stri == 'muscle_pain':
                        muscle_pain = 1
                    stri=''
            elif parent_count%2==1:
                stri+=symptom
        # print(f'itching: {itching}')
        # print(f'skin_rash: {skin_rash}')
        # print(f'continuous_sneezing: {continuous_sneezing}')
        # print(f'shivering: {shivering}')
        # print(f'joint_pain: {joint_pain}')
        # print(f'vomiting: {vomiting}')
        # print(f'cough: {cough}')
        # print(f'breathlessness: {breathlessness}')
        # print(f'sweating: {sweating}')
        # print(f'headache: {headache}')
        # print(f'nausea: {nausea}')
        # print(f'chills: {chills}')
        # print(f'diarrhoea: {diarrhoea}')
        # print(f'chest_pain: {chest_pain}')
        # print(f'muscle_pain: {muscle_pain}')

        # itching = int(request.POST['itching'])
        # skin_rash = int(request.POST['skin_rash'])
        # continuous_sneezing = int(request.POST['continuous_sneezing'])
        # shivering = int(request.POST['shivering'])
        # joint_pain = int(request.POST['joint_pain'])
        # vomiting = int(request.POST['vomiting'])
        # cough = int(request.POST['cough'])
        # breathlessness = int(request.POST['breathlessness'])
        # sweating = int(request.POST['sweating'])
        # headache = int(request.POST['headache'])
        # nausea = int(request.POST['nausea'])
        # chills = int(request.POST['chills'])
        # diarrhoea = int(request.POST['diarrhoea'])
        # chest_pain = int(request.POST['chest_pain'])
        # muscle_pain = int(request.POST['muscle_pain'])
        # print(itching, type(itching))
        features = [itching, skin_rash, 0, continuous_sneezing, shivering, chills, joint_pain, 0, 0, 0, 0, vomiting, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, cough, 0, 0, breathlessness, sweating, 0, 0, headache, 0, 0, nausea, 0, 0, 0, 0, 0, diarrhoea, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, chest_pain, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, muscle_pain, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        y_pred = low_end_model.predict([features])[0]
        index = diseases.index(y_pred)
        
        resu = 'positive'
        user = request.user
        ins = History(app= "MedScan", disease=y_pred, result= resu, probability = 100, person=user)
        ins.save()

        diseases_str = "Disease: " + y_pred
        symptoms_str = "Symptoms: " + symptoms[index][0] + ", " + symptoms[index][1] + ", " + symptoms[index][2]
        treatments_str = "Treatments: " + treatments[index][0] + ", " + treatments[index][1] + ", " + treatments[index][2]
        print(symptoms, diseases, diseases_str, treatments_str)
        return render(request, 'medScan_res.html', {'diseases_str':diseases_str, 'symptoms_str':symptoms_str,'treatments_str':treatments_str})
 
