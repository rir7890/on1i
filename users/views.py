from django.shortcuts import render, redirect
from .models import app_user_mst, UserProfile, LinkProfile
# from .encryption import encrypt_user_name, decrypt_user_name
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from .constants import ICON_MAP
from validate_email import validate_email
# from django.conf import settings
# from django.contrib.auth import login
import json


def SignUp(request):

    if request.session.get('user_name'):
        return redirect('home-page')
    else:

        if request.method == 'POST':
            user_name = request.POST.get('user_name')
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirmPassword = request.POST.get('confirm-password')

            # is_valid = validate_email(email, verify=True)

            # if not is_valid:
            #     messages.error(request, 'Email is not valid.')
            #     return redirect('signup')

            if not user_name or not f_name or not l_name or not mobile or not email or not password:
                messages.error(
                    request, 'Check all the data correctly don\'t enter empty values')
                return redirect('signup')

            if password != confirmPassword:
                messages.error(request, 'Password mismatch')
                return redirect('signup')

            if app_user_mst.objects.filter(user_name=user_name).exists():
                messages.error(request, 'Username is already taken')
                return redirect('signin')

            try:
                hashed_password = make_password(password)
                newuser = app_user_mst(user_name=user_name, f_name=f_name,
                                       l_name=l_name, password=hashed_password, mobile=mobile, email=email)
                user_profile_new = UserProfile(user_name=user_name)
                newuser.save()
                user_profile_new.save()
            except Exception as e:
                print("error in saving new user: " + str(e))
                # print(e)
                messages.error(request, "Value Error in Registration Form")
                return redirect('signup')

            messages.success(request, 'User created successfully')
            return redirect('signin')

        else:
            return render(request, 'users/signup.html')


def SignIn(request):

    if request.session.get('user_name'):
        return redirect('home-page')
    else:

        if request.method == 'POST':

            user_name = request.POST.get('user_name')
            password = request.POST.get('password')
            if not user_name or not password:
                messages.error(
                    request, 'missing or Invalid username or password')
                return redirect('signin')

            try:
                registered_user = app_user_mst.objects.get(user_name=user_name)
            except Exception as e:
                print("error in saving new user."+str(e))
                messages.error(
                    request, 'Error in the Server from the Backend.')
                return redirect('signin')

            if not user_name == UserProfile.objects.get(user_name=user_name).user_name:
                return redirect('signup')

            if registered_user and check_password(password, registered_user.password):
                request.session['user_name'] = registered_user.user_name
                messages.success(request, 'User Login Successfully')
                return redirect('home-page')
            else:
                messages.error(request, 'User is not registered.')
                return redirect('signup')

        return render(request, 'users/signin.html')


# this page is only visible when website is opened
def Home(request):
    if request.session.get('user_name'):
        return redirect('home-page')
    else:
        return render(request, 'users/home.html')


# after user login this page will be showned
def HomePage(request):

    user_name = request.session.get('user_name')
    try:
        user_info = app_user_mst.objects.get(user_name=user_name)
        user_profile = UserProfile.objects.get(user_name=user_name)
    except Exception as e:
        print("Couldn't find user information:"+str(e))
        messages.error(request, "Couldn't find user information.")
        return redirect('signin')

    # print(user_profile.image.url)

    if not user_info:
        messages.error(request, 'Username not found')
        return redirect('signin')

    if not user_profile:
        messages.error(request, 'Username not found in the Server')
        return redirect('signin')

    if not user_name:
        return redirect('signin')

    if request.method == 'POST':
        # uploading file logic
        if 'upload_profile' in request.POST:

            user_profile_data = {
                'image': request.FILES.get('image', user_profile.image),
                'user_name': request.POST.get('username', user_name),
                'description': request.POST.get('description', user_profile.description),
                'mobile': request.POST.get('mobile', user_info.mobile),
                'email': request.POST.get('email', user_info.email),
            }

            if user_profile_data['user_name'] or user_profile_data['mobile'] or user_profile_data['email']:
                updated_user = app_user_mst.objects.get(user_name=user_name)
                updated_user.user_name = user_profile_data['user_name']
                updated_user.mobile = user_profile_data['mobile']
                updated_user.email = user_profile_data['email']
                updated_user.save()

            # print(user_profile_data['image'])
            if user_profile_data['image'] or user_profile_data['description']:
                try:
                    user_profile_update = UserProfile.objects.get(
                        user_name=user_name)
                except Exception as e:
                    print("Error in getting user profile for update.")
                    messages.error(
                        request, "Could not get user profile for update.")
                    return redirect('home-page')

                if user_profile_data['image']:
                    user_profile_update.image = user_profile_data['image']

                if user_profile_data['description']:
                    user_profile_update.description = user_profile_data['description']

                user_profile_update.save()

            user_link_profile = LinkProfile.objects.filter(user_name=user_name)
            if user_link_profile:
                try:
                    user_link_profile = LinkProfile.objects.filter(
                        user_name=user_name)
                    user_link_profile['user_name'] = user_profile_data['user_name']
                    user_link_profile.save()
                except Exception as e:
                    print("Error in updating link profile username: " + str(e))
                    print(e)
                    messages.error(
                        request, "Error in updating link profile username.")
                    return redirect('home-page')

            if updated_user or user_link_profile or user_profile_update:

                messages.success(request, 'User Profile updated successfully')
            else:
                messages.error(request, "Error in model updation")

        # adding link logic
        elif 'add_link' in request.POST:

            user_link_data = {
                'channel_link': request.POST.get('channel'),
                'personal_link': request.POST.get('link')
            }

            if not user_link_data['channel_link'] and not user_link_data['personal_link']:
                messages.error(
                    request, "Provide channel and personal user url correctly")
                return redirect('home-page')

            try:
                link_user_data = LinkProfile.objects.filter(
                    user_name=user_name)
            except Exception as e:
                print("Error in filter the link profile: " + str(e))
                messages.error(request, "Error in filter the link profile.")
                return redirect('home-page')

            for i in link_user_data:
                if i.personal_url == user_link_data['personal_link']:
                    messages.error(request, "personal link already exits.")
                    return redirect('home-page')

           # adding the link of channel and personal
            try:
                LinkProfile.objects.create(
                    user_name=user_name, channel_url=user_link_data['channel_link'], personal_url=user_link_data['personal_link'])
            except Exception as e:
                print("Error creating link profile: " + e)
                messages.error(request, "Could not create link profile")
                return redirect('home-page')

        return redirect('home-page')

    context = {
        'user_name': user_name,
        'email': user_info.email,
        'mobile': user_info.mobile,
        'description': user_profile.description,
        'user_image': user_profile.image.url
    }

    return render(request, 'users/home_page.html', context)


