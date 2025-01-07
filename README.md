# Rizzder web server #

* Authors:
  * Cazacu Alexandru-Dan 322CA
  * Giurgiu Andrei-Ștefan 325CA
  * Plopeanu Teodora-Anca 322CA
  * Ungureanu Vlad-Marin 325CA

* Github repository:
  * <https://github.com/Alexh1972/Rizzder-Web-Server>

* Website link:
  * <https://rizzder-web-server.onrender.com/>

## Application description ##

* We decided to implement a Tinder-like web application, where each user can meet, chat and exchange photos with other users
* Each user is responsible for his/her account, where he/her can change their personal description and their dating preferences, upload good photos, delete bad photos and set a profile picture
* After setting up the account, the user can meet new people and chat with them via text messages if they think the receiving user is worth the attention
* If a user thinks another user is not right for him/her, it is recommended to explain to him/her why and end the relationship with decency by unmatching
* Ghosting and unreasoneable blocking will trigger <b>punishments</b> to the abusive user

## Application flow ##

* When a user first opens our website, he/she will land on the home page where a greeting will be seen and an encouragement to signup based on previous users experience
* If the user clicks on the signup button, the website will redirect to the signup page, where a username, a strong password and a birthdate will be required.
* After that, the user can edit their own profile, by adding photos and updating the description and preferences
* The user can edit the profile by clicking on the profile icon in the top-right corner
* To meet new people, the user will press on the multiple people icon on the navigation bar
* There will appear of other users that are compatible with the user.
* The user that requested compatible users can choose to <b>smash</b> or <b>pass</b> the recommended users.
* If the smashed account, considers they are compatible, they can a start a text chat.
* The user can see it's active chats if he/she clicks on the chat icon in the navigation bar.
* Also, if a user has problems or wants to learn more about us, by clicking on the information icon in the navigation, an <b>About us</b> page will appear.
* There it is displayed our mail and phone number, along with a Q&A and our "HQ" location

## Languages and technologies used ##

* The backend part of the application was written in Python, using the Django framework.
* The python version required to run the application is Python 3.13.1.
* For the frontend, we decided to use HTML, CSS and Javascript.
* The database management system we used is SQLite.
* The authentication system for our application is based on simple-jwt.
* The token will be stored in the cookie.
* Since we want our users to feel safe, we are using HTTPS and not HTTP.
* For the deployment and hosting part of the website, we used the platform Render, since it has a lot of free benefits and <b>doesn't require a credit card</b>

## Individual contributions ##

* Backend infrastructure : Cazacu Alexandru-Dan
* Graphical design : Plopeanu Teodora-Anca
* Home, edit pages : Plopeanu Teodora-Anca
* Navigation bar : Plopeanu Teodora-Anca
* Chatrooms : Ungureanu Vlad-Marin
* Meet page: Ungureanu Vlad-Marin
* About us page: Giurgiu Andrei-Ștefan
* Deployment and hosting: Giurgiu Andrei-Ștefan

## Difficulties and frustrating moments ##

* Deployment problems: 
  * Initially, the deployed website couldn't see the static files, because Django doesn't collect static files by default. We fixed that by creating a specific folder where the static files will be collected and added a specific command in the Procfile to do that before the site is launched
    * The Procfile command `python3 manage.py collectstatic --noinput`

* Development problems and frustrating problems: 
  * Problems with the modules since everytime we moved to a different computer we had to install all the modules for the program to work. Thankfully, we wrote a `requirements.txt` file where there are all the modules used.
  * Database problems when we moved to a different computer, because we had to make the migrations.

* Frontend frustrating problems:
  * Scroll-bar problems: Sometimes, on the HTML pages the scroll-bar wouldn't work. To fix this we had to introduce a new field for the css elements `overflow:auto`

