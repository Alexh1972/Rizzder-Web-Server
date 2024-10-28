from django.shortcuts import render, HttpResponse, redirect
from ..utils import *
from ..models import User, UserImage, Gender
import logging
import base64
import json
import uuid

logger = logging.getLogger(__name__)


def userEditView(request):
    try:
        jwt_token_decoder = JWTTokenDecoder(request.GET['token'])
        user = jwt_token_decoder.getUserFromToken()

        if user is None:
            return redirect("login")

        images = user.getImagesList()
        user_age = user.calculateAge()

        return render(request, "user/edit.html", {"user": user, "images" : images, "age" : user_age})
    except:
        return redirect("login")


def userEdit(request):
    try:
        jwt_token_decoder = JWTTokenDecoder(request.POST['token'])
        user = jwt_token_decoder.getUserFromToken()

        if user is None:
            return redirect("login")

        userQuery = User.objects.filter(user_id=user.user_id)

        if request.POST['description'] != "":
            userQuery.update(
                description_encoded_64=base64.b64encode(request.POST['description'].encode("utf-8")).decode("utf-8"))

        if request.POST['gender'] != "":
            userQuery.update(
                gender=request.POST['gender'])

        if request.POST['genderPreference'] != "":
            userQuery.update(
                gender_preference=request.POST['genderPreference'])

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    except Exception as e:
        logger.error(e)
        return redirect("login")


def userEditPhoto(request):
    try:
        jwt_token_decoder = JWTTokenDecoder(request.GET['token'])
        user = jwt_token_decoder.getUserFromToken()

        if user is None:
            return redirect("login")

        if user.images.all().count() >= 5:
            response = {'error': "Can't add more than 5 photos."}
            return HttpResponse(json.dumps(response), content_type="application/json")

        if 'file' not in request.FILES:
            response = {'error': "No photo uploaded."}
            return HttpResponse(json.dumps(response), content_type="application/json")

        filename = 'rizzder_app/files/user_images/tmp-' + str(uuid.uuid4())

        with open(filename, "wb+") as file:
            file.write(request.FILES['file'].read())
            file.flush()
            userImage = UserImage.objects.create(active=True, image=filename)
            userImage.save()
            user.images.add(userImage)
            user.save()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    except Exception as e:
        logger.error(e)
        return redirect("login")

def userDeletePhoto(request):
    try:
        jwt_token_decoder = JWTTokenDecoder(request.POST['token'])
        user = jwt_token_decoder.getUserFromToken()

        if user is None:
            return redirect("login")

        image_id = request.POST['id']
        UserImage.objects.filter(user_image_id=image_id).delete()

        response = {'status': 'success'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    except Exception as e:
        logger.error(e)
        return redirect("login")

def getGenders(request):
    try:
        jwt_token_decoder = JWTTokenDecoder(request.POST['token'])
        user = jwt_token_decoder.getUserFromToken()

        if user is None:
            return redirect("login")

        genders = [{"key": e.value, "value": e.name} for e in Gender]

        response = {'status': 'success', "genders": genders}
        return HttpResponse(json.dumps(response), content_type="application/json")
    except Exception as e:
        logger.error(e)
        return redirect("login")