# logout working
def logout_view(request):

    request.session.flush()
    messages.success(request, 'User have been successfully logged out')
    return redirect('signin')


# linked page code
def linked_view(request):

    user_name = request.session.get('user_name')
    if not user_name:
        messages.error(request, "request denied to access Link Page.")
        return redirect('signin')

    try:
        data = LinkProfile.objects.filter(user_name=user_name)
    except Exception as e:
        print("Error in getting linked profile using Filter"+str(e))
        messages.error(request, "Could not get linked profile data.")
        return redirect('home-page')

    channel_data = {}
    i = 0
    for x in data:
        channel_data[i] = {
            'channel_icon': ICON_MAP.get(x.channel_url, 'channel/default-icon.png'),
            'personal_url': x.personal_url,
            'profile_id': x.profile_id,
            'channel_name': x.channel_url,
        }
        i += 1

    # encrypted_user_name = encrypt_user_name(user_name)

    context = {
        'linked_data': channel_data,
        'user_name': user_name,
        'copy_link': request.build_absolute_uri().replace('linked-view', 'public-link'),

    }

    return render(request, 'users/linked_page.html', context)


def public_link(request, user_name):

    if user_name == request.session.get('user_name'):
        messages.error(request, 'User cannot access public page of itself')
        return redirect('signin')

    if not user_name:
        messages.error(request, "Invalid link.")
        return redirect('home')

    try:
        data = LinkProfile.objects.filter(user_name=user_name)
        print(data)
    except Exception as e:
        print("Error in getting linked profile using Filter"+str(e))
        messages.error(request, "Could not get linked profile data.")
        return redirect('home')

    channel_data = {}
    i = 0
    for x in data:
        channel_data[i] = {
            'channel_icon': ICON_MAP.get(x.channel_url, 'channel/default-icon.png'),
            'channel_name': x.channel_url,
            'personal_url': x.personal_url,
            'profile_id': x.profile_id
        }
        i += 1

    print(channel_data)
    context = {
        'linked_data': channel_data,
    }

    return render(request, 'users/public_link.html', context)


def track_click(request, profile_id):

    if not profile_id:
        messages.error(request, "Profile Id is not Valid")
        return redirect('home')

    try:
        data = LinkProfile.objects.get(profile_id=profile_id)
    except Exception as e:
        print("Error in getting linked profile using Filter"+str(e))
        messages.error(request, "Could not get linked profile data")
        return redirect('home')

    # print(data)
    data.click_count += 1
    data.save()

    return redirect(data.personal_url)


def DashBoardView(request):
    user_name = request.session.get('user_name')

    if not user_name:
        messages.error(request, "Invalid link")
        return redirect('home')

    try:
        data = LinkProfile.objects.filter(user_name=user_name)
    except Exception as e:
        print("Error in getting linked profile using Filter" + str(e))
        messages.error(request, "Could not get linked profile data.")
        return redirect('home')

    label = [profile.channel_url for profile in data]
    countData = [profile.click_count for profile in data]
    # print(label, countData)
    context = {
        'labels': json.dumps(label),
        'countData': json.dumps(countData),
        'user_name': user_name
    }
    return render(request, 'users/dashboard.html', context)
