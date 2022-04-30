from flask import *
import datetime
import re, random
from flask_mail import FlaskMailUnicodeDecodeError, Mail,Message

from datetime import date


# from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mlibrary865@gmail.com'
app.config['MAIL_PASSWORD'] = 'mlibrary@828'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='vidhi@30'
# app.config['MYSQL_DB']='library_management'

# mysql=MySQL(app)
email=None
@app.route("/")
def index():
    return render_template('/index.html')
user={}


@app.route("/login", methods=[ 'GET','POST'])
def login():
    if(request.method=="GET"):
        return render_template("login.html")
    if(request.method=="POST"):
        print("form submitted")
        password=request.form.get("password")
        email=request.form.get("email")
        print(email,"  ", password,"hello")
        if(email not in email_data):
                flash('No such account exists', 'error_login')
                return redirect(request.url)
        else:
            if(password==password_data[email_data.index(email)]):
                if(usertype_data[email_data.index(email)]=='admin'):
                    return redirect(url_for('admin'))
                else:
                    return redirect( url_for('student'))
            else:
                flash('Invalid password provided', 'error_password')
                return redirect(request.url)
    return render_template("login.html")

@app.route("/signup", methods=[ 'GET','POST'])
def signup():
    if(request.method=="GET"):
        return render_template("signup.html")
    if(request.method=='POST'):
        global email, USERNAME, EMAIL , PASSWORD, USERTYPE
        USERNAME=request.form.get("USERNAME")
        EMAIL=request.form.get("EMAIL")
        PASSWORD=request.form.get("PASSWORD")
        USERTYPE=request.form.get("USERTYPE")
     
        print(USERTYPE)
        email=EMAIL
        if(email in email_data):
            flash('User already exists!',"error_userexists")
            return redirect(request.url)
        global otp
        otp=random.randint(100000,999999)
        print(otp)
        print(email)
        msg = Message('Your unique verification code', sender =   'mlibrary865gmail.com', recipients = [email])
        msg.body = "Please confirm your otp. This is your unique verification code: "+str(otp)
        mail.send(msg)
        flash('message sent',"message_sent")
        
        return redirect(url_for("confirmemail"))
    return render_template("signup.html")
username_data=[]
password_data=[]
usertype_data=[]
email_data=[]

global otp

@app.route("/confirmemail", methods=[ 'GET','POST'])
def confirmemail():
    if(request.method=="GET"):
        return render_template("confirmemail.html")
    if(request.method=='POST'):
    
        return render_template("confirmemail.html")

@app.route("/confirmotp", methods=[ 'GET','POST'])
def confirmotp():
    if(request.method=='GET'):
        return render_template('confirmemail.html')
    if(request.method=='POST'):
        global otp
        global email
        OTP=request.form.get("OTP")
        print("otp: ",otp, "OTP= ",OTP)
        if(int(otp)==int(OTP)):
            otp=000000
            
            global USERNAME
            global EMAIL 
            global PASSWORD
            global USERTYPE
            username_data.append(USERNAME)
            email_data.append(EMAIL)
            password_data.append(PASSWORD)
            usertype_data.append(USERTYPE)
            email=EMAIL
        
            if USERTYPE=='admin':
                return redirect(url_for('admin'))
            else:
                return redirect(url_for('student'))
        else:
            print("wrong otp")
            flash("Wrong otp ", "error_otp")
            return redirect(request.url)                      
        
            
            

@app.route("/admin", methods=[ 'GET','POST'])
def admin():
    global email
    print(email)
    if(email==None):
        return render_template("admin.html",username=username_data[email_data.index(email)])
    else:

        return render_template("admin.html",username=username_data[email_data.index(email)])


@app.route("/student", methods=[ 'GET','POST'])
def student():
    global email
    if(email==None):
        return render_template("error.html")
    else:
        return render_template("student.html",username=username_data[email_data.index(email)])
issuebook_visited=0

@app.route('/issue', methods=[ 'GET','POST'])
def issue():
    if (request.method=='POST'):
        return render_template('issue.html',books=books)
    else:
        return('error.html')
              


