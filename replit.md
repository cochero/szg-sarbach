# SZG Sarbach Gesundheitszentrum - Django Health Center Management System

## Overview
A comprehensive health center management system for SZG Sarbach Gesundheitszentrum in Leukerbad, Switzerland. Converted from PHP/CodeIgniter/MySQL to Django/Python/PostgreSQL (development) / MySQL (production). Supports 4 user roles with multilingual support (DE/FR/IT/RU/EN).

## Current State
- **Status**: MVP Complete
- **Framework**: Django 5.x with Python 3.11
- **Database**: PostgreSQL (Replit dev) / MySQL (production)
- **Frontend**: Bootstrap 5.3, Font Awesome 6, AOS animations
- **Theme**: Green (#6cb444)

## Project Architecture

### Django Apps
- `core` - Base models (UserProfile, Banner, ContactSubmission, SiteSettings), authentication views, home/about/contact pages, SEO (robots.txt, sitemap.xml)
- `clinic` - Department, Treatment, Doctor, Hotel, City, Package, Addon models and public-facing views
- `appointments` - Appointment, Examination, DietItem, PatientDietChart models, booking system
- `shop` - Medicine, Order, OrderItem, AddonOrder, PackageOrder models, cart & checkout
- `blog_app` - BlogPost model (Blog/Event/Workshop types), public listing and detail views
- `admin_panel` - Internal admin dashboard with CRUD for all entities, role-based access

### User Roles
1. **Super Admin** - Full access to admin panel (/panel/)
2. **Doctor** - Doctor portal with appointments, examinations (/panel/doctor/)
3. **Front Desk** - Limited admin access (/panel/)
4. **Patient** - Public site with dashboard, booking, shopping (/user/)

### Key URLs
- Public: /, /about/, /contact/, /packages/, /accommodations/, /blog/, /events/
- Auth: /register/, /doctor/, /welcome/admin/
- Admin Panel: /panel/
- API/AJAX: /ajax/*

### Login Credentials (Development)
- Super Admin: admin / admin123
- Access admin panel at: /welcome/admin/

## Design Choices
- Bootstrap 5.3 CDN (no local CSS framework files)
- Google Translate for multilingual (DE/FR/IT/RU/EN)
- Session-based shopping cart
- JSON-LD structured data for SEO
- Context processors for site settings and navigation

## Recent Changes
- 2026-02-20: Full admin panel CRUD for all entities
  - Blog/Events: add, edit, delete, toggle active/inactive
  - Packages, Addons, Banners, Medicines: full CRUD with modals
  - Patient management: register, edit/update, view history
  - Settings page: all fields (general, certifications, social, about content)
  - About page made dynamic (content from SiteSettings, team from Doctor model)
- 2026-02-20: Integrated real content from sarbach.swiss
  - Database populated with 7 departments, 18 symptoms, 18 treatments, 2 doctors, 4 addons, 6 banners
  - Homepage redesigned with symptoms grid, treatment cards, promo banners, certification badges, addons, CTA
  - About page updated with team photos, expanded FAQ, CTA
  - Contact page and base template: address corrected to Dorfstrasse 23
  - Banner images: optimized 1600x600px (60-200KB each)
  - Treatment images: optimized 80-90% size reduction
  - SEO structured data made dynamic (uses site_settings)
- 2026-02-25: WhatsApp integration for enquiries (+41 79 290 77 44)
  - Floating WhatsApp button on all pages (bottom-right corner)
  - WhatsApp link in top bar header
  - WhatsApp card on contact page with "Start Chat" button
  - WhatsApp CTA buttons on home page and about page
  - Footer WhatsApp icon in social links
- 2026-02-25: Comprehensive pytest suite (100 tests across all 6 apps)
- 2026-02-25: Security fix for ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS
- 2026-02-25: VPS deployment package (deploy_package/) with MySQL config
- 2026-02-20: Initial MVP build complete
- Admin panel templates (26 templates) created
- SEO: robots.txt, sitemap.xml, JSON-LD schema, meta tags
- Deployment documentation and user manual created

## Files Structure
```
szg_sarbach/          # Django project settings
core/                 # Core app (auth, home, contact)
clinic/               # Clinic app (departments, treatments, doctors)
appointments/         # Appointments and examinations
shop/                 # Pharmacy/shop
blog_app/             # Blog and events
admin_panel/          # Internal admin dashboard
templates/            # All HTML templates
static/               # CSS, JS, images
  img/                # Original PHP project images
  images/             # Extracted zip images
  css/                # Custom CSS
DEPLOYMENT.md         # Production deployment guide
USER_MANUAL.md        # Complete user manual
```

## User Preferences
- Swiss health center context (EMR, ASCA, EGK, ZSR certifications)
- German as primary language with easy language switching
- Green theme matching original PHP design
- MySQL for production deployment on shared hosting
