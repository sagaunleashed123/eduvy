# Generated by Django 3.0.5 on 2021-05-20 11:20

import datetime
from django.db import migrations, models
import ed.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1, verbose_name='User')),
                ('BranchCode', models.CharField(blank=True, max_length=10, unique=True, verbose_name='Branch Code')),
                ('BranchName', models.CharField(blank=True, max_length=100, unique=True, verbose_name='Branch Name')),
                ('Image', models.ImageField(upload_to=ed.models.branch_upload, verbose_name='BranchImage')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=20)),
                ('DateofJoin', models.DateField(default=datetime.date.today, verbose_name='Date of Joining')),
            ],
            options={
                'verbose_name': 'Branch',
                'verbose_name_plural': 'Branches',
                'db_table': 'Branch',
                'ordering': ['-DateofJoin'],
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1, verbose_name='User')),
                ('CourseCode', models.CharField(max_length=10, unique=True, verbose_name='Course Code')),
                ('CourseName', models.CharField(max_length=100, unique=True, verbose_name='Course Name')),
                ('Branch', models.IntegerField(default=1, verbose_name='branch')),
                ('CourseDuration', models.IntegerField(verbose_name='Course Duration')),
                ('CourseDescription', models.TextField(verbose_name='Course Description')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=20)),
                ('DateofJoin', models.DateField(default=datetime.date.today, verbose_name='Date of Joining')),
                ('SupDoc', models.CharField(default=None, max_length=25, verbose_name='Supporting Doc')),
                ('CourseImage', models.ImageField(upload_to='', verbose_name='Course Image')),
            ],
            options={
                'verbose_name': 'Course',
                'verbose_name_plural': 'Courses',
                'db_table': 'Courses',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='instituteBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1, verbose_name='User ID')),
                ('Title', models.CharField(default='Title', max_length=150, verbose_name='Title')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=150, verbose_name='Status')),
                ('Image', models.ImageField(upload_to='institutebanner/')),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'institutebanner',
                'verbose_name_plural': 'institutebanners',
                'db_table': 'institute Banner',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='instituteBranch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institutionId', models.IntegerField(default=1, verbose_name='Institution ID')),
                ('branchCode', models.CharField(default='BSC', max_length=150, unique=True, verbose_name='Branch Code')),
                ('branchId', models.IntegerField(default=1, verbose_name='Branch ID')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=254, verbose_name='Status')),
                ('dateCreated', models.DateField(default=datetime.date.today, verbose_name='Date Created')),
            ],
            options={
                'verbose_name': 'InstitutionBranch',
                'verbose_name_plural': 'InstitutionBranches',
                'db_table': 'Institution Branch',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1, verbose_name='Users')),
                ('institutionCode', models.CharField(default='000', max_length=150, unique=True, verbose_name='Institution Code')),
                ('name', models.CharField(default='Name', max_length=150, unique=True, verbose_name='Institution Name')),
                ('chairmanName', models.CharField(default='Chairman Name', max_length=150, verbose_name='Chairman Name')),
                ('contactPersonName', models.CharField(default='Contact Person Name', max_length=150, verbose_name='Contact Person Name')),
                ('contactPersonPhone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('contactPersonEmail', models.EmailField(default='Contact Person Email', max_length=150, verbose_name='Contact Person Email')),
                ('address', models.CharField(default='Address', max_length=500, verbose_name='Address')),
                ('image', models.ImageField(default='static/images/brochure.jpg', upload_to=ed.models.Institution.user_directory_path, verbose_name='Image')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=50, verbose_name='Status')),
                ('cityId', models.IntegerField(default=1, verbose_name='City ID')),
                ('stateID', models.IntegerField(default=1, verbose_name='State Id')),
                ('logo', models.ImageField(default='brochure.jpg', upload_to=ed.models.Institution.user_directory_path)),
                ('description', models.TextField(blank=True, max_length=500, verbose_name='description')),
                ('brochure', models.ImageField(default='brochure.jpg', upload_to=ed.models.Institution.user_directory_path)),
            ],
            options={
                'verbose_name': 'Institution',
                'verbose_name_plural': 'Institutions',
                'db_table': 'Institution',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='institutionCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institutionId', models.IntegerField(default=1, verbose_name='Institution ID')),
                ('courseCode', models.CharField(default='BSC', max_length=150, unique=True, verbose_name='Course Code')),
                ('courseFee', models.CharField(default='100000', max_length=150, verbose_name='Course Fee')),
                ('branchId', models.IntegerField(default=1, verbose_name='Branch ID')),
                ('courseId', models.IntegerField(default=1, verbose_name='Course ID')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=254, verbose_name='Status')),
                ('admissionid', models.IntegerField(default=0, verbose_name='Students')),
                ('dateCreated', models.DateField(default=datetime.date.today, verbose_name='Date Created')),
            ],
            options={
                'verbose_name': 'InstitutionCourse',
                'verbose_name_plural': 'InstitutionCourses',
                'db_table': 'Institution Course',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='introBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1, verbose_name='User ID')),
                ('Title', models.CharField(default='Title', max_length=150, verbose_name='Title')),
                ('Description', models.CharField(default='Description', max_length=500, verbose_name='Description')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=150, verbose_name='Status')),
                ('Image', models.ImageField(upload_to='Introbanner/')),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'Introbanner',
                'verbose_name_plural': 'Introbanners',
                'db_table': 'Intro Banner',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='planBanner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1, verbose_name='User ID')),
                ('Title', models.CharField(default='Title', max_length=150, verbose_name='Title')),
                ('Description', models.CharField(default='Description', max_length=500, verbose_name='Description')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active', max_length=150, verbose_name='Status')),
                ('Image', models.ImageField(upload_to='Planbanner/')),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'Planbanner',
                'verbose_name_plural': 'Planbanners',
                'db_table': 'Plan Banner',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institutionID', models.IntegerField(default=1, verbose_name='Institution ID')),
                ('image', models.ImageField(default='static/images/brochure.jpg', upload_to=ed.models.Staff.user_directory_path, verbose_name='Image')),
                ('name', models.CharField(default='Staff Name', max_length=150, unique=True, verbose_name='Name')),
                ('fatehrName', models.CharField(default='Father Name', max_length=150, verbose_name="Father's Name")),
                ('nationality', models.CharField(default='Indian', max_length=150, verbose_name='Nationality')),
                ('email', models.EmailField(default='email@email.com', max_length=254, unique=True, verbose_name='Email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('DOB', models.DateField(verbose_name='Date of Birth')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=150, verbose_name='Gender')),
                ('maritalStatus', models.CharField(choices=[('Single', 'Single'), ('Married', 'Married'), ('Widowed', 'Widowed'), ('Divorced', 'Divorced')], default='Single', max_length=150, verbose_name='Marital Status')),
                ('annualSalary', models.IntegerField(default=25000, verbose_name='Annual Salary')),
                ('designation', models.CharField(default='Founder', max_length=150, verbose_name='Designation')),
                ('branchId', models.IntegerField(default=1, verbose_name='Branch')),
                ('aadhaarNumber', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('panNumber', models.CharField(default='Pan132V2hh', max_length=254, verbose_name='Pan Number')),
                ('DateofJoin', models.DateField(default=datetime.date.today)),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=254, verbose_name='Status')),
                ('date', models.DateField(default=datetime.date.today)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staffs',
                'db_table': 'Staff',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch', models.IntegerField(default=2021, verbose_name='Batch')),
                ('batchSection', models.CharField(default='1st year', max_length=254, verbose_name='batch year')),
                ('studentID', models.CharField(default='BRANCH-COURSE-BATCH-AdID', max_length=120, verbose_name='Student ID')),
                ('institutionId', models.CharField(default=1, max_length=150, verbose_name='Institution ID')),
                ('name', models.CharField(default='Name', max_length=150, verbose_name='Student Name')),
                ('email', models.CharField(default='email@email.com', max_length=245, verbose_name='Student Email')),
                ('branchId', models.IntegerField(default=1, verbose_name='Branch')),
                ('courseId', models.IntegerField(default=1, verbose_name='Course')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('documents', models.ImageField(blank=True, upload_to='')),
                ('address', models.CharField(default='address', max_length=600, verbose_name='Address')),
                ('guardianName', models.CharField(default='Gaurdian Name', max_length=150, verbose_name='Gaurdian Name')),
                ('guardianPhone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, region=None)),
                ('DateOfJoin', models.DateField(default=datetime.date.today, verbose_name='Date of Join')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
                'db_table': 'Student',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SupportingDoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(default=1, verbose_name='User')),
                ('DocumentName', models.CharField(default=None, max_length=25, unique=True, verbose_name='Supporting Documents')),
                ('Status', models.CharField(choices=[('Active', 'Active'), ('Inactive', 'Inactive')], max_length=25)),
                ('DateofAdd', models.DateField(default=datetime.date.today, verbose_name='Date of Joining')),
            ],
            options={
                'verbose_name': 'Supporting Document',
                'verbose_name_plural': 'Supporting Documents',
                'db_table': 'Supporting Documents',
                'managed': True,
            },
        ),
    ]