flag_addbooks=0
addbook_visited=0
@app.route('/addbook', methods=[ 'GET','POST'])
def addbook():
    global addbook_visited
    if(request.method=='POST'):
        print(flag_addbooks)
        # if(flag_addbooks==1):
        global bookname,bookid
        bookname=request.form.get('bookname')
        bookid=request.form.get('bookid')
        author=request.form.get('author')
        type=request.form.get('type')
        if(bookid==None):
            return render_template('addbook.html')
        if(bookid in (books.keys())):
            print("book id exists")
            flash("Book ID already in use. Try with a new book id. See all the books in library to know the book ids alreday in use.","error_bookidexists")
            addbook_visited=1
            return redirect(request.url)
        bookfound=0
       
        books[bookid]={'author':author, 'name': bookname,'type':type,'issuedby':None,"issuedate":None,"returndate":None,"quantity":1}
        flash('Book added successfully',"book_added")
        addbook_visited=1
        return redirect(request.url)
       
         
    else:
        if(addbook_visited==1):   
            addbook_visited=0
            return render_template('addbook.html')
        else:
            return render_template('error.html')
              
deletebook_visited=0  
@app.route('/deletebook', methods=[ 'GET','POST'])
def deletebook():
    global deletebook_visited
    if(request.method=='POST'):
        
        global bookname,bookid
        bookname=request.form.get('bookname')
        bookid=request.form.get('bookid')

        if(bookid==None):
            return render_template('deletebook.html')
        print(books[bookid]," ",books[bookid]['name'])
        if(bookid not in (books.keys()) or books[bookid]['name']!=bookname):
            print("book id exists")
            flash("No such book exists in the library. You have wrong book ID or wrong Book Name","error_booknotexists")
            deletebook_visited=1
            return redirect(request.url)
       
        del books[bookid]       
      
        flash('Book deleted successfully',"book_deleted")
        deletebook_visited=1
        return redirect(request.url)
       
         
    else:
        if(deletebook_visited==1):   
            deletebook_visited=0
            return render_template('deletebook.html')
        else:
            return render_template('error.html')
              
