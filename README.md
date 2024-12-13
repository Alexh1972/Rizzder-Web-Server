# **IAp1-homework: Photo management web app**
**Ungureanu Vlad-Marin 315CA**

## Task Description
The program is a simple image sharing website hosted on a locally run python server. I have used it as a platform for sharing some wallpapers that I like.

### Functionalities
The program provides the following functionalities for authenticated users:
* **upload**: add an image to the gallery
* **delete**: removes an image or a category of images form the gallery

## Usage
To use the program, follow these steps:
* build the docker image:
```bash
vlad@DESKTOP-K4QHK8I:~$ docker build -t iap1-tema .
```
* start the server:
```bash
vlad@DESKTOP-K4QHK8I:~$ docker run -p 5000:5000 -it iap1-tema
```
Note: These commands might need `sudo` in order to work properly.

## Implementation
The sever runs from the `server.py` file and renders html files from the `templates/` directory. The wallpapers are stored in the `public/wallpapers/` directory and they are tracked by a dictionary that is written in the `public/database.txt` file. Each time one of the images is added/removed, its corresponding file (and thumbnail) is created/removed and the dictionary is modified. Editing the dictionary involves writing it to the file and then reading it to avoid desynchronizations. The dictionary is being sorted each time it is being read. Regarding the rendering of the thumbnails on the front page, it is done when the page is accessed.

## Design Choices
I chose the wallpaper theme because I like to do something with meaning, not just for the sake of it and I already had a collection of possible future wallpapers. Regarding the general aspect of the site, I mostly did what I thought would look good.

## Challenges
My main challenge was not knowing the language. I have never worked with python before this course and I have just played with html in highschool. I had to do a lot of research, like tutorials and reading the labs.

## Resources / Bibliography:
* The [skeleton](https://ocw.cs.pub.ro/courses/_media/ii/labs/s2/lab02-skel.zip) for the lab from which I 'borrowed' most of the code and then I modified it.