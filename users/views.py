from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from .models import app_user_mst, UserProfile, LinkProfile
from django.contrib import messages
from .constants import ICON_MAP
from on1i.settings import MEDIA_ROOT
# from django.conf import settings
# from django.contrib.auth import login


def SignUp(request):
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirm-password')

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
            newuser = app_user_mst(user_name=user_name, f_name=f_name,
                                   l_name=l_name, password=password, mobile=mobile, email=email)
            newuser.save()
        except Exception as e:
            print("error in saving new user: " + str(e))
            messages.error(request, "Value Error in Registration Form")
            return redirect('signup')

        messages.success(request, 'User created successfully')
        return redirect('signin')

    else:
        return render(request, 'users/signup.html')


def SignIn(request):

    if request.method == 'POST':

        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        if not user_name or not password:
            messages.error(request, 'missing or Invalid username or password')
            return redirect('signin')

        try:
            registered_user = app_user_mst.objects.get(user_name=user_name)
        except Exception as e:
            print("error in saving new user."+str(e))
            messages.error(request, 'Error in the Server from the Backend.')
            return redirect('signin')

        if registered_user and registered_user.password == password:
            request.session['user_name'] = registered_user.user_name
            messages.success(request, 'User Login Successfully')
            return redirect('home-page')
        else:
            messages.error(request, 'User is not registered.')
            return redirect('signup')

    return render(request, 'users/signin.html')


# this page is only visible when website is opened
def Home(request):
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

            if user_profile_data['user_name'] is not None:

                try:
                    user_link_profile = LinkProfile.objects.get(
                        user_name=user_name)
                    user_link_profile['user_name'] = user_profile_data['user_name']
                    user_link_profile.save()
                except Exception as e:
                    print("Error in updating link profile username: " + str(e))
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
                if i.channel_url == user_link_data['channel_link']:
                    messages.error(request, "Channel link already exits.")
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
    for x in data:
        channel_data[x.channel_url] = {
            'channel_icon': ICON_MAP.get(x.channel_url, 'channel/default-icon.png'),
            'personal_url': x.personal_url
        }

    context = {
        'linked_data': channel_data,
        'user_name': user_name,
    }

    return render(request, 'users/linked_page.html', context)