books={}
books['211'] = {'author':"Jodi Picoult", 'name': "My Sister's Keeper",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['212'] = {'author':"Amish Tripathi", 'name': "Immortals of Meluha",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['213'] = {'author':"Salman Rushdie", 'name': "Midnight's Children ",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['214'] = {'author':"Arundhati Roy", 'name': "God of Small Things",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['215'] = {'author':"Anon", 'name': "Sindbad the Sailor",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['216'] = {'author':"PLato", 'name': "Socrates’ Defence",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['217'] = {'author':"Charles Dickens", 'name': "Bleak House",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['218'] = {'author':"Honoré de Balzac", 'name': "The Atheist’s Mass",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['219'] = {'author':"Jane Austen", 'name': "The Beautifull Cassandra",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['220'] = {'author':"Virgil", 'name': "Cruel Alexis",'type':"novels",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['221'] = {'author':"Anne Franke", 'name': "The Diary of a Young Girl",'type':"autobiography",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['222'] = {'author':"Adolf Hitler", 'name': "Mein Kampf",'type':"autobiography",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['223'] = {'author':"A.P.J Abdul Kalam", 'name': "Wings of Fire",'type':"autobiography",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['224'] = {'author':"MIchelle Obama", 'name': "Becoming",'type':"autobiography",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['225'] = {'author':"Nelson Mandela", 'name': "Long Walk to Freedom",'type':"autobiography",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['226'] = {'author':"Stanley B. Lippman, Josée Lajoie, and Barbara E. Moo", 'name': "Agastha Christie: An Autobiography",'type':"autobiography",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['227'] = {'author':"Michael Sipser", 'name': "Introduction to Theory of Computation",'type':"educational",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['228'] = {'author':"Peter Sykes", 'name': "Mechanism for organic chemistry",'type':"educational",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['229'] = {'author':"I.E.Irodov", 'name': "Problems in General Physics",'type':"educational",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}
books['230'] = {'author':"Garrett Grolemund.", 'name': "Hands on Programming with R",'type':"educational",'issuedby':None,"issuedate":None,"returndate":None,'quantity':1}

@app.route('/allbooks', methods=[ 'GET','POST'])
def allbooks():
    if request.method == 'POST':
        return redirect(url_for('allbooks'))
    return render_template('allbooks.html',books=books)

@app.route('/issuedbooks', methods=[ 'GET','POST'])
def issuedbooks():
    if request.method == 'POST':
        return redirect(url_for('issuedbooks'))
    return render_template('issuedbooks.html',books=books,issuedbook=issuedbook)
issuedbook={}

@app.route('/mybooks', methods=[ 'GET','POST'])
def mybooks():
    
    if request.method == 'POST':
        return redirect(url_for('mybooks'))
    return render_template('mybooks.html',issuedbook=issuedbook)

@app.route('/confirmissue', methods=[ 'GET','POST'])
def confirmissue():
    global issuebook_visited
    if(request.method=='POST'):
       
        global bookname,bookid
        issuedbookname=request.form.get("issuedbookname")
        issuedbookid=request.form.get("issuedbookid")
        print(issuedbookid," ",issuedbookname)
        if(issuedbookid==None):
            print("yes yes")
            return render_template('confirmissue.html')
       
        if(issuedbookid not in (books.keys()) or books[issuedbookid]['name']!=issuedbookname):
            print("book id exists")
            flash("No such book exists in the library. You have wrong book ID or wrong Book Name","error_bookissuenotexists")
            issuebook_visited=1
            return redirect(request.url)
        print(type(issuedbookid))
        issuedbook[issuedbookid]=books[issuedbookid]
        print(issuedbook[issuedbookid],[issuedbook[issuedbookid]['issuedby']],username_data[email_data.index(email)])
        issuedbook[issuedbookid]['issuedby']={"username":username_data[email_data.index(email)],"email":email}
        issuedbook[issuedbookid]['issuedate']=datetime.datetime.today().strftime('%d-%m-%Y')
        print(datetime.datetime.today().strftime('%d-%m-%Y'))
        issuedbook[issuedbookid]['returndate']=(datetime.datetime.today() + datetime.timedelta(days=7)).strftime('%d-%m-%Y')
        del books[issuedbookid]      
     
       
        issuebook_visited=1
        return redirect(url_for('bookissued')) 
         
    else:
        if(issuebook_visited==1):   
            issuebook_visited=0
            return render_template('confirmissue.html')
        else:
            return render_template('error.html')


@app.route('/bookissued', methods=[ 'GET','POST'])
def bookissued():
    return render_template('bookissued.html',issuedbook=issuedbook)

@app.route('/bookreturned', methods=[ 'GET','POST'])
def bookreturned():
    return render_template('bookreturned.html',issuedbook=issuedbook,books=books)


returnbook_visited=0
@app.route('/returnbook', methods=[ 'GET','POST'])
def returnbook():
    if(request.method=='POST'):
        global returnbook_visited
        returnedbookname=request.form.get("returnedbookname")
        returnedbookid=request.form.get("returnedbookid")
   
    
        if(returnedbookid==None):
            return render_template('returnbook.html')
       
        if(returnedbookid not in (issuedbook.keys()) or issuedbook[returnedbookid]['name']!=returnedbookname):
            flash("No such book issued. You have wrong book ID or wrong Book Name","error_bookreturnnotexists")
            returnbook_visited=1
            return redirect(request.url)
      
    
        
        books[returnedbookid]=issuedbook[returnedbookid]
        books[returnedbookid]['issuedate']=None
        books[returnedbookid]['returndate']=None
        books[returnedbookid]['issuedby']=None

        del issuedbook[returnedbookid]

     
        flash('Book returned successfully',"book_returned")
        returnbook_visited=1
        return redirect(url_for('bookreturned')) 
         
    else:
        if(returnbook_visited==1):   
            returnbook_visited=0
            return render_template('returnbook.html')
        else:
            return render_template('error.html')
   

if __name__ == '__main__':
    app.debug= True
    app.run()



