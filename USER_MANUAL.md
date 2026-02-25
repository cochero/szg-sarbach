# SZG Sarbach Health Centre - User Manual

## Complete Guide to Using the Health Centre Management System

**SZG Sarbach Gesundheitszentrum**
Dorfstrasse 19, CH-3954 Leukerbad, Wallis
Phone: +41 79 290 77 44
Email: help@sarbach.swiss

**Certification Numbers:**
- EMR Nr: 26054
- ZSR Nr: B494360
- ASCA ID: 106773
- EGK Nr: 42736
- GLN Nr: 7601002563383

---

## Table of Contents

1. [Overview](#1-overview)
2. [Super Admin Guide](#2-super-admin-guide)
3. [Doctor Guide](#3-doctor-guide)
4. [Front Desk Staff Guide](#4-front-desk-staff-guide)
5. [Patient Guide](#5-patient-guide)
6. [Public Website Features](#6-public-website-features)
7. [SEO and Language Features](#7-seo-and-language-features)

---

## 1. Overview

The SZG Sarbach Health Centre system is a comprehensive web application for managing a health and wellness centre. It supports multiple types of users, each with their own login portal and set of features.

### User Types and Login Locations

| User Type | Login URL | Description |
|---|---|---|
| Super Admin | yourdomain.com/welcome/admin/ | Full system access, manages everything |
| Doctor | yourdomain.com/doctor/ | Medical staff, manages patients and examinations |
| Front Desk Staff | yourdomain.com/welcome/admin/ | Limited admin access for daily operations |
| Patient | yourdomain.com/register/ | Patient self-service portal |

---

## 2. Super Admin Guide

### 2.1 Logging In

1. Open your browser and go to yourdomain.com/welcome/admin/
2. Enter your username (default: **admin**) and password (default: **admin123**).
3. Click the **Login** button.
4. You will be redirected to the Admin Dashboard.

**Important:** Change the default password after your first login for security reasons.

---

### 2.2 Dashboard Overview

After logging in, you will see the Admin Dashboard at yourdomain.com/panel/

The dashboard displays:
- **Total Doctors** - Number of registered doctors
- **Total Patients** - Number of registered patients
- **Total Appointments** - Number of all appointments
- **Total Treatments** - Number of available treatments
- **Recent Appointments** - A list of the most recent appointments with patient name, doctor, date, and status
- **Quick Links** - Shortcuts to commonly used sections

---

### 2.3 Managing Departments

**URL:** yourdomain.com/panel/department/treatments/ (for Treatment departments)

Departments are the main categories that organize your treatments and doctors (e.g., Ayurveda, Massage Therapy, Yoga).

#### Adding a New Department

1. Go to the Departments page from the sidebar menu.
2. Click the **Add Department** button.
3. Fill in the department details:
   - **Name** - The department name
   - **Type** - Choose between "Treatments" or another category
   - **Description** - A brief description of the department
   - **Image** - Upload an image representing this department
4. Click **Submit** to save.

#### Editing a Department

1. Find the department in the list.
2. Click the **Edit** button next to it.
3. Update the information as needed.
4. Click **Update** to save changes.

#### Toggling Active/Inactive

1. Find the department in the list.
2. Click the **Toggle** button to switch between active and inactive.
3. Inactive departments will not be shown on the public website.

---

### 2.4 Managing Treatments

**URL:** yourdomain.com/panel/treatments/

Treatments are the individual services offered by the health centre (e.g., Abhyangam Massage, Craniosacral Therapy).

#### Adding a New Treatment

1. Go to **Treatments** from the sidebar menu.
2. Click **Add Treatment**.
3. Fill in the details:
   - **Name** - Treatment name
   - **Department** - Select the department this treatment belongs to
   - **Description** - Detailed description of the treatment
   - **Price** - Cost of the treatment in CHF
   - **Duration** - How long the treatment takes
   - **Image** - Upload a photo of the treatment
4. Click **Submit** to save.

#### Editing a Treatment

1. Find the treatment in the list.
2. Click **Edit**.
3. Update the fields as needed.
4. Click **Update** to save.

#### Deleting a Treatment

1. Find the treatment in the list.
2. Click the **Delete** button.
3. Confirm the deletion when prompted.

#### Toggling Active/Inactive

1. Click the **Toggle** button next to the treatment.
2. Inactive treatments will not appear on the public website or in booking options.

---

### 2.5 Managing Doctors

**URL:** yourdomain.com/panel/doctors/

Doctors are the medical and therapy practitioners at the health centre.

#### Adding a New Doctor

1. Go to **Doctors** from the sidebar menu.
2. Click **Add Doctor**.
3. Fill in the details:
   - **First Name** and **Last Name**
   - **Email** - Doctor's email address
   - **Username** - Login username for the doctor portal
   - **Password** - Login password for the doctor portal
   - **Phone** - Contact number
   - **Specialization** - Area of expertise
   - **Department** - Assign the doctor to a department
   - **Profile Image** - Upload a professional photo
   - **Bio/Description** - A brief biography
4. Click **Submit** to save.

The doctor can then log in at yourdomain.com/doctor/ using the username and password you created.

#### Editing a Doctor

1. Find the doctor in the list.
2. Click **Edit**.
3. Update the information and click **Update**.

---

### 2.6 Managing Patients

**URL:** yourdomain.com/panel/patients/

#### Viewing the Patient List

1. Go to **Patients** from the sidebar menu.
2. Browse the list of all registered patients.
3. Each entry shows the patient's name, email, phone, and registration date.

#### Registering a New Patient

1. Click **Register Patient**.
2. Enter the patient's details (name, email, phone, date of birth, address).
3. Set a username and password for the patient.
4. Click **Submit** to create the account.

#### Viewing Patient History

1. Find the patient in the list.
2. Click **View History** (or click on the patient's name).
3. This page shows:
   - All appointments for this patient
   - Examination records
   - Treatment orders
   - Diet charts and prescribed medicines

---

### 2.7 Managing Appointments

**URL:** yourdomain.com/panel/appointments/

#### Creating a New Appointment

1. Go to **Appointments** from the sidebar menu.
2. Click **Create Appointment**.
3. Fill in:
   - **Patient** - Search and select a patient (start typing the name)
   - **Doctor** - Select a doctor
   - **Department** - Select the department
   - **Date** - Choose the appointment date
   - **Time** - Choose the appointment time
   - **Notes** - Add any relevant notes
4. Click **Submit** to create the appointment.

#### Updating Appointment Status

1. Find the appointment in the list.
2. Click **Update**.
3. Change the status to one of the following:
   - **Pending** - Not yet confirmed
   - **Confirmed** - Appointment is confirmed
   - **Completed** - Treatment has been done
   - **Cancelled** - Appointment was cancelled
4. Click **Update** to save.

---

### 2.8 Managing Examinations

**URL:** yourdomain.com/panel/examinations/

Examinations are medical records created by doctors after seeing patients.

1. Go to **Examinations** from the sidebar.
2. View all examination records.
3. To create a new examination:
   - Select the **Patient**
   - Select the **Doctor**
   - Enter examination **Findings**
   - Add **Diagnosis** and **Recommendations**
4. Click **Submit** to save.

---

### 2.9 Managing Hotels and Apartments

**URL:** yourdomain.com/panel/hotels/

The system can list accommodation options in Leukerbad for patients traveling for treatments.

#### Adding Accommodation

1. Go to **Hotels/Apartments** from the sidebar.
2. Click **Add Hotel/Apartment**.
3. Fill in:
   - **Name** - Property name
   - **Type** - Hotel or Apartment
   - **Description** - Details about the property
   - **Address** - Full address
   - **Price** - Nightly rate
   - **Image** - Upload a photo
   - **Contact Info** - Phone number and/or website
4. Click **Submit** to save.

#### Editing and Deleting

- Click **Edit** to update accommodation details.
- Click **Delete** to remove a listing.
- Click **Toggle** to make it active or inactive on the public website.

---

### 2.10 Managing Cities

**URL:** yourdomain.com/panel/cities/

Cities are used for location-based appointment booking.

1. Go to **Cities** from the sidebar.
2. Click **Add City** to create a new city entry.
3. Enter the city name and any relevant details.
4. Click **Submit** to save.

---

### 2.11 Managing Banners

**URL:** yourdomain.com/panel/banners/

Banners are the large images and text that appear on the homepage slider.

#### Adding a Banner

1. Go to **Banners** from the sidebar.
2. Click **Add Banner**.
3. Fill in:
   - **Title** - Banner headline text
   - **Subtitle** - Secondary text
   - **Image** - Upload a banner image (recommended size: 1900x600 pixels)
   - **Link** - Optional URL to link to when clicked
4. Click **Submit** to save.

#### Editing a Banner

1. Find the banner in the list.
2. Click **Edit**.
3. Update the text or image.
4. Click **Update** to save.

---

### 2.12 Managing Packages

**URL:** yourdomain.com/panel/packages/

Packages combine multiple treatments and addons into bundled offerings at a special price.

#### Creating a Package

1. Go to **Packages** from the sidebar.
2. Click **Add Package**.
3. Fill in:
   - **Name** - Package name (e.g., "Wellness Weekend Package")
   - **Description** - What is included
   - **Treatments** - Select the treatments included in the package
   - **Addons** - Select any addons included
   - **Price** - Package price (typically discounted compared to individual prices)
   - **Duration** - Total package duration
   - **Image** - Upload a package image
4. Click **Submit** to save.

---

### 2.13 Managing Addons

**URL:** yourdomain.com/panel/addons/

Addons are supplementary services or products that can be added to treatments or packages (e.g., herbal oils, special wraps).

1. Go to **Addons** from the sidebar.
2. Click **Add Addon** to create a new addon.
3. Fill in the name, description, price, and image.
4. Click **Submit** to save.
5. Use the **Toggle** button to activate or deactivate addons.

---

### 2.14 Managing Blog, Events, and Workshops

**URL:** yourdomain.com/panel/blog/

The blog section supports three types of content: Blog posts, Events, and Workshops.

#### Creating a Post

1. Go to **Blog** from the sidebar.
2. Click **Add Post**.
3. Fill in:
   - **Title** - Post title
   - **Type** - Select Blog, Event, or Workshop
   - **Content** - Write the full article text
   - **Image** - Upload a featured image
   - **Published** - Check this to make the post visible on the public website
4. Click **Submit** to publish.

Posts will appear on the public website at:
- Blog posts: yourdomain.com/blogs/
- Events: yourdomain.com/events/
- Workshops: yourdomain.com/workshops/

---

### 2.15 Managing Orders

The system handles three types of orders:

#### Treatment Orders

**URL:** yourdomain.com/panel/orders/

View all treatment orders placed by patients through the shop. Each order shows the patient, treatment, quantity, total price, and status.

#### Addon Orders

**URL:** yourdomain.com/panel/addon-orders/

View all addon orders. These are supplementary items ordered alongside treatments.

#### Package Orders

**URL:** yourdomain.com/panel/package-orders/

View all package orders. These are bundled treatment packages purchased by patients.

---

### 2.16 Managing Enquiries

**URL:** yourdomain.com/panel/enquiries/

Enquiries are messages submitted through the public website's contact form.

1. Go to **Enquiries** from the sidebar.
2. View all submitted enquiries with the sender's name, email, subject, and message.
3. Review and respond to enquiries via email.

---

### 2.17 Managing Diets and Medicines

#### Diets

**URL:** yourdomain.com/panel/diets/

1. Go to **Diets** from the sidebar.
2. Click **Add Diet** to create a new diet plan.
3. Fill in the diet name, description, and associated patient.
4. Click **Submit** to save.

#### Medicines

**URL:** yourdomain.com/panel/medicines/

1. Go to **Medicines** from the sidebar.
2. Click **Add Medicine** to add a new medicine to the system.
3. Fill in the medicine name, description, dosage information, and usage instructions.
4. Click **Submit** to save.

---

### 2.18 Managing Staff (Front Desk Users)

**URL:** yourdomain.com/panel/staff/

Front desk staff members have limited admin access for daily operations.

#### Adding a Staff Member

1. Go to **Staff** from the sidebar.
2. Click **Add Staff**.
3. Fill in:
   - **First Name** and **Last Name**
   - **Email**
   - **Username** - Login username
   - **Password** - Login password
4. Click **Submit** to create the account.

Staff members log in at the same URL as admin (yourdomain.com/welcome/admin/) but have restricted permissions.

---

### 2.19 Site Settings

**URL:** yourdomain.com/panel/settings/

Site settings control the global information displayed across the website.

#### What You Can Configure

- **Clinic Name** - Your health centre's name
- **Phone Number** - Displayed on the website (e.g., +41 79 290 77 44)
- **Email Address** - Contact email (e.g., help@sarbach.swiss)
- **Address** - Physical address (Dorfstrasse 19, CH-3954 Leukerbad, Wallis)
- **Social Media Links** - Facebook, Instagram, Twitter, YouTube URLs
- **Certification Numbers:**
  - EMR Nr: 26054
  - ZSR Nr: B494360
  - ASCA ID: 106773
  - EGK Nr: 42736
  - GLN Nr: 7601002563383
- **About Text** - Description shown on the About page
- **Working Hours** - Operating hours for each day of the week
- **Logo** - Upload the clinic's logo

To update any setting:
1. Go to **Settings** from the sidebar.
2. Modify the desired fields.
3. Click **Save** to apply changes.

---

## 3. Doctor Guide

### 3.1 Logging In

1. Open your browser and go to yourdomain.com/doctor/
2. Enter the username and password provided by the administrator.
3. Click **Login**.
4. You will be redirected to the Doctor Dashboard.

---

### 3.2 Doctor Dashboard

**URL:** yourdomain.com/panel/doctor-portal/

The Doctor Dashboard shows:
- **Today's Appointments** - A list of patients scheduled for today
- **Total Patients** - Number of patients assigned to you
- **Upcoming Appointments** - Future scheduled appointments

---

### 3.3 Viewing and Managing Appointments

**URL:** yourdomain.com/panel/doctor-portal/appointments/

1. Click **Appointments** in the navigation menu.
2. View all appointments assigned to you.
3. Each appointment shows:
   - Patient name
   - Date and time
   - Treatment/Department
   - Status (Pending, Confirmed, Completed, Cancelled)
4. Click on an appointment to view full details.

---

### 3.4 Creating Examinations

**URL:** yourdomain.com/panel/examinations/

After seeing a patient, create an examination record:

1. Go to **Examinations** from the navigation.
2. Click **Add Examination**.
3. Fill in:
   - **Patient** - Select the patient from the list
   - **Date** - Date of the examination
   - **Findings** - What you observed during the examination
   - **Diagnosis** - Your professional diagnosis
   - **Recommendations** - Suggested treatments, lifestyle changes, or follow-ups
4. Click **Submit** to save.

The patient will be able to view this examination in their personal dashboard.

---

### 3.5 Creating Diet Charts

**URL:** yourdomain.com/panel/diets/

Prescribe dietary plans for patients:

1. Go to **Diets** from the navigation.
2. Click **Add Diet**.
3. Select the **Patient**.
4. Enter the diet plan details including:
   - Recommended foods
   - Foods to avoid
   - Meal schedule
   - Special instructions
5. Click **Submit** to save.

---

### 3.6 Prescribing Medicines

**URL:** yourdomain.com/panel/medicines/

Prescribe medicines to patients:

1. Go to **Medicines** from the navigation.
2. Click **Add Medicine** (if the medicine is not already in the system).
3. Enter the medicine name, dosage, and instructions.
4. Click **Submit** to save.

---

## 4. Front Desk Staff Guide

### 4.1 Logging In

1. Open your browser and go to yourdomain.com/welcome/admin/
2. Enter the username and password provided by the administrator.
3. Click **Login**.

Front desk staff use the same login page as the admin but have limited access.

---

### 4.2 Available Features

As a front desk staff member, you can:

#### Creating Appointments

1. Go to **Appointments** from the sidebar.
2. Click **Create Appointment**.
3. Search for the patient (start typing the name in the search field).
4. Select the doctor and department.
5. Choose the date and time.
6. Click **Submit** to create.

#### Registering New Patients

1. Go to **Patients** from the sidebar.
2. Click **Register Patient**.
3. Enter the patient's personal details.
4. Create login credentials for the patient.
5. Click **Submit** to register.

#### Managing Enquiries

1. Go to **Enquiries** from the sidebar.
2. View messages submitted through the website's contact form.
3. Note down important enquiries and follow up via phone or email.

---

### 4.3 Limitations

Front desk staff cannot:
- Modify site settings
- Delete treatments or departments
- Access financial reports
- Manage other staff accounts
- Create or edit blog posts

---

## 5. Patient Guide

### 5.1 Creating an Account

#### Option 1: Register on the Website

1. Go to yourdomain.com/register/
2. Click the **Register** tab.
3. Fill in your details:
   - **First Name** and **Last Name**
   - **Email Address**
   - **Phone Number**
   - **Username** - Choose a unique username
   - **Password** - Choose a secure password
4. Click **Register** to create your account.

#### Option 2: Login Button on Homepage

1. Visit the homepage at yourdomain.com
2. Click the **Login** button in the top navigation bar.
3. You will be taken to the login/registration page.

#### Option 3: Registered by Front Desk

The front desk staff can register you during your visit. They will provide you with your login credentials.

---

### 5.2 Logging In

1. Go to yourdomain.com/register/
2. Enter your username and password.
3. Click **Login**.
4. You will be redirected to your Patient Dashboard.

---

### 5.3 Patient Dashboard

**URL:** yourdomain.com/user/

Your dashboard shows:
- **Your Appointments** - All your upcoming and past appointments
- **Your Orders** - Treatment and product orders
- **Quick Actions** - Book a new appointment, view treatments

---

### 5.4 Profile Management

**URL:** yourdomain.com/user/profile/

1. Click **Profile** in the navigation menu.
2. View and update your personal information:
   - Name
   - Email
   - Phone number
   - Date of birth
   - Address
3. Click **Update** to save changes.

---

### 5.5 Booking an Appointment

**URL:** yourdomain.com/appointment/

1. Go to **Book Appointment** from the navigation or dashboard.
2. Fill in the appointment form:
   - **Department** - Select the type of treatment you need
   - **Treatment** - Choose a specific treatment (options change based on department)
   - **Doctor** - Select your preferred doctor (optional)
   - **Preferred Date** - Choose your desired date
   - **Preferred Time** - Choose your desired time
   - **Location** - Select the location
   - **Notes** - Add any special requirements or concerns
3. Click **Submit** to request the appointment.
4. The clinic staff will confirm your appointment.

---

### 5.6 Shopping for Treatments

#### Browsing Treatments

1. Visit any department page on the website.
2. Click on a treatment to see details and pricing.
3. Click **Book Now** or **Add to Cart**.

#### Using the Cart

**URL:** yourdomain.com/cart/

1. Review items in your cart.
2. Adjust quantities if needed.
3. Remove items by clicking the remove button.
4. Click **Proceed to Checkout** when ready.

#### Checkout

**URL:** yourdomain.com/checkout/

1. Review your order summary.
2. Confirm your contact details.
3. Click **Place Order** to complete the purchase.

#### Viewing Your Orders

**URL:** yourdomain.com/orders/

1. Click **My Orders** in the navigation.
2. View all your past and current orders.
3. Each order shows the treatment name, date, quantity, and total price.

---

### 5.7 Viewing Examination Reports

After a doctor creates an examination record for you, you can view it in your dashboard:

1. Log in to your account.
2. Go to your dashboard.
3. Find the **Examinations** section.
4. Click on an examination to see full details including:
   - Doctor's findings
   - Diagnosis
   - Recommendations
   - Diet charts (if prescribed)
   - Medicines (if prescribed)

---

### 5.8 Viewing Addons

**URL:** yourdomain.com/myaddons/

1. Click **My Addons** in the navigation.
2. View all addon services you have ordered.

---

## 6. Public Website Features

These features are available to all visitors without logging in.

### 6.1 Homepage

**URL:** yourdomain.com

The homepage includes:
- **Banner Slider** - Large images showcasing the health centre and its services
- **Featured Departments** - Quick links to main treatment categories
- **Featured Treatments** - Popular treatments with images and prices
- **About Section** - Brief introduction to the health centre
- **Doctor Profiles** - Featured doctors with their specializations
- **Certification Badges** - Swiss health certifications (EMR, ASCA, ZSR, EGK)
- **Contact Information** - Phone, email, and address
- **Quick Appointment Booking** - A form to request an appointment directly from the homepage

---

### 6.2 Browsing Departments and Treatments

**URL:** yourdomain.com/department-name/ (e.g., yourdomain.com/ayurveda/)

1. Click on any department from the homepage or navigation menu.
2. View all treatments available in that department.
3. Each treatment shows:
   - Treatment name and image
   - Brief description
   - Price in CHF
   - Duration
4. Click on a treatment for full details.

#### Treatment Detail Page

**URL:** yourdomain.com/treatment/treatment-name/

Each treatment detail page shows:
- Full description of the treatment
- Benefits and what to expect
- Price and duration
- Related treatments
- Option to book an appointment or add to cart

---

### 6.3 Viewing Doctor Profiles

**URL:** yourdomain.com/doctor-profile/

View information about the health centre's practitioners:
- Doctor's name and photo
- Specialization and department
- Professional biography
- Qualifications and certifications

---

### 6.4 Packages

**URL:** yourdomain.com/packages/

Browse treatment packages that combine multiple services:

1. Click **Packages** in the navigation.
2. View all available packages with images and prices.
3. Click on a package for full details.

#### Package Detail Page

**URL:** yourdomain.com/package/package-name/

Each package page shows:
- Package name and description
- Included treatments and addons
- Total price (discounted from individual prices)
- Duration
- Booking option

---

### 6.5 Addons

**URL:** yourdomain.com/addons/

Browse supplementary services and products:
- Herbal oils and preparations
- Special therapy add-ons
- Wellness products

---

### 6.6 Accommodation Listings

**URL:** yourdomain.com/accomodations/

For patients traveling to Leukerbad for treatments:

1. Click **Accommodations** in the navigation.
2. Browse available hotels and apartments.
3. Each listing shows photos, descriptions, and pricing.
4. Click on a listing for more details.

#### Accommodation Detail

**URL:** yourdomain.com/apartment/id/

View full details about a specific accommodation including:
- Photos
- Room descriptions
- Amenities
- Location
- Contact information
- Pricing

---

### 6.7 Blog, Events, and Workshops

#### Blog

**URL:** yourdomain.com/blogs/

Read articles about health, wellness, Ayurveda, and natural therapies.

#### Events

**URL:** yourdomain.com/events/

View upcoming events at the health centre.

#### Workshops

**URL:** yourdomain.com/workshops/

Browse available workshops and training sessions.

Each post can be read in full by clicking on the title or "Read More" link. The detail pages show the full article text, images, and publication date.

---

### 6.8 Contact Form

**URL:** yourdomain.com/contact/

1. Click **Contact** in the navigation.
2. Fill in:
   - **Your Name**
   - **Your Email**
   - **Subject**
   - **Message**
3. Click **Send** to submit your enquiry.
4. The clinic staff will receive your message and respond via email.

**Direct Contact:**
- Phone: +41 79 290 77 44
- Email: help@sarbach.swiss
- Address: Dorfstrasse 19, CH-3954 Leukerbad, Wallis

---

### 6.9 Language Switching

The website supports multiple languages to serve the diverse population of Switzerland and international visitors:

- **Deutsch (DE)** - German
- **Français (FR)** - French
- **Italiano (IT)** - Italian
- **Русский (RU)** - Russian
- **English (EN)** - English

To switch languages:
1. Look for the language selector in the website header (usually displayed as flag icons or language codes).
2. Click on your preferred language.
3. The website content will switch to the selected language.

Additional languages are available through Google Translate integration (see Section 7).

---

### 6.10 Booking an Appointment (Public)

**URL:** yourdomain.com/appointment/

Visitors can request an appointment:
1. Click **Book Appointment** in the navigation.
2. If not logged in, you will be asked to log in or register first.
3. Fill in the appointment form with your preferred department, treatment, doctor, date, and time.
4. Submit the form.
5. The clinic will confirm your appointment.

---

### 6.11 Real Estate / Property Listings

**URL:** yourdomain.com/realestate/

View property and real estate listings in the Leukerbad area.

---

### 6.12 Additional Pages

- **About Us:** yourdomain.com/about/ - Learn about the health centre's history, mission, and team.
- **Privacy Policy:** yourdomain.com/privacy/ - Read the privacy policy.
- **Terms and Conditions:** yourdomain.com/terms/ - Read the terms of service.

---

## 7. SEO and Language Features

### 7.1 Google Translate Integration

The website includes Google Translate integration, allowing visitors to translate the entire site into any language supported by Google:

1. Look for the Google Translate widget on the page.
2. Select your desired language from the dropdown.
3. All text on the page will be automatically translated.

This is in addition to the native language support for German, French, Italian, Russian, and English.

---

### 7.2 Structured Data (JSON-LD)

The website includes structured data markup (JSON-LD format) that helps search engines like Google understand the content better. This enables:

- **Rich search results** - Your health centre may appear with enhanced information in Google search results
- **Knowledge panel** - Google may display business information directly
- **Local business listing** - Helps with local search visibility in Leukerbad and Wallis

The structured data includes:
- Business name, address, and phone number
- Opening hours
- Services offered
- Certification numbers
- Geographic coordinates

---

### 7.3 robots.txt

**URL:** yourdomain.com/robots.txt

The robots.txt file tells search engines which pages to crawl and index. It is automatically generated by the system and includes:
- Permission for all search engines to crawl public pages
- Restrictions on admin and private pages
- Link to the sitemap

---

### 7.4 Sitemap

**URL:** yourdomain.com/sitemap.xml

The sitemap is an XML file that lists all public pages on the website. It helps search engines discover and index your content efficiently. The sitemap is automatically generated and includes:
- Homepage
- Department pages
- Treatment pages
- Blog posts, events, and workshops
- Package pages
- Static pages (About, Contact, etc.)

Submit this sitemap URL to Google Search Console for best results.

---

### 7.5 Meta Tags Optimization

Each page includes optimized meta tags for search engines:
- **Title Tag** - Descriptive page title including "SZG Sarbach Health Centre"
- **Meta Description** - Summary of the page content
- **Open Graph Tags** - For social media sharing (Facebook, LinkedIn)
- **Canonical URLs** - Prevent duplicate content issues

---

## Quick Reference

### Important URLs

| Page | URL |
|---|---|
| Homepage | yourdomain.com |
| Admin Login | yourdomain.com/welcome/admin/ |
| Admin Dashboard | yourdomain.com/panel/ |
| Doctor Login | yourdomain.com/doctor/ |
| Doctor Dashboard | yourdomain.com/panel/doctor-portal/ |
| Patient Login/Register | yourdomain.com/register/ |
| Patient Dashboard | yourdomain.com/user/ |
| Patient Profile | yourdomain.com/user/profile/ |
| Book Appointment | yourdomain.com/appointment/ |
| Treatments Shop | yourdomain.com/shop/treatment-name/ |
| Cart | yourdomain.com/cart/ |
| Checkout | yourdomain.com/checkout/ |
| My Orders | yourdomain.com/orders/ |
| Packages | yourdomain.com/packages/ |
| Addons | yourdomain.com/addons/ |
| Accommodations | yourdomain.com/accomodations/ |
| Blog | yourdomain.com/blogs/ |
| Events | yourdomain.com/events/ |
| Workshops | yourdomain.com/workshops/ |
| Contact | yourdomain.com/contact/ |
| About | yourdomain.com/about/ |
| Privacy Policy | yourdomain.com/privacy/ |
| Terms | yourdomain.com/terms/ |
| Django Admin | yourdomain.com/admin/ |

### Default Login Credentials

| Role | Username | Password | Login URL |
|---|---|---|---|
| Super Admin | admin | admin123 | yourdomain.com/welcome/admin/ |
| Doctor | (set by admin) | (set by admin) | yourdomain.com/doctor/ |
| Front Desk | (set by admin) | (set by admin) | yourdomain.com/welcome/admin/ |
| Patient | (self-registered) | (self-created) | yourdomain.com/register/ |

---

## Support

For assistance with any feature or technical issue:

- **Email:** help@sarbach.swiss
- **Phone:** +41 79 290 77 44
- **Address:** Dorfstrasse 19, CH-3954 Leukerbad, Wallis

**Certification Numbers:**
- EMR Nr: 26054
- ZSR Nr: B494360
- ASCA ID: 106773
- EGK Nr: 42736
- GLN Nr: 7601002563383
