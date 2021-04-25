# HEI-ASYST

## Overview
Health Information and Attendance System (HEI-ASYST) adalah aplikasi berbasis web yang dapat mengatur data kehadiran dan kesehatan dengan mudah. Anda dapat menambah, melihat dan mengubah data kehadiran dan kesehatan melalui UI yang mudah dimengerti. 

## Setup
1. Install virtual environment python
```console
> pip install virtualenv
> virtualenv env
> \env\Scripts\activate.bat
```
2. Install requirements.txt
```console
> pip install requirements.txt
```
3. Lakukan Migrasi database
```console
> cd heiAyst
> python manage.py makemigrations
> python manage.py migrate
```
4. Buat admin (Untuk aktivasi user)
```console
> python manage.py createsuperuser
```
5. Jalankan code
```console
> python manage.py runserver
```
6. Jika ingin di hosting jangan lupa mengubah `DEBUG = True`
