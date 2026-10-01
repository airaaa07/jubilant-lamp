#!/usr/bin/env python3
"""
UniversityERP - Master Enterprise Architecture & Functional Presentation Generator
Generates a comprehensive, 32-slide, widescreen 16:9 executive PowerPoint deck.
Covers 100% of the platform: Architecture, 14 Modules, 24 Roles, Student Lifecycle,
Statutory Gateways, 138 Database Models, 71 API Controllers, and 49 Frontend Pages.
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- Color Palette (Executive Dark Slate & Modern Accents) ---
BG_COLOR = RGBColor(15, 23, 42)        # Slate 900 #0F172A
CARD_BG = RGBColor(30, 41, 59)        # Slate 800 #1E293B
CARD_BORDER = RGBColor(51, 65, 85)    # Slate 700 #334155
CARD_BG_ALT = RGBColor(24, 32, 47)    # Slate 850 #18202F

TEXT_WHITE = RGBColor(255, 255, 255)  # Pure White #FFFFFF
TEXT_BODY = RGBColor(226, 232, 240)   # Slate 200 #E2E8F0
TEXT_MUTED = RGBColor(148, 163, 184)  # Slate 400 #94A3B8

ACCENT_BLUE = RGBColor(56, 189, 248)   # Cyan / Sky #38BDF8
ACCENT_GREEN = RGBColor(16, 185, 129)  # Emerald #10B981
ACCENT_AMBER = RGBColor(245, 158, 11)  # Amber Gold #F59E0B
ACCENT_PURPLE = RGBColor(168, 85, 247) # Violet / Purple #A855F7
ACCENT_ROSE = RGBColor(244, 63, 94)    # Rose / Crimson #F43F5E
ACCENT_INDIGO = RGBColor(99, 102, 241) # Indigo #6366F1

TOTAL_SLIDES = 32

def set_slide_background(slide):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background()
    return bg

def add_header(slide, category, title, subtitle, slide_num):
    # Category Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.38), Inches(3.2), Inches(0.32))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 58, 138)
    pill.line.color.rgb = ACCENT_BLUE
    pill.line.width = Pt(1)
    tf_pill = pill.text_frame
    tf_pill.word_wrap = True
    p_pill = tf_pill.paragraphs[0]
    p_pill.text = category.upper()
    p_pill.font.name = 'Arial'
    p_pill.font.size = Pt(9)
    p_pill.font.bold = True
    p_pill.font.color.rgb = ACCENT_BLUE
    p_pill.alignment = PP_ALIGN.CENTER

    # Title & Subtitle Box
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.733), Inches(0.95))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(21)
    p_title.font.bold = True
    p_title.font.color.rgb = TEXT_WHITE

    p_sub = tf.add_paragraph()
    p_sub.text = subtitle
    p_sub.font.name = 'Arial'
    p_sub.font.size = Pt(11)
    p_sub.font.color.rgb = TEXT_MUTED

    # Divider Line
    sep = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.72), Inches(11.733), Inches(0.02))
    sep.fill.solid()
    sep.fill.fore_color.rgb = CARD_BORDER
    sep.line.fill.background()

    add_footer(slide, slide_num)

def add_footer(slide, slide_num):
    tx_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.05), Inches(6.0), Inches(0.3))
    tf_l = tx_left.text_frame
    p_l = tf_l.paragraphs[0]
    p_l.text = "UniversityERP Platform | 20-Year Principal Enterprise Architect Blueprint"
    p_l.font.name = 'Arial'
    p_l.font.size = Pt(9)
    p_l.font.color.rgb = TEXT_MUTED

    tx_mid = slide.shapes.add_textbox(Inches(5.0), Inches(7.05), Inches(4.5), Inches(0.3))
    tf_m = tx_mid.text_frame
    p_m = tf_m.paragraphs[0]
    p_m.text = "Confidential & Enterprise Architecture Specification"
    p_m.font.name = 'Arial'
    p_m.font.size = Pt(9)
    p_m.font.color.rgb = RGBColor(100, 116, 139)
    p_m.alignment = PP_ALIGN.CENTER

    tx_right = slide.shapes.add_textbox(Inches(10.5), Inches(7.05), Inches(2.0), Inches(0.3))
    tf_r = tx_right.text_frame
    p_r = tf_r.paragraphs[0]
    p_r.text = f"Slide {slide_num} of {TOTAL_SLIDES}"
    p_r.font.name = 'Arial'
    p_r.font.size = Pt(9)
    p_r.font.bold = True
    p_r.font.color.rgb = ACCENT_BLUE
    p_r.alignment = PP_ALIGN.RIGHT

def add_card(slide, left, top, width, height, title, items, accent_color=ACCENT_BLUE, subtitle=None):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_BG
    card.line.color.rgb = CARD_BORDER
    card.line.width = Pt(1)

    hl = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(0.06))
    hl.fill.solid()
    hl.fill.fore_color.rgb = accent_color
    hl.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(left + 0.18), Inches(top + 0.15), Inches(width - 0.36), Inches(height - 0.25))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_title = tf.paragraphs[0]
    p_title.text = title
    p_title.font.name = 'Arial'
    p_title.font.size = Pt(12.5)
    p_title.font.bold = True
    p_title.font.color.rgb = accent_color

    if subtitle:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = 'Arial'
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = TEXT_MUTED

    for item in items:
        p_item = tf.add_paragraph()
        if isinstance(item, tuple):
            label, val = item
            run_lbl = p_item.add_run()
            run_lbl.text = f"• {label}: "
            run_lbl.font.bold = True
            run_lbl.font.color.rgb = TEXT_WHITE
            run_lbl.font.size = Pt(9.5)
            run_val = p_item.add_run()
            run_val.text = val
            run_val.font.color.rgb = TEXT_BODY
            run_val.font.size = Pt(9.5)
        else:
            p_item.text = f"• {item}"
            p_item.font.name = 'Arial'
            p_item.font.size = Pt(9.5)
            p_item.font.color.rgb = TEXT_BODY

def add_table_slide(slide, left, top, width, height, headers, rows, col_widths):
    table_shape = slide.shapes.add_table(len(rows) + 1, len(headers), Inches(left), Inches(top), Inches(width), Inches(height))
    tbl = table_shape.table

    for i, w in enumerate(col_widths):
        tbl.columns[i].width = Inches(w)

    for j, h in enumerate(headers):
        cell = tbl.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 58, 138)
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.name = 'Arial'
        p.font.size = Pt(9.5)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE

    for r_idx, row in enumerate(rows):
        bg = CARD_BG if r_idx % 2 == 0 else CARD_BG_ALT
        for c_idx, val in enumerate(row):
            cell = tbl.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.text = str(val)
            p.font.name = 'Arial'
            p.font.size = Pt(9)
            p.font.color.rgb = TEXT_WHITE if c_idx == 0 else TEXT_BODY

def add_metrics_banner(slide, left, top, width, height, metrics):
    n = len(metrics)
    col_w = (width - 0.2 * (n - 1)) / n
    for idx, (val, lbl, sub, color) in enumerate(metrics):
        cx = left + idx * (col_w + 0.2)
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(top), Inches(col_w), Inches(height))
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = CARD_BORDER
        box.line.width = Pt(1)

        hl = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(top), Inches(col_w), Inches(0.04))
        hl.fill.solid()
        hl.fill.fore_color.rgb = color
        hl.line.fill.background()

        tb = slide.shapes.add_textbox(Inches(cx + 0.08), Inches(top + 0.08), Inches(col_w - 0.16), Inches(height - 0.16))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_val = tf.paragraphs[0]
        p_val.text = val
        p_val.font.name = 'Arial'
        p_val.font.size = Pt(20)
        p_val.font.bold = True
        p_val.font.color.rgb = color
        p_val.alignment = PP_ALIGN.CENTER

        p_lbl = tf.add_paragraph()
        p_lbl.text = lbl
        p_lbl.font.name = 'Arial'
        p_lbl.font.size = Pt(9.5)
        p_lbl.font.bold = True
        p_lbl.font.color.rgb = TEXT_WHITE
        p_lbl.alignment = PP_ALIGN.CENTER

        if sub:
            p_sub = tf.add_paragraph()
            p_sub.text = sub
            p_sub.font.name = 'Arial'
            p_sub.font.size = Pt(8)
            p_sub.font.color.rgb = TEXT_MUTED
            p_sub.alignment = PP_ALIGN.CENTER

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    print("Building 32 Executive Slides for UniversityERP...")

    # =========================================================================
    # SLIDE 1: Title Slide & Platform Overview
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative Tech Grids
    grid = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.8))
    grid.fill.solid()
    grid.fill.fore_color.rgb = CARD_BG
    grid.line.color.rgb = CARD_BORDER
    grid.line.width = Pt(1.5)

    # Platform Category Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(1.2), Inches(4.5), Inches(0.35))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 58, 138)
    pill.line.color.rgb = ACCENT_BLUE
    tf_p = pill.text_frame
    p_p = tf_p.paragraphs[0]
    p_p.text = "ENTERPRISE CAMPUS OPERATING SYSTEM (CAMPUS OS)"
    p_p.font.name = 'Arial'
    p_p.font.size = Pt(9.5)
    p_p.font.bold = True
    p_p.font.color.rgb = ACCENT_BLUE
    p_p.alignment = PP_ALIGN.CENTER

    # Main Title
    tb_title = s1.shapes.add_textbox(Inches(1.3), Inches(1.7), Inches(10.7), Inches(1.8))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p1 = tf_t.paragraphs[0]
    p1.text = "UniversityERP"
    p1.font.name = 'Arial'
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_WHITE

    p2 = tf_t.add_paragraph()
    p2.text = "Unified Higher Education Operating System & Enterprise Architecture Blueprint"
    p2.font.name = 'Arial'
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = ACCENT_BLUE

    p3 = tf_t.add_paragraph()
    p3.text = "Authoritative 20-Year Principal Enterprise Architect Blueprint • Next-Gen Cloud Native Campus Infrastructure"
    p3.font.name = 'Arial'
    p3.font.size = Pt(11)
    p3.font.color.rgb = TEXT_MUTED

    # Metrics Banner
    m_data = [
        ("14", "Domain Modules", "01 Auth to 14 Analytics", ACCENT_BLUE),
        ("24", "System Roles", "SuperAdmin to Alumni", ACCENT_GREEN),
        ("138", "Prisma Models", "10 Domain Relational Clusters", ACCENT_AMBER),
        ("71", "API Controllers", "43 Modular Backend Services", ACCENT_PURPLE),
        ("49", "Frontend Pages", "React 18 SPA Suite", ACCENT_ROSE)
    ]
    add_metrics_banner(s1, 1.3, 3.8, 10.7, 1.1, m_data)

    # Tech Stack Badges
    tb_tech = s1.shapes.add_textbox(Inches(1.3), Inches(5.1), Inches(10.7), Inches(1.0))
    tf_tech = tb_tech.text_frame
    tf_tech.word_wrap = True
    p_tech1 = tf_tech.paragraphs[0]
    p_tech1.text = "CORE TECHNOLOGIES & STATUTORY FOUNDATION"
    p_tech1.font.name = 'Arial'
    p_tech1.font.size = Pt(10)
    p_tech1.font.bold = True
    p_tech1.font.color.rgb = TEXT_WHITE

    p_tech2 = tf_tech.add_paragraph()
    p_tech2.text = "React 18 • Vite • Tailwind CSS • NestJS 10 • TypeScript • PostgreSQL 16 • Prisma ORM • Redis 7 • Razorpay • TRAI DLT • DigiLocker / ABC / APAAR • Biometrics IoT • S3"
    p_tech2.font.name = 'Arial'
    p_tech2.font.size = Pt(10.5)
    p_tech2.font.color.rgb = ACCENT_BLUE

    # Footer Metadata
    tx_meta = s1.shapes.add_textbox(Inches(0.8), Inches(6.8), Inches(11.7), Inches(0.4))
    tf_meta = tx_meta.text_frame
    p_m = tf_meta.paragraphs[0]
    p_m.text = "Produced by Principal Enterprise Architect | National Education Policy (NEP 2020) & NAAC / NBA / NIRF Compliant"
    p_m.font.name = 'Arial'
    p_m.font.size = Pt(9.5)
    p_m.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: Executive Summary & Strategic Value Proposition
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "EXECUTIVE STRATEGY", "Executive Summary: The Unified Campus Paradigm Shift", 
               "Transforming fragmented point solutions into a cohesive, high-performance institutional operating system", 2)

    c1 = [
        ("Legacy Point Solutions", "Unconnected silos for admissions, LMS, exams, and accounts causing data discrepancies."),
        ("Manual Friction & Lag", "Spreadsheets, manual paper registers, and human reconciliation leading to revenue leakage."),
        ("Compliance Vulnerability", "Difficulty assembling verified evidence for NAAC SSR, NBA OBE, NIRF, and AICTE/UGC."),
        ("Astronomical TCO", "Exorbitant licensing, implementation fees, and rigid lock-in of legacy Tier-1 ERP suites.")
    ]
    add_card(s2, 0.8, 1.9, 3.7, 4.9, "1. The Institutional Dilemma", c1, ACCENT_ROSE, "Challenges of Legacy University ERPs")

    c2 = [
        ("Unified System of Record", "All academic, financial, operational, and student data unified in a single relational schema."),
        ("Automated Workflows", "Multi-tier approval chains, SLA enforcement, and automated trigger-based notifications."),
        ("Statutory First Design", "Native alignment with NEP 2020, CBCS credits, APAAR/ABC syncing, and TRAI DLT compliance."),
        ("Zero Vendor Lock-in", "Clean modern stack (TypeScript, NestJS, React, PostgreSQL) designed for long-term self-sovereignty.")
    ]
    add_card(s2, 4.8, 1.9, 3.7, 4.9, "2. The UniversityERP Solution", c2, ACCENT_BLUE, "Next-Generation Operating Architecture")

    c3 = [
        ("65% Cost Reduction", "Significant drop in operational administrative overhead and paper processing costs."),
        ("100% Revenue Integrity", "Zero fee leakage via automated billing, Razorpay dual verification, and double-entry ledger."),
        ("4x Faster Accreditation", "Instant quantitative data compilation for NAAC SSR Criteria 1-7 and NBA CO-PO attainment."),
        ("99.95% Availability", "Stateless horizontal scaling with Redis caching and automated multi-AZ PostgreSQL replication.")
    ]
    add_card(s2, 8.8, 1.9, 3.7, 4.9, "3. Measurable Strategic ROI", c3, ACCENT_GREEN, "Quantifiable Institutional Value")

    # =========================================================================
    # SLIDE 3: Enterprise Architecture & Technical Topology (C4 Model)
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "ENTERPRISE ARCHITECTURE", "System Architecture & C4 Technical Topology", 
               "Microservices-ready modular monolith with strict layer decoupling, zero-trust security, and high availability", 3)

    t1 = [
        ("React 18 SPA Suite", "Vite build tool, dynamic component routing, role-scoped sidebar navigation."),
        ("State & Interaction", "React hooks, optimistic UI updates, responsive Tailwind CSS grid layouts."),
        ("Visual Engines", "Interactive Canvas Document Designer, drag-and-drop timetable, seat matrix."),
        ("Client Security", "Zero storage of sensitive credentials, HttpOnly auth tokens, XSS/CSRF mitigation.")
    ]
    add_card(s3, 0.8, 1.9, 2.75, 4.9, "Frontend Layer (Client)", t1, ACCENT_BLUE, "49 Administrative & Portal Pages")

    t2 = [
        ("NestJS 10 Framework", "TypeScript modular monolith structured into 43 isolated domain modules."),
        ("Robust Controller Layer", "71 Controllers exposing RESTful endpoints with OpenAPI/Swagger specifications."),
        ("Validation & Guards", "Class-validator DTO pipes, JWT authentication, RBAC effective union guards."),
        ("Interceptors & Filters", "Global exception handling, response formatting, and tamper-proof audit logging.")
    ]
    add_card(s3, 3.78, 1.9, 2.75, 4.9, "Application Layer (Core API)", t2, ACCENT_GREEN, "71 Controllers, 43 Modules")

    t3 = [
        ("PostgreSQL 16 Engine", "ACID compliant relational store hosting 138 Prisma models across 10 clusters."),
        ("Prisma 5.x ORM", "Type-safe database client, foreign key enforcement, connection pooling."),
        ("Redis 7 In-Memory Cache", "Session state, rate limiting counters, timetable and query result caching."),
        ("Transaction Boundaries", "Atomic rollback guarantees using prisma.$transaction on all financial ops.")
    ]
    add_card(s3, 6.76, 1.9, 2.75, 4.9, "Data & Persistence Layer", t3, ACCENT_AMBER, "138 Models, Redis & S3")

    t4 = [
        ("FinTech Gateway", "Razorpay payments, subscriptions, refunds, and HMAC-SHA256 webhooks."),
        ("Telecom (TRAI DLT)", "Approved DLT templates, Principal Entity ID, dynamic token substitution."),
        ("Academic Repositories", "DigiLocker, Academic Bank of Credits (ABC), and APAAR ID federation."),
        ("Hardware & Storage", "Biometric IoT attendance gateways, AWS S3 / MinIO pre-signed object store.")
    ]
    add_card(s3, 9.74, 1.9, 2.75, 4.9, "Statutory Gateways Layer", t4, ACCENT_PURPLE, "External Integrations & IoT")

    # =========================================================================
    # SLIDE 4: Master Domain Functional Matrix (14 Enterprise Modules)
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "FUNCTIONAL CATALOG", "Master Domain Functional Matrix: 14 Core Modules", 
               "Exhaustive coverage of every institutional operational unit with zero functional gaps", 4)

    m_headers = ["Module ID & Name", "Core Functional Capabilities", "Key Business Stakeholders", "Primary API Scope"]
    m_rows = [
        ["01 Auth & Access Control", "JWT auth, RBAC effective union, multi-tenant scoping, password lifecycle", "All 24 Roles, Security Admin", "/auth, /users, /roles"],
        ["02 Master Data & Structure", "Universities, campuses, departments, programs, batches, academic years", "UnivAdmin, InstAdmin, Registrar", "/master, /departments, /programs"],
        ["03 Academics & Timetable", "CBCS / NEP courses, syllabus versions, conflict-free timetable, attendance", "Dean, HOD, Faculty, Students", "/courses, /timetables, /attendance"],
        ["04 Admissions & Seat Master", "Multi-channel leads, merit list engine, seat matrix, enrollment onboarding", "Admission Approver, Registrar", "/admissions, /seat-master, /leads"],
        ["05 Exams & CBE Engine", "Exam scheduling, anonymous codes, admit cards, marks lock, CBE engine", "COE, Evaluators, Students", "/exams, /cbe, /grading"],
        ["06 Fees & Financial Ops", "Fee structures, invoicing, Razorpay dual verify, double-entry ledger, refunds", "Finance Head, Accounts Officer", "/fees, /payments, /ledger"],
        ["07 Campus Facilities", "Hostel rooms & mess, fleet transit & QR bus passes, RFID library circulation", "Warden, Transport Head, Librarian", "/hostel, /transport, /library"],
        ["08 HR & Faculty Leaves", "Staff profiles, biometric shift logs, multi-tier leave approval, proxy balance", "HR Head, Deans, All Staff", "/hr, /leaves, /staff"],
        ["09 Health & Counselling", "Clinic EHR, prescription dispensing, confidential AES-256 counselling notes", "Medical Officer, Counsellor", "/clinic, /counselling"],
        ["10 Documents & Stock", "Canvas document designer, encrypted QR verify, pre-printed stock tracking", "Document Issuer, Registrar", "/documents, /certificates"],
        ["11 Dynamic Forms & Surveys", "Drag-and-drop form builder, public surveys, NAAC feedback collection", "Accreditation Officer, Deans", "/forms, /surveys, /responses"],
        ["12 Workflow & Approvals", "Visual workflow builder, SLA timeout escalation, multi-stage approval chains", "Registrar, Deans, Admin Staff", "/workflows, /approvals"],
        ["13 Governance & Audit", "DLT SMS templates, security policies, tamper-proof audit trail, backup/restore", "SuperAdmin, Compliance Officer", "/governance, /audit-logs, /system"],
        ["14 Institutional Analytics", "Executive Cockpit, real-time enrollment/finance KPIs, NAAC SSR aggregations", "Chancellor, Vice-Chancellor, Dean", "/analytics/exec, /reports"]
    ]
    add_table_slide(s4, 0.8, 1.9, 11.733, 4.9, m_headers, m_rows, [2.5, 4.8, 2.5, 1.933])

    # =========================================================================
    # SLIDE 5: End-to-End Student Lifecycle Journey (11 Stages)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "STUDENT LIFECYCLE", "The End-to-End Student Lifecycle Journey: 11 Stages", 
               "From initial prospect inquiry to alumni status — complete lifecycle governance with automated accountability", 5)

    stages_row1 = [
        ("01. Lead Ingestion", "Multi-channel capture, UTM attribution, automated CRM scoring.", ACCENT_BLUE),
        ("02. Scrutiny & Merit", "Document verification, 48h defect cure timer, category quota merit list.", ACCENT_GREEN),
        ("03. Fee Generation", "Finance Head assigns fee structure, quota billing, concession deduction.", ACCENT_AMBER),
        ("04. Dual-Verify Pay", "Razorpay checkout, HMAC-SHA256 signature check, double-entry ledger.", ACCENT_PURPLE)
    ]
    for idx, (st_t, st_d, col) in enumerate(stages_row1):
        add_card(s5, 0.8 + idx * 2.98, 1.9, 2.8, 2.3, st_t, [st_d], col)

    stages_row2 = [
        ("05. Seat Allocation", "Statutory intake check, batch/section assignment, roll number generation.", ACCENT_ROSE),
        ("06. Academic Execution", "CBCS / NEP curriculum, dynamic timetable, biometric attendance (75% rule).", ACCENT_INDIGO),
        ("07. Examination & CBE", "Anonymous roll numbers, admit cards, marks lock, 3-tier moderation.", ACCENT_BLUE),
        ("08. Certificate Stock", "Canvas designer, pre-printed serial security paper, tamper-proof vector QR.", ACCENT_GREEN)
    ]
    for idx, (st_t, st_d, col) in enumerate(stages_row2):
        add_card(s5, 0.8 + idx * 2.98, 4.4, 2.8, 2.4, st_t, [st_d], col)

    # =========================================================================
    # SLIDE 6: Admissions, Lead Funnel & Seat Master Governance
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "ADMISSIONS ENGINE", "Admissions, Lead Funnel & Seat Master Governance", 
               "Enforcing statutory approved intake, reservation quotas, and transparent merit list generation", 6)

    c_adm1 = [
        ("Omnichannel Capture", "Inquiries from website, social ads, education portals, and walk-in front desk."),
        ("Lead Scoring & Nurturing", "Automated DLT SMS reminders, counselor call logs, and conversion tracking."),
        ("Application Form Engine", "Dynamic field builder, multi-step validation, and document attachment upload."),
        ("Application Fee Settlement", "Online application fee collection with instant receipt generation.")
    ]
    add_card(s6, 0.8, 1.9, 3.7, 4.9, "Lead Funnel & Application", c_adm1, ACCENT_BLUE, "Inquiry to Application Scrutiny")

    c_adm2 = [
        ("48h Defect Cure Window", "Scrutiny officer marks deficiencies; applicant gets 48h to upload corrected files."),
        ("Category Quota Engine", "Automated ranking across General, OBC, SC, ST, EWS, and Institutional Quotas."),
        ("Normalization & Cutoffs", "Board percentage normalization, entrance exam weighting, tie-breaking rules."),
        ("Provisional Offer Letters", "Automated generation of admission offers with expiry countdown timers.")
    ]
    add_card(s6, 4.8, 1.9, 3.7, 4.9, "Scrutiny & Merit Engine", c_adm2, ACCENT_GREEN, "Transparent Verification & Selection")

    c_adm3 = [
        ("Statutory Seat Ceiling", "Hard cap enforcement preventing admissions beyond AICTE/UGC approved intake."),
        ("Batch & Section Matrix", "Subdividing approved intake into manageable batch sizes and lab sections."),
        ("Roll Number Allocation", "Automated sequential institutional roll number and matriculation numbering."),
        ("Statutory XLSX/PDF Export", "Single-click export of statutory seat allotment matrix for regulatory audits.")
    ]
    add_card(s6, 8.8, 1.9, 3.7, 4.9, "Seat Master & Matriculation", c_adm3, ACCENT_AMBER, "Statutory Intake Compliance")

    # =========================================================================
    # SLIDE 7: Fee Structures, Invoicing & Razorpay Integration
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "FINANCE & BILLING", "Fee Structures, Invoicing & Razorpay Integration", 
               "End-to-end institutional financial operations with dual-verification gateway and double-entry accounting", 7)

    c_fee1 = [
        ("Finance Head Governance", "Only authorized Finance Officers can configure fee heads and fee structures."),
        ("Granular Fee Heads", "Tuition, Lab, Library, Hostel, Transport, Examination, Caution Deposit."),
        ("Cohort-Based Pricing", "Structures assigned by Academic Year, Program, Batch, and Admission Quota."),
        ("Concessions & Waivers", "Merit scholarships, sibling discounts, and sports quota waiver approvals.")
    ]
    add_card(s7, 0.8, 1.9, 3.7, 4.9, "Fee Structure Configuration", c_fee1, ACCENT_BLUE, "Setup by Finance Leadership")

    c_fee2 = [
        ("Automated Term Invoicing", "Scheduled fee bill generation with configurable early-bird and late penalty rules."),
        ("Dual Gateway Verification", "Webhook signature (HMAC-SHA256) check PLUS direct Razorpay API order verify."),
        ("Omnichannel Cashiering", "Supports online card/UPI/net-banking, offline DD, bank challan, and POS receipts."),
        ("Reconciliation Engine", "Automated bank settlement reconciliation, chargeback tracking, and refund ledger.")
    ]
    add_card(s7, 4.8, 1.9, 3.7, 4.9, "Billing & Payment Gateway", c_fee2, ACCENT_GREEN, "Razorpay & Cashiering Operations")

    c_fee3 = [
        ("Double-Entry Accounting", "Every transaction creates paired debit and credit entries ensuring perfect balance."),
        ("Defaulter Management", "Automated DLT SMS payment reminders, hall ticket holds for chronic defaulters."),
        ("Late Fee Waiver Audit", "Role-restricted waiver approval workflow with mandatory reason logging."),
        ("Instant PDF Receipts", "Tamper-proof digital receipts with transaction ID, QR code, and breakdown.")
    ]
    add_card(s7, 8.8, 1.9, 3.7, 4.9, "Ledger & Financial Control", c_fee3, ACCENT_AMBER, "Zero Revenue Leakage Guarantee")

    # =========================================================================
    # SLIDE 8: Academic Curriculum, CBCS & NEP 2020 Governance
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "ACADEMIC GOVERNANCE", "Academic Curriculum, CBCS & NEP 2020 Governance", 
               "Next-gen curriculum structure supporting multi-disciplinary education, credit banking, and flexible electives", 8)

    c_acad1 = [
        ("CBCS & NEP Compliance", "Full support for Major, Minor, Open Elective, and Ability Enhancement courses."),
        ("Credit Framework", "Granular Lecture (L), Tutorial (T), and Practical (P) credit distribution rules."),
        ("Prerequisite Chains", "Hard and soft prerequisite course validations during student semester registration."),
        ("Syllabus Versioning", "Academic Council approval workflows for syllabus revisions and course objectives.")
    ]
    add_card(s8, 0.8, 1.9, 3.7, 4.9, "Curriculum & Course Master", c_acad1, ACCENT_BLUE, "NEP 2020 Multi-Disciplinary Tracks")

    c_acad2 = [
        ("Elective Selection Window", "Configurable student registration windows with real-time seat quota counters."),
        ("Minimum Enrollment Rules", "Automatic elective consolidation if enrollment falls below minimum threshold."),
        ("Batch & Lab Partitioning", "Splitting large lecture cohorts into smaller lab sections for hands-on sessions."),
        ("Credit Ceiling Controls", "Enforcing minimum and maximum semester credit limits per degree regulation.")
    ]
    add_card(s8, 4.8, 1.9, 3.7, 4.9, "Course Enrollment Engine", c_acad2, ACCENT_GREEN, "Student Self-Service Registration")

    c_acad3 = [
        ("Conflict-Free Scheduling", "Automated timetable generator preventing faculty, room, and student clashes."),
        ("Faculty Workload Balancing", "Monitoring weekly teaching hours against statutory UGC/AICTE norms."),
        ("Room Capacity Optimization", "Matching classroom physical capacity with enrolled cohort sizes."),
        ("Visual Timetable Grid", "Interactive drag-and-drop grid with real-time collision detection.")
    ]
    add_card(s8, 8.8, 1.9, 3.7, 4.9, "Timetable Engine", c_acad3, ACCENT_AMBER, "Optimized Campus Resource Scheduling")

    # =========================================================================
    # SLIDE 9: Student Attendance & Faculty Operations
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "ATTENDANCE OPERATIONS", "Student Attendance & Faculty Operations", 
               "Real-time attendance tracking, statutory 75% rule enforcement, and seamless faculty proxy management", 9)

    c_att1 = [
        ("1-Click Faculty Marking", "Responsive mobile/tablet UI for fast in-classroom attendance logging."),
        ("Biometric IoT Integration", "Direct integration with fingerprint and facial recognition turnstiles."),
        ("Period-Wise vs Daily Mode", "Configurable institutional attendance modes based on program requirements."),
        ("Late Entry & Tardy Tracking", "Distinguishing between excused absences, unexcused absences, and late arrivals.")
    ]
    add_card(s9, 0.8, 1.9, 3.7, 4.9, "Attendance Capture Modes", c_att1, ACCENT_BLUE, "Multi-Channel Verification")

    c_att2 = [
        ("75% Statutory Rule", "Continuous dynamic calculation of attendance percentages against statutory minimums."),
        ("Attendance Health Gauge", "Color-coded visual indicator on student and parent portal dashboards."),
        ("Automated Absentee Alerts", "Instant DLT-compliant SMS notifications sent to parents upon absence."),
        ("At-Risk Intervention", "Automated escalation of chronic absentees to academic counselors and mentors.")
    ]
    add_card(s9, 4.8, 1.9, 3.7, 4.9, "Statutory Enforcement", c_att2, ACCENT_ROSE, "UGC 75% Rule & Alerts")

    c_att3 = [
        ("Medical Condonation Workflow", "Digital medical certificate upload, HOD review, and Dean approval."),
        ("On-Duty (OD) Attendance", "Automatic attendance credit for authorized sports and cultural representations."),
        ("Faculty Proxy Management", "Automated proxy assignment when faculty take leave, preventing idle classes."),
        ("Hall Ticket Debarment", "Automated blocking of exam admit cards for students below threshold.")
    ]
    add_card(s9, 8.8, 1.9, 3.7, 4.9, "Condonation & Operations", c_att3, ACCENT_AMBER, "Workflow-Driven Clearances")

    # =========================================================================
    # SLIDE 10: Examination Management & Controller of Examinations (COE)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "EXAMINATION INTEGRITY", "Examination Management & Controller of Exams (COE)", 
               "Guaranteed exam integrity with anonymous barcoded roll numbers, 3-tier moderation, and marks lock", 10)

    c_coe1 = [
        ("Centralized Exam Scheduling", "Automated exam timetable generation with gap days between major subjects."),
        ("Seating Arrangement Engine", "Algorithmic desk allotment preventing adjacent students from same branch."),
        ("Hall Ticket / Admit Card", "Barcode-enabled digital admit cards with photo, venue, and eligibility rules."),
        ("Fee & Attendance Verification", "Automatic admit card generation only if attendance > 75% and fees cleared.")
    ]
    add_card(s10, 0.8, 1.9, 3.7, 4.9, "Exam Operations & Seating", c_coe1, ACCENT_BLUE, "Admit Cards & Hall Allotment")

    c_coe2 = [
        ("Identity Masking Engine", "Student roll numbers replaced with randomized encrypted barcoded codes."),
        ("Evaluator Blind Grading", "Faculty evaluate physical or digital answer books without knowing student identity."),
        ("Fictitious Number Decoding", "Only COE master key can decode anonymous marks back to student records."),
        ("Physical Security Paper", "Barcode stickers printed on tamper-evident synthetic security paper.")
    ]
    add_card(s10, 4.8, 1.9, 3.7, 4.9, "Anonymous Code Protection", c_coe2, ACCENT_PURPLE, "Zero Bias Evaluation Firewall")

    c_coe3 = [
        ("Continuous Assessment (CIA)", "Internal tests, assignments, and lab marks locked by Dean prior to end-sem."),
        ("3-Tier Marks Moderation", "Evaluator Entry -> Department Chief Scrutiny -> COE Board of Examiners Lock."),
        ("Relative & Absolute Grading", "Configurable grading scales (10-point UGC, percentage, Letter Grades A+ to F)."),
        ("Result Publication Firewall", "Staged result publishing with re-evaluation and retotalling request window.")
    ]
    add_card(s10, 8.8, 1.9, 3.7, 4.9, "Grading & Moderation", c_coe3, ACCENT_GREEN, "3-Tier Quality Assurance")

    # =========================================================================
    # SLIDE 11: Computer-Based Exam (CBE) & Digital Proctoring
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "DIGITAL ASSESSMENT", "Computer-Based Exam (CBE) & Digital Proctoring", 
               "Secure browser lockdown, Bloom's taxonomy question banks, and automated psychometric evaluation", 11)

    c_cbe1 = [
        ("Fullscreen Browser Lockdown", "Forced fullscreen mode disabling clipboard, right-click, and developer tools."),
        ("Tab-Switch Detection", "Real-time logging of focus loss; automated test auto-submission after 3 warnings."),
        ("Webcam Snapshot Verification", "Periodic random webcam capture to verify candidate presence."),
        ("Bandwidth Resilient State", "Client-side offline answer caching ensuring zero data loss during network blips.")
    ]
    add_card(s11, 0.8, 1.9, 3.7, 4.9, "Proctored Exam Engine", c_cbe1, ACCENT_ROSE, "Secure Browser Environment")

    c_cbe2 = [
        ("Bloom's Taxonomy Tagging", "Questions categorized by Remember, Understand, Apply, Analyze, Evaluate, Create."),
        ("Item Difficulty Index (P)", "Automated statistical calculation of question pass rate and difficulty level."),
        ("Discrimination Index (D)", "Differentiating high-performing from low-performing students for question curation."),
        ("Rich Media Support", "Supports LaTeX mathematical formulas, code blocks, diagrams, and audio clips.")
    ]
    add_card(s11, 4.8, 1.9, 3.7, 4.9, "Question Bank Psychometrics", c_cbe2, ACCENT_BLUE, "Standardized Item Banking")

    c_cbe3 = [
        ("Instant Auto-Evaluation", "Real-time grading for MCQs, multiple-select, fill-in-blanks, and matching items."),
        ("Rubrics-Based Subjective", "Standardized rubrics grading for long essays and descriptive case studies."),
        ("Negative Marking Rules", "Configurable fractional negative marking for competitive entrance exams."),
        ("Post-Exam Analytics", "Instant question-wise success heatmaps and distractor efficiency reports.")
    ]
    add_card(s11, 8.8, 1.9, 3.7, 4.9, "Evaluation & Analytics", c_cbe3, ACCENT_GREEN, "Automated Scoring & Insights")

    # =========================================================================
    # SLIDE 12: Visual Document Designer & Certificate Stock Security
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "CREDENTIAL GOVERNANCE", "Visual Document Designer & Certificate Stock Security", 
               "Canvas document creator with anti-counterfeit QR verification and pre-printed security paper serial tracking", 12)

    c_doc1 = [
        ("Visual Drag-and-Drop Canvas", "Design degree certificates, provisional certs, grade cards, and bonafide letters."),
        ("Student Details Pair Layouts", "Flexible field pairing (e.g. Roll No + CGPA, Father Name + DOB)."),
        ("Custom Typography & Borders", "Custom fonts, official university seals, watermarks, and micro-text borders."),
        ("Reusable Document Templates", "Institutional template repository with role-based editing permissions.")
    ]
    add_card(s12, 0.8, 1.9, 3.7, 4.9, "Canvas Document Designer", c_doc1, ACCENT_BLUE, "WYSIWYG Layout Engine")

    c_doc2 = [
        ("Dynamic Replacement Tokens", "Instant token injection: {{student.name}}, {{course.title}}, {{exam.cgpa}}."),
        ("Vector Encrypted QR Codes", "High-density QR containing digitally signed payload for offline verification."),
        ("Public Verification Portal", "Employers scan QR or visit portal to verify authenticity without logging in."),
        ("Tamper-Evident Signatures", "Cryptographic hash generated per document preventing retrospective alterations.")
    ]
    add_card(s12, 4.8, 1.9, 3.7, 4.9, "Tokens & Public Verification", c_doc2, ACCENT_GREEN, "Instant Anti-Counterfeit Validation")

    c_doc3 = [
        ("Physical Security Paper Master", "Tracking incoming inventory of watermarked, pre-printed numbered paper."),
        ("Sequential Serial Allocation", "Mandatory serial number prompt before printing; logs exact sheet used."),
        ("Damaged Stock Audit Trail", "Requires damaged sheet scan and supervisor reason code for spoilage audit."),
        ("Issuer Identity Stamping", "Every printed certificate stamped with issuer user ID and exact timestamp.")
    ]
    add_card(s12, 8.8, 1.9, 3.7, 4.9, "Security Paper Stock Tracking", c_doc3, ACCENT_AMBER, "Zero Certificate Leakage")

    # =========================================================================
    # SLIDE 13: Campus Facilities — Hostel & Residential Life
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "CAMPUS OPERATIONS", "Campus Facilities: Hostel & Residential Life Management", 
               "Comprehensive residential governance from room matrix inventory to digital gate passes and curfew logs", 13)

    c_hos1 = [
        ("Multi-Block Hierarchy", "Hostel Block -> Floors -> Rooms -> Beds hierarchy with gender-segregated zones."),
        ("Room Typologies", "AC, Non-AC, Single, Double, Triple, and Attached-Bathroom room configurations."),
        ("Real-Time Occupancy Grid", "Color-coded visual bed matrix showing vacant, occupied, and maintenance beds."),
        ("Automated Room Allocation", "Rules-based bed allocation based on student preference, merit, or seniority.")
    ]
    add_card(s13, 0.8, 1.9, 3.7, 4.9, "Room Matrix & Inventory", c_hos1, ACCENT_BLUE, "Bed-Level Inventory Management")

    c_hos2 = [
        ("Digital Gate-Pass Requests", "Student applies for day-out or night-out passes via mobile app."),
        ("Warden & Parent Dual Approval", "Automated SMS OTP confirmation sent to parents before warden sign-off."),
        ("Security Gate Biometric Scan", "Campus security guards verify pass QR code at campus entry/exit turnstiles."),
        ("Curfew Violation Monitoring", "Automated real-time notification to warden for students past curfew hour.")
    ]
    add_card(s13, 4.8, 1.9, 3.7, 4.9, "Gate Pass & Curfew Governance", c_hos2, ACCENT_PURPLE, "Student Safety & Parent Linkage")

    c_hos3 = [
        ("Mess Billing & Diet Opt-Out", "Subscription billing for student mess with planned absence fee rebates."),
        ("Room Inspection & Damages", "Warden room inspection logging; assessed damage charges billed to ledger."),
        ("Hostel Caution Deposit", "Automated deposit accounting and damage deduction upon vacating room."),
        ("Automated No Dues Clearance", "Instant digital clearance sign-off if room handed over and dues settled.")
    ]
    add_card(s13, 8.8, 1.9, 3.7, 4.9, "Mess, Damages & No Dues", c_hos3, ACCENT_AMBER, "Financial & Inventory Settlement")

    # =========================================================================
    # SLIDE 14: Campus Facilities — Fleet & Transport Logistics
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "FLEET LOGISTICS", "Campus Facilities: Fleet & Transport Logistics Management", 
               "Real-time fleet tracking, digital QR bus passes, route optimization, and student passenger manifests", 14)

    c_tr1 = [
        ("Vehicle Master Governance", "Tracking buses, vans, driver licenses, fitness certificates, and insurance expiry."),
        ("Route & Stop Optimization", "Configurable bus routes, geographic waypoints, and scheduled arrival timings."),
        ("Seat Capacity Enforcement", "Hard capacity limits preventing overcrowding; automated waitlist for full buses."),
        ("Fleet Maintenance Logs", "Tracking odometer readings, fuel consumption logs, and periodic service records.")
    ]
    add_card(s14, 0.8, 1.9, 3.7, 4.9, "Fleet & Route Management", c_tr1, ACCENT_BLUE, "Vehicle Master & Capacity")

    c_tr2 = [
        ("Dynamic QR Bus Passes", "Time-expiring encrypted QR pass generated on student mobile app upon fee payment."),
        ("Conductor Validation App", "Fast offline-capable QR scanner for bus conductors during boarding."),
        ("Real-Time Passenger Manifest", "Instant attendance logging of which students boarded which bus each morning."),
        ("Emergency SOS Alerts", "Driver and student panic button sending instant location alerts to security.")
    ]
    add_card(s14, 4.8, 1.9, 3.7, 4.9, "Digital Bus Passes & Safety", c_tr2, ACCENT_GREEN, "QR Ticketing & Boarding Control")

    c_tr3 = [
        ("Distance-Based Fee Slabs", "Automated fee calculation based on pickup stop distance from university campus."),
        ("Term Invoicing Integration", "Transport fees integrated seamlessly into student master fee ledger."),
        ("Temporary Route Change", "Self-service requests for temporary stop changes during exams or internships."),
        ("Transport No Dues Sign-Off", "Automated transport clearance upon pass surrender and zero fee arrears.")
    ]
    add_card(s14, 8.8, 1.9, 3.7, 4.9, "Billing & Transport Clearance", c_tr3, ACCENT_AMBER, "Automated Fee & No Dues Integration")

    # =========================================================================
    # SLIDE 15: Campus Facilities — Library & Resource Center (RFID)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    set_slide_background(s15)
    add_header(s15, "LIBRARY AUTOMATION", "Campus Facilities: Library & Resource Center (RFID)", 
               "Marc21 cataloging, RFID self-service circulation, automated overdue fine accounting, and digital repositories", 15)

    c_lib1 = [
        ("Marc21 / Dublin Core Cataloging", "International standard bibliographic metadata and Dewey decimal classification."),
        ("Multi-Copy Accessioning", "Individual barcode and RFID tag encoding for every physical copy on shelves."),
        ("E-Book & Journal Repositories", "Digital asset management, publisher link integration, and Open Access catalogs."),
        ("Departmental Sub-Libraries", "Centralized inventory tracking across departmental seminar libraries.")
    ]
    add_card(s15, 0.8, 1.9, 3.7, 4.9, "Bibliographic Cataloging", c_lib1, ACCENT_BLUE, "Standardized Library Inventory")

    c_lib2 = [
        ("RFID Self-Checkout Kiosk", "Students scan student ID and place multiple books on RFID pad for instant issue."),
        ("Smart Book Drop Station", "Automated book return chute with RFID detection and instant check-in confirmation."),
        ("Anti-Theft RFID Security Gates", "Audible alarm and security alerts if unissued books pass through library gates."),
        ("Circulation Rules Engine", "Configurable loan periods and borrowing limits by role (Student, Faculty, Scholar).")
    ]
    add_card(s15, 4.8, 1.9, 3.7, 4.9, "RFID Circulation Operations", c_lib2, ACCENT_GREEN, "Self-Service Kiosks & Gates")

    c_lib3 = [
        ("Automated Daily Fine Ledger", "Daily automated cron job calculating overdue fines against student accounts."),
        ("Book Hold & Reservation Queue", "Automated notification to student when reserved book is checked back in."),
        ("Lost Book Replacement Fee", "Replacement cost plus administrative processing charge billed to ledger."),
        ("Instant Library No Dues", "Automated clearance sign-off if all books returned and zero outstanding fines.")
    ]
    add_card(s15, 8.8, 1.9, 3.7, 4.9, "Overdue Fines & Clearance", c_lib3, ACCENT_AMBER, "Fines, Reservations & No Dues")

    # =========================================================================
    # SLIDE 16: Human Resources, Faculty & Leave Governance
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    set_slide_background(s16)
    add_header(s16, "HUMAN RESOURCES", "Human Resources, Faculty & Leave Governance", 
               "Complete faculty lifecycle, biometric shift scheduling, multi-tier leave approval, and proxy class arrangement", 16)

    c_hr1 = [
        ("Comprehensive Staff Master", "Faculty ranks (Professor, Associate, Assistant), contracts, and pay scales."),
        ("Academic Credentials Vault", "PhD thesis titles, UGC NET/SET scores, publications, and patent filings."),
        ("Statutory Faculty Ratios", "Automated monitoring of Student-to-Faculty Ratio (SFR) for NAAC & NBA compliance."),
        ("Service Book & Experience", "Digital service record tracking promotions, awards, and disciplinary history.")
    ]
    add_card(s16, 0.8, 1.9, 3.7, 4.9, "Faculty & Staff Master", c_hr1, ACCENT_BLUE, "Comprehensive Profile Governance")

    c_hr2 = [
        ("Biometric Shift Synchronization", "Direct sync with biometric turnstiles for in/out shift recording."),
        ("Flexible Shift Configurations", "Configurable morning, general, and evening shifts with grace periods."),
        ("Late Entry & Overtime Rules", "Automated tracking of half-day cuts and overtime allowances."),
        ("Monthly Payroll Attendance", "Export of verified monthly work hours directly into institutional payroll.")
    ]
    add_card(s16, 4.8, 1.9, 3.7, 4.9, "Shifts & Biometric Tracking", c_hr2, ACCENT_GREEN, "Accurate Time & Attendance")

    c_hr3 = [
        ("Configurable Leave Quotas", "Casual (CL), Sick (SL), Earned (EL), Duty (DL), and Sabbatical leave quotas."),
        ("Multi-Stage Approval Hierarchy", "Applicant -> HOD Review -> Dean Recommendation -> HR Approval."),
        ("Mandatory Class Proxy Arrangement", "Faculty must assign substitute teaching colleagues before leave submission."),
        ("Leave Encashment & Carryover", "Automated annual leave balance rollovers and encashment calculations.")
    ]
    add_card(s16, 8.8, 1.9, 3.7, 4.9, "Leave Engine & Proxy Workflows", c_hr3, ACCENT_AMBER, "Zero Disrupted Classrooms")

    # =========================================================================
    # SLIDE 17: Health Clinic, Counselling & Student Welfare
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    set_slide_background(s17)
    add_header(s17, "STUDENT WELFARE", "Campus Health Clinic, Counselling & Student Welfare", 
               "Confidential AES-256 encrypted psychological counselling notes, clinic EHR, and student mentorship", 17)

    c_wel1 = [
        ("Electronic Health Record (EHR)", "Student and staff outpatient visits, medical history, and allergy warnings."),
        ("Pharmacy Dispensing Ledger", "Campus clinic medicine inventory tracking and prescription dispensing logs."),
        ("Emergency Dispatch Integration", "Direct link to campus ambulance, local hospitals, and parent emergency SMS."),
        ("Medical Certificate Issuance", "Digital issuance of clinic rest slips linked to attendance condonation.")
    ]
    add_card(s17, 0.8, 1.9, 3.7, 4.9, "Campus Health Clinic", c_wel1, ACCENT_ROSE, "Primary Care & Medical Records")

    c_wel2 = [
        ("Zero-Knowledge AES-256 Encryption", "Counselling session notes encrypted at column level; inaccessible even to DBAs."),
        ("Confidential Appointment Booking", "Students can book confidential appointments without revealing reason to staff."),
        ("Mental Wellness Assessments", "Periodic standardized screening (PHQ-9, GAD-7) for early stress intervention."),
        ("Anonymized Crisis Escalation", "Emergency high-risk flags alerting Dean of Student Welfare without breach.")
    ]
    add_card(s17, 4.8, 1.9, 3.7, 4.9, "Psychological Counselling", c_wel2, ACCENT_PURPLE, "Encrypted Mental Health Support")

    c_wel3 = [
        ("Faculty Mentorship System", "Cohorts of 15-20 students assigned to faculty mentors for holistic guidance."),
        ("Anti-Ragging Committee Logs", "Statutory UGC anti-ragging compliance, affidavit tracking, and incident logging."),
        ("Grievance Redressal Portal", "Transparent grievance submission, committee review, and resolution SLAs."),
        ("Equal Opportunity Cell", "Monitoring assistance and scholarships for differently-abled and minority students.")
    ]
    add_card(s17, 8.8, 1.9, 3.7, 4.9, "Mentorship & Grievance Governance", c_wel3, ACCENT_BLUE, "Statutory Student Welfare")

    # =========================================================================
    # SLIDE 18: Student Exit Governance & 5-Department "No Dues" Clearance
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    set_slide_background(s18)
    add_header(s18, "EXIT GOVERNANCE", "Student Exit Governance & 5-Department 'No Dues' Clearance", 
               "Rigorous multi-department clearance workflow ensuring zero institutional loss prior to student departure", 18)

    c_ex1 = [
        ("Library Clearance (Dept 1)", "Validates all borrowed books returned and zero outstanding fine ledger balances."),
        ("Hostel Warden Clearance (Dept 2)", "Validates room physical inspection, keys handed over, and damage dues paid."),
        ("Transport Fleet Clearance (Dept 3)", "Validates bus pass cancellation and zero outstanding transport fee balances."),
        ("Department HOD Clearance", "Validates lab locker clearance, project equipment return, and seminar sign-off.")
    ]
    add_card(s18, 0.8, 1.9, 3.7, 4.9, "Operational Clearances (1-3)", c_ex1, ACCENT_BLUE, "Physical Asset & Key Return")

    c_ex2 = [
        ("Accounts & Finance (Dept 4)", "Audit of master ledger: tuition fees, hostel fees, fines, and caution deposits."),
        ("Caution Deposit Refund", "Automated refund voucher generation after netting off assessed damage charges."),
        ("Registrar Final Sign-Off (Dept 5)", "Unlocks TC, Migration Certificate, and final Degree Certificate upon all sign-offs."),
        ("Automated Hold Placements", "Any departmental rejection immediately blocks certificate generation system-wide.")
    ]
    add_card(s18, 4.8, 1.9, 3.7, 4.9, "Finance & Registrar Final Lock", c_ex2, ACCENT_GREEN, "Financial Balance & Final Sign-Off")

    c_ex3 = [
        ("Formal Cancellation Flow", "Student raises withdrawal request; requires parent consent and exit interview."),
        ("Dean Scrutiny & Comment", "Dean reviews justification, discusses retention options, and submits remarks."),
        ("Registrar Approval & Grace Period", "Approval sets 15-day deactivation grace period during which action is reversible."),
        ("Automated Ledger Refund", "Pro-rata tuition refund calculated based on UGC cancellation refund schedule.")
    ]
    add_card(s18, 8.8, 1.9, 3.7, 4.9, "Course Cancellation / Withdrawal", c_ex3, ACCENT_AMBER, "15-Day Reversible Deactivation")

    # =========================================================================
    # SLIDE 19: Degree Conferral, National Repositories & Alumni Network
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    set_slide_background(s19)
    add_header(s19, "DEGREE & ALUMNI", "Degree Conferral, National Repositories & Alumni Network", 
               "Automated convocation gazettes, DigiLocker / APAAR federation, and lifelong alumni engagement", 19)

    c_deg1 = [
        ("Degree Gazette Publication", "Official senate-approved degree gazette with CGPA, division, and honors roll."),
        ("Convocation Seating & Tokens", "Managing convocation guest registrations, robes issuance, and stage tokens."),
        ("Bilingual Certificate Generation", "Automated generation of degrees in English and official state/Hindi languages."),
        ("Transcript Issuance Portal", "Official authenticated transcripts sent directly to overseas universities via WES.")
    ]
    add_card(s19, 0.8, 1.9, 3.7, 4.9, "Degree Conferral & Convocation", c_deg1, ACCENT_BLUE, "Senate Gazette & Honors")

    c_deg2 = [
        ("National Academic Depository (NAD)", "Direct API sync pushing student degrees to Government of India NAD portal."),
        ("DigiLocker Integration", "Graduates access verifiable digital certificates instantly via their DigiLocker app."),
        ("Academic Bank of Credits (ABC)", "Automated credit balance push to student APAAR / ABC identity account."),
        ("Global Verification API", "Authorized background verification agencies query credentials via secure API.")
    ]
    add_card(s19, 4.8, 1.9, 3.7, 4.9, "DigiLocker, ABC & APAAR", c_deg2, ACCENT_PURPLE, "National Statutory Federation")

    c_deg3 = [
        ("Alumni Directory & Portal", "Graduates retain lifelong portal access with personal non-university email logins."),
        ("Mentorship & Placement Network", "Alumni offer internships, job referrals, and career webinars to current students."),
        ("Endowment & Donation Tracking", "Fundraising campaigns, scholarship endowments, and 80G tax receipt issuance."),
        ("Alumni Chapters & Reunions", "Managing regional alumni chapter events, election voting, and newsletters.")
    ]
    add_card(s19, 8.8, 1.9, 3.7, 4.9, "Lifelong Alumni Network", c_deg3, ACCENT_GREEN, "Endowment & Mentorship Ecosystem")

    # =========================================================================
    # SLIDE 20: Master Roles & Permissions Governance (24 System Roles)
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    set_slide_background(s20)
    add_header(s20, "ROLE GOVERNANCE", "Master Roles & Permissions Governance: 24 System Roles", 
               "Fine-grained role-based access control with effective union evaluation and multi-tenant boundary isolation", 20)

    r_headers = ["Persona Tier", "Specific System Roles", "Core Governance Scope", "Write Boundaries & Guards"]
    r_rows = [
        ["1. Executive Leadership", "SuperAdmin, UnivAdmin, InstAdmin", "Multi-tenant setup, institutions, campuses, global settings, audit logs", "Full Write on respective tenant; SuperAdmin has cross-tenant scope"],
        ["2. Academic Leadership", "Registrar, COE, Dean, HOD, Faculty", "Matriculation, curricula, exam timetables, marks locking, daily attendance", "Restricted to assigned Academic Entity; Faculty restricted to active courses"],
        ["3. Finance & Logistics", "Finance Head, Accounts Officer, Warden, Transport, Librarian", "Fee structures, cashiering, hostel rooms, bus routes, library RFID desk", "Finance restricted to ledger; Facilities restricted to asset inventories"],
        ["4. Specialized Officers", "Admission Approver, Document Issuer, Results Publisher, QuestionBank Approver", "Application scrutiny, canvas certificate printing, exam grading, item curation", "Workflow stage restricted; Document Issuer restricted to assigned stock"],
        ["5. Health & Welfare", "Campus Doctor, Psychological Counsellor, Welfare Officer", "Outpatient clinic EHR, confidential counselling notes, anti-ragging logs", "Zero-knowledge encryption for Counsellor; strict medical confidentiality"],
        ["6. End Users", "Applicant, Student, Parent, Alumni", "Application forms, course registration, fee payment, bus pass, credential verification", "Self-scoped only (id == req.user.id); Parent linked to student record"]
    ]
    add_table_slide(s20, 0.8, 1.9, 11.733, 4.9, r_headers, r_rows, [2.3, 3.2, 3.7, 2.533])

    # =========================================================================
    # SLIDE 21: Zero-Trust Security, Multi-Tenant Isolation & Audit Trails
    # =========================================================================
    s21 = prs.slides.add_slide(blank_layout)
    set_slide_background(s21)
    add_header(s21, "SECURITY ARCHITECTURE", "Zero-Trust Security, Multi-Tenant Isolation & Audit Trails", 
               "Enterprise-grade defense-in-depth security protecting institutional records and personal data", 21)

    c_sec1 = [
        ("JWT Stateless Tokens", "Short-lived access tokens (15m) paired with HttpOnly refresh tokens."),
        ("Argon2id Password Hashing", "State-of-the-art cryptographic password hashing resisting GPU cracking."),
        ("Session Invalidation Engine", "Instant session revocation upon password reset or security compromise."),
        ("Brute-Force Rate Limiting", "Redis-backed rate limiters on login and OTP verification endpoints.")
    ]
    add_card(s21, 0.8, 1.9, 3.7, 4.9, "Authentication & Tokens", c_sec1, ACCENT_BLUE, "Stateless & Secure Sessions")

    c_sec2 = [
        ("Row-Level Tenant Isolation", "Tenant and institution IDs injected into every Prisma query execution."),
        ("Zero Cross-Tenant Leakage", "Strict logical isolation guaranteeing university data privacy."),
        ("Granular Module Guards", "Requests checked against user's effective roles union (roles.util.ts)."),
        ("Write Guard Verification", "Read-only enforcement during fee freeze or marks lock windows.")
    ]
    add_card(s21, 4.8, 1.9, 3.7, 4.9, "Multi-Tenant Isolation", c_sec2, ACCENT_GREEN, "Strict Row-Level Partitioning")

    c_sec3 = [
        ("Tamper-Proof Audit Logging", "Every mutating HTTP action logged with Actor, IP, User-Agent, and Timestamp."),
        ("Before / After Diffs", "Deep JSON diffs of database state recorded for all financial and grading changes."),
        ("AES-256 Field Encryption", "Sensitive counselling notes and payment credentials encrypted at rest."),
        ("SOC 2 / ISO 27001 Ready", "Audit trails exported for annual enterprise compliance certifications.")
    ]
    add_card(s21, 8.8, 1.9, 3.7, 4.9, "Audit Logs & Cryptography", c_sec3, ACCENT_ROSE, "Immutable Accountability")

    # =========================================================================
    # SLIDE 22: Statutory Gateways & External Integrations Architecture
    # =========================================================================
    s22 = prs.slides.add_slide(blank_layout)
    set_slide_background(s22)
    add_header(s22, "INTEGRATIONS ARCHITECTURE", "Statutory Gateways & External Integrations Architecture", 
               "Seamless integration with national statutory portals, telecom DLT gateways, banking, and IoT hardware", 22)

    g1 = [
        ("Payment Processing", "Orders API, Checkout SDK, and Subscriptions."),
        ("Webhook Dual Verify", "HMAC-SHA256 signature verification on event."),
        ("Automated Reconciliation", "Server-to-server query confirms bank capture."),
        ("Idempotent Transactions", "Idempotency key prevents duplicate billing.")
    ]
    add_card(s22, 0.8, 1.9, 2.75, 4.9, "1. FinTech: Razorpay", g1, ACCENT_BLUE, "Banking & Payments")

    g2 = [
        ("TRAI DLT Compliance", "Principal Entity ID & Registered Sender IDs."),
        ("Approved Templates", "DLT approved SMS text with dynamic tokens."),
        ("Priority Routing", "OTP messages dispatched via transactional route."),
        ("Delivery Telemetry", "Carrier delivery status logged to database.")
    ]
    add_card(s22, 3.78, 1.9, 2.75, 4.9, "2. Telecom: TRAI DLT", g2, ACCENT_GREEN, "SMS Gateway Engine")

    g3 = [
        ("NAD Push Integration", "Conferred degrees pushed to national depository."),
        ("DigiLocker Pull API", "Graduates fetch official certificates via app."),
        ("APAAR / ABC Credits", "Student academic credits synced automatically."),
        ("XML/JSON Schemas", "Conforms to National Academic Exchange norms.")
    ]
    add_card(s22, 6.76, 1.9, 2.75, 4.9, "3. National Repositories", g3, ACCENT_AMBER, "DigiLocker & ABC")

    g4 = [
        ("Biometric Turnstiles", "IoT push gateways for fingerprint and facial gates."),
        ("AWS S3 / MinIO Store", "Pre-signed URLs for secure document attachments."),
        ("GPS Telematics", "Transit bus GPS trackers sending coordinates."),
        ("RFID Readers", "High-frequency RFID readers for library kiosks.")
    ]
    add_card(s22, 9.74, 1.9, 2.75, 4.9, "4. IoT & Cloud Storage", g4, ACCENT_PURPLE, "Hardware & Object Store")

    # =========================================================================
    # SLIDE 23: Relational Database Architecture (138 Models, 10 Clusters)
    # =========================================================================
    s23 = prs.slides.add_slide(blank_layout)
    set_slide_background(s23)
    add_header(s23, "DATA ARCHITECTURE", "Relational Database Architecture: 138 Models across 10 Clusters", 
               "PostgreSQL 16 relational data topology mapped via Prisma ORM with strict referential integrity", 23)

    db_headers = ["Functional Cluster", "Prisma Models Count", "Representative Core Entities", "Referential Integrity & Constraints"]
    db_rows = [
        ["1. Auth & Access Control", "12 Models", "User, Role, UserRole, Permission, Session, AuditLog, RefreshToken", "Cascade deletes on sessions; User soft-delete flags"],
        ["2. Master Structure", "14 Models", "University, Campus, Department, Program, AcademicYear, Term, Batch", "Strict hierarchical foreign keys (Univ -> Campus -> Dept)"],
        ["3. Admissions & Leads", "15 Models", "Lead, Application, AdmissionQuota, MeritList, ScrutinyRecord, SeatMatrix", "Unique constraints on ApplicationNumber and Email/Phone"],
        ["4. Academics & Timetable", "20 Models", "Course, CourseVersion, Prerequisite, Timetable, TimetableSlot, Attendance", "Unique slot constraints preventing room & faculty collisions"],
        ["5. Examinations & CBE", "18 Models", "ExamSchedule, AdmitCard, AnonymousCode, CIAMark, Question, CBEAttempt", "Immutable marks once locked; AnonymousCode salted mapping"],
        ["6. Fees & Financial Ops", "16 Models", "FeeStructure, FeeHead, Invoice, Payment, TransactionLedger, Refund", "Double-entry balance verification; zero negative balances"],
        ["7. Campus Logistics", "15 Models", "HostelBlock, Room, Bed, GatePass, BusRoute, Vehicle, Book, BorrowRecord", "Bed occupancy status machine; RFID accession unique indexes"],
        ["8. HR & Faculty Leaves", "12 Models", "StaffProfile, StaffShift, LeaveBalance, LeaveRequest, ProxyArrangement", "Leave deduction atomic transactions; shift overlap checks"],
        ["9. Health & Welfare", "6 Models", "ClinicVisit, Prescription, CounsellingCase, MentorshipCohort, Grievance", "AES-256 encrypted confidential notes; zero foreign key leaks"],
        ["10. Documents & Forms", "10 Models", "DocumentTemplate, CertificateStock, DynamicForm, FormResponse, DltTemplate", "Pre-printed serial number unique index; stock damaged audits"]
    ]
    add_table_slide(s23, 0.8, 1.9, 11.733, 4.9, db_headers, db_rows, [2.5, 1.8, 4.5, 2.933])

    # =========================================================================
    # SLIDE 24: Backend API Architecture (71 Controllers, 43 Modules)
    # =========================================================================
    s24 = prs.slides.add_slide(blank_layout)
    set_slide_background(s24)
    add_header(s24, "BACKEND ARCHITECTURE", "Backend API Architecture: 71 Controllers across 43 Modules", 
               "NestJS enterprise service catalog with standard REST verbs, class-validator DTOs, and OpenAPI docs", 24)

    c_api1 = [
        ("Standard RESTful Verbs", "Uniform resource endpoints: GET (query), POST (create), PUT/PATCH (update), DELETE."),
        ("Strict DTO Validation", "Every incoming payload validated by NestJS ValidationPipe using class-validator."),
        ("OpenAPI / Swagger 3.0", "Complete interactive API documentation generated automatically at /api/docs."),
        ("Idempotency Keys", "Financial and registration endpoints enforce UUID idempotency keys to prevent repeats.")
    ]
    add_card(s24, 0.8, 1.9, 3.7, 4.9, "Design Standards & Contracts", c_api1, ACCENT_BLUE, "Predictable RESTful Endpoints")

    c_api2 = [
        ("Decoupled NestJS Modules", "43 isolated modules ensuring clean separation of concerns and maintainability."),
        ("Dependency Injection (DI)", "Service layers injected via DI tokens, enabling painless unit and e2e testing."),
        ("Database Transaction Boundaries", "All multi-table mutations wrapped in atomic prisma.$transaction blocks."),
        ("Event-Driven Side Effects", "Asynchronous events trigger DLT SMS, emails, and audit logs without latency.")
    ]
    add_card(s24, 4.8, 1.9, 3.7, 4.9, "Service & Business Logic Layer", c_api2, ACCENT_GREEN, "Modular Monolith Architecture")

    c_api3 = [
        ("Unified Exception Filter", "Standard error envelope { statusCode, message, timestamp, path } across all errors."),
        ("Response Serialization", "Interceptors strip out internal database fields and password hashes before return."),
        ("Performance Telemetry", "Logging interceptor records execution duration (ms) for slow query optimization."),
        ("Rate Limiting Throttler", "DDoS mitigation and IP-based request throttling on public endpoints.")
    ]
    add_card(s24, 8.8, 1.9, 3.7, 4.9, "Resilience & Cross-Cutting", c_api3, ACCENT_AMBER, "Filters, Interceptors & Telemetry")

    # =========================================================================
    # SLIDE 25: Frontend Architecture & User Experience (49 React Pages)
    # =========================================================================
    s25 = prs.slides.add_slide(blank_layout)
    set_slide_background(s25)
    add_header(s25, "FRONTEND ARCHITECTURE", "Frontend Architecture & User Experience: 49 React Pages", 
               "Modern React 18 single-page application engineered for high-density academic operations and speed", 25)

    c_ui1 = [
        ("React 18 & Vite Tooling", "Sub-second hot module replacement (HMR) and lightning-fast production bundles."),
        ("Dynamic Breadcrumb Routing", "React Router v6 with hierarchical pathing reflecting academic structures."),
        ("Role-Scoped Navigation", "Sidebar menus dynamically rendered based on user's active permissions union."),
        ("Responsive Layout Engine", "Tailwind CSS responsive design supporting high-res desktops, laptops, and tablets.")
    ]
    add_card(s25, 0.8, 1.9, 3.7, 4.9, "Core Architecture & Routing", c_ui1, ACCENT_BLUE, "Single-Page Application (SPA)")

    c_ui2 = [
        ("Canvas Document Designer", "Visual drag-and-drop certificate layout engine with real-time vector preview."),
        ("Interactive Seat Matrix", "Live quota capacity grids with instant XLSX/PDF export and batch row filters."),
        ("Page-Level Gear Modals", "Dedicated modal configuration gear (e.g. Fees page gateway settings)."),
        ("Drag-and-Drop Timetable", "Visual slot allocation matrix with collision prevention and teacher load gauges.")
    ]
    add_card(s25, 4.8, 1.9, 3.7, 4.9, "Specialized UI Engines", c_ui2, ACCENT_PURPLE, "Interactive Academic Tools")

    c_ui3 = [
        ("Optimistic UI Updates", "Immediate visual feedback on status changes with background rollback on failure."),
        ("Accessible Data Tables", "Client/server pagination (5/10/20/50 rows), multi-column sorting, and filters."),
        ("Toast Feedback System", "Non-intrusive green/red/amber toast alerts for all mutating actions."),
        ("Zero Client Memory Leaks", "Strict cleanup in useEffect hooks and memoized calculations with useMemo.")
    ]
    add_card(s25, 8.8, 1.9, 3.7, 4.9, "Performance & Micro-Interactions", c_ui3, ACCENT_GREEN, "Snappy Institutional Operations")

    # =========================================================================
    # SLIDE 26: Enterprise Data Migration & Bulk Ingestion Engine
    # =========================================================================
    s26 = prs.slides.add_slide(blank_layout)
    set_slide_background(s26)
    add_header(s26, "DATA MIGRATION SUITE", "Enterprise Data Migration & Bulk Ingestion Engine", 
               "Strict 10-level topological dependency graph (DAG) and 4-way field dictionary ensuring zero foreign key errors", 26)

    c_mig1 = [
        ("Level 1-2: Foundation", "Academic Years, Campuses, Departments, Faculties."),
        ("Level 3-4: Curricular Structure", "Degree Programs, Semesters, Course Master, Fee Heads."),
        ("Level 5-6: Personnel & Cohorts", "Staff Master, Batches, Sections, Fee Structures."),
        ("Level 7-8: Students & Invoicing", "Student Profiles, Parent Links, Term Invoices."),
        ("Level 9-10: Academic Execution", "Course Enrollments, Timetable Slots, Historical Marks.")
    ]
    add_card(s26, 0.8, 1.9, 3.7, 4.9, "10-Level Topological DAG", c_mig1, ACCENT_BLUE, "Zero Foreign Key Violations")

    c_mig2 = [
        ("Pre-Formatted CSV/XLSX Schemas", "Standardized downloadable templates with column data types and examples."),
        ("Staging Buffer Tables", "Incoming data loaded into staging tables for validation before production insertion."),
        ("Dry-Run Validation Engine", "Identifies duplicate emails, invalid phone formats, and missing prerequisites."),
        ("Detailed Error Reports", "Generates downloadable error spreadsheets highlighting exact row and column faults.")
    ]
    add_card(s26, 4.8, 1.9, 3.7, 4.9, "Bulk Ingestion & Validation", c_mig2, ACCENT_GREEN, "Automated Quality Gates")

    c_mig3 = [
        ("Legacy CSV Column", "Maps legacy database column headers (e.g. STUD_DOB, ENR_NUM)."),
        ("Admin UI Input Field", "Maps corresponding field on React administrative portal forms."),
        ("Backend API DTO", "Maps TypeScript validation DTO property with type decorators."),
        ("Prisma Database Column", "Maps target PostgreSQL column name and relational foreign key.")
    ]
    add_card(s26, 8.8, 1.9, 3.7, 4.9, "4-Way Field Mapping Dictionary", c_mig3, ACCENT_AMBER, "Universal Field Rosetta Stone")

    # =========================================================================
    # SLIDE 27: 30-Day Institutional Cutover & Go-Live Playbook
    # =========================================================================
    s27 = prs.slides.add_slide(blank_layout)
    set_slide_background(s27)
    add_header(s27, "GO-LIVE RUNBOOK", "30-Day Institutional Cutover & Go-Live Playbook", 
               "Proven enterprise implementation methodology ensuring smooth cutover, operational readiness, and zero downtime", 27)

    c_go1 = [
        ("T-30 to T-20: Data Audit", "Extracting legacy datasets, resolving orphan records, standardizing student records."),
        ("T-19 to T-15: Pilot Dry Run", "Executing full 10-level DAG ingestion into Staging environment for verification."),
        ("T-14 to T-10: End-to-End Testing", "Stakeholder user acceptance testing (UAT) across Admissions, Fees, and Exams."),
        ("T-9 to T-5: Role-Based Training", "Hands-on workshop training for Deans, HODs, Cashiers, Wardens, and Faculty.")
    ]
    add_card(s27, 0.8, 1.9, 3.7, 4.9, "T-30 to T-5: Preparation & UAT", c_go1, ACCENT_BLUE, "Data Cleansing & Role Training")

    c_go2 = [
        ("Friday 18:00 (Freeze)", "Legacy ERP placed in read-only mode; final database snapshot taken."),
        ("Saturday 06:00 (Delta Load)", "Automated delta ETL script ingests recent transactions into UniversityERP."),
        ("Saturday 18:00 (Audit Recon)", "Finance Head and Registrar sign off on ledger balance and student enrollments."),
        ("Sunday 12:00 (DNS Switch)", "Domain routing switched to production cluster; health checks validated.")
    ]
    add_card(s27, 4.8, 1.9, 3.7, 4.9, "Cutover Weekend Timeline", c_go2, ACCENT_AMBER, "Hour-by-Hour Execution Plan")

    c_go3 = [
        ("Day 1: On-Site War Room", "Dedicated architecture and support engineers on campus assisting staff."),
        ("Dual-Running Reconciliation", "Daily cross-checks between bank deposits and cashiering collections."),
        ("T+7: Final Acceptance", "Steering committee formal sign-off; legacy ERP servers decommissioned."),
        ("Emergency Rollback Plan", "Pre-tested fallback runbook in case of critical unrecoverable failure.")
    ]
    add_card(s27, 8.8, 1.9, 3.7, 4.9, "T+1 to T+7: Stabilization & Sign-Off", c_go3, ACCENT_GREEN, "War Room & Steady State")

    # =========================================================================
    # SLIDE 28: Accreditation Intelligence & Statutory Compliance
    # =========================================================================
    s28 = prs.slides.add_slide(blank_layout)
    set_slide_background(s28)
    add_header(s28, "STATUTORY COMPLIANCE", "Accreditation Intelligence & Statutory Compliance (NAAC, NBA, NEP)", 
               "Built-in compliance automation providing quantitative evidence for NAAC SSR, NBA OBE, and NIRF rankings", 28)

    c_acc1 = [
        ("Multiple Entry / Exit Points", "Certificates (Year 1), Diplomas (Year 2), Degrees (Year 3), Honors (Year 4)."),
        ("Academic Bank of Credits (ABC)", "Automated credit logging and seamless credit transfer across institutions."),
        ("Multi-Disciplinary Curricula", "Support for major/minor tracks, vocational training, and internship credits."),
        ("Indian Knowledge Systems (IKS)", "Categorization of indigenous knowledge courses and community engagement.")
    ]
    add_card(s28, 0.8, 1.9, 3.7, 4.9, "National Education Policy (NEP 2020)", c_acc1, ACCENT_BLUE, "Curricular Flexibility & Credits")

    c_acc2 = [
        ("Criteria 1-7 Evidence Engine", "Automated aggregation of student data, teaching loads, and infrastructure."),
        ("Criterion 2: Teaching-Learning", "Real-time calculation of student-to-faculty ratios, mentor ratios, and pass rates."),
        ("Criterion 5: Student Support", "Automated tracking of scholarships, competitive exam coaching, and placements."),
        ("One-Click SSR Metric Export", "Generates quantitative Excel spreadsheets strictly conforming to NAAC portal.")
    ]
    add_card(s28, 4.8, 1.9, 3.7, 4.9, "NAAC SSR Accreditation Suite", c_acc2, ACCENT_GREEN, "Criteria 1-7 Automated Metrics")

    c_acc3 = [
        ("Outcome-Based Education (OBE)", "Mapping Course Outcomes (COs) to Program Outcomes (POs) and PSOs."),
        ("Direct Attainment Engine", "Calculates attainment thresholds from internal tests, quizzes, and end-sem exams."),
        ("Indirect Attainment Surveys", "Course-end surveys and graduate exit surveys feeding into indirect attainment."),
        ("Continuous Quality Improvement", "Automated gap analysis reports for department curriculum review boards.")
    ]
    add_card(s28, 8.8, 1.9, 3.7, 4.9, "NBA Accreditation & OBE Attainment", c_acc3, ACCENT_AMBER, "CO-PO Attainment Calculation")

    # =========================================================================
    # SLIDE 29: Institutional Analytics & Executive Cockpit (Module 14)
    # =========================================================================
    s29 = prs.slides.add_slide(blank_layout)
    set_slide_background(s29)
    add_header(s29, "EXECUTIVE INTELLIGENCE", "Institutional Analytics & Executive Cockpit (Module 14)", 
               "Real-time decision intelligence for Chancellors, Vice-Chancellors, Trustees, and Academic Deans", 29)

    c_an1 = [
        ("Chancellor / VC Cockpit", "High-level visual summary of total enrollment, revenue collection, and pass rates."),
        ("Admissions Conversion Funnel", "Real-time tracking of leads -> applications -> scrutinies -> paid enrollments."),
        ("Fee Collection Velocity", "Daily collection rates compared against target schedules and past fiscal years."),
        ("Seat Utilization Heatmap", "Branch-wise seat filling percentage highlighting under-subscribed courses.")
    ]
    add_card(s29, 0.8, 1.9, 3.7, 4.9, "Executive KPI Cockpit", c_an1, ACCENT_BLUE, "Top-Level Institutional Health")

    c_an2 = [
        ("Multi-Campus Benchmarking", "Compare academic performance, attendance, and revenue across campus sites."),
        ("Departmental Scorecards", "Faculty research output, student satisfaction ratings, and budget utilization."),
        ("Course Pass Rate Outliers", "Automated anomaly detection flagging abnormally high failure or scoring rates."),
        ("Placement Analytics", "Tracking placement offers, average salary packages, and top corporate recruiters.")
    ]
    add_card(s29, 4.8, 1.9, 3.7, 4.9, "Comparative Academic Analytics", c_an2, ACCENT_GREEN, "Campus & Department Performance")

    c_an3 = [
        ("Student Dropout Early Warning", "Machine learning heuristic identifying students with low attendance and marks."),
        ("Revenue Forecasting", "Predictive cash-flow modeling based on upcoming semester installments and arrears."),
        ("Hostel & Transport Utilization", "Optimizing vehicle routes and hostel rooms based on occupancy trends."),
        ("Automated Board Reports", "Scheduled PDF digest generation emailed weekly to University Board of Trustees.")
    ]
    add_card(s29, 8.8, 1.9, 3.7, 4.9, "Predictive Alerts & Forecasting", c_an3, ACCENT_AMBER, "Proactive Institutional Strategy")

    # =========================================================================
    # SLIDE 30: Disaster Recovery, High Availability & Enterprise SLA
    # =========================================================================
    s30 = prs.slides.add_slide(blank_layout)
    set_slide_background(s30)
    add_header(s30, "INFRASTRUCTURE & RESILIENCE", "Disaster Recovery, High Availability & Enterprise SLA", 
               "Zero single-point-of-failure infrastructure with multi-AZ replication, point-in-time recovery, and 99.95% SLA", 30)

    c_dr1 = [
        ("Stateless NestJS Containers", "API service runs in Docker containers behind an auto-scaling load balancer."),
        ("Multi-AZ PostgreSQL Replication", "Primary-standby database topology spanning multiple availability zones."),
        ("Redis Sentinel Caching", "In-memory cache with automatic master failover ensuring continuous availability."),
        ("Object Storage Redundancy", "S3 multi-region replication ensuring 99.999999999% durability of student files.")
    ]
    add_card(s30, 0.8, 1.9, 3.7, 4.9, "High-Availability Architecture", c_dr1, ACCENT_BLUE, "Zero Single-Point-of-Failure")

    c_dr2 = [
        ("Continuous WAL Archiving", "Write-Ahead Log (WAL) archiving enabling Point-In-Time Recovery (PITR)."),
        ("Recovery Point Objective (RPO)", "RPO < 5 Minutes: Maximum allowable data loss in catastrophic disaster."),
        ("Recovery Time Objective (RTO)", "RTO < 15 Minutes: Automated failover recovers full service within 15 minutes."),
        ("Automated Daily Off-Site Backups", "Encrypted daily database dumps transferred to isolated cold cloud storage.")
    ]
    add_card(s30, 4.8, 1.9, 3.7, 4.9, "Disaster Recovery & PITR", c_dr2, ACCENT_ROSE, "RPO < 5 Min | RTO < 15 Min")

    c_dr3 = [
        ("99.95% Uptime Guarantee", "Financially backed enterprise availability SLA excluding scheduled maintenance."),
        ("DDoS & WAF Protection", "Cloudflare enterprise web application firewall filtering malicious traffic."),
        ("Real-Time APM Telemetry", "Prometheus and Grafana dashboards monitoring CPU, memory, and query latencies."),
        ("24/7 Incident Escalation", "Automated PagerDuty alerts dispatched to on-call infrastructure engineers.")
    ]
    add_card(s30, 8.8, 1.9, 3.7, 4.9, "Enterprise SLA & Monitoring", c_dr3, ACCENT_GREEN, "99.95% SLA & 24/7 Telemetry")

    # =========================================================================
    # SLIDE 31: Total Cost of Ownership (TCO) & Strategic ROI Analysis
    # =========================================================================
    s31 = prs.slides.add_slide(blank_layout)
    set_slide_background(s31)
    add_header(s31, "FINANCIAL VALUE", "Total Cost of Ownership (TCO) & Strategic ROI Analysis", 
               "Delivering 60% lower TCO and 100% elimination of revenue leakage compared to legacy Tier-1 ERP suites", 31)

    tco_headers = ["Evaluation Category", "Legacy ERP Suites (SAP / Banner)", "UniversityERP Modern Platform", "Institutional Benefit"]
    tco_rows = [
        ["Upfront Licensing", "Extremely expensive per-core / per-user license", "Predictable institutional SaaS / self-hosted model", "65% lower initial capital expenditure"],
        ["Implementation Timeline", "12 to 24 Months complex consulting project", "30-Day automated cutover with proven DAG tools", "4x faster time-to-value and deployment"],
        ["Customization & Flexibility", "Proprietary code (ABAP/PL-SQL), expensive consultants", "Modern TypeScript, NestJS, React, Prisma stack", "In-house team easily manages customizations"],
        ["Revenue Leakage Elimination", "Frequent leakage due to disconnected billing & cashiering", "Dual-verify Razorpay gateway + double-entry ledger", "100% fee recovery and zero cash leakage"],
        ["Paper & Manual Operations", "Extensive physical paperwork, paper forms, registers", "100% paperless digital workflows with DLT SMS alerts", "90% reduction in paper and printing costs"],
        ["Accreditation Preparation", "3 to 6 months of manual spreadsheet compilation", "Real-time SSR Criteria 1-7 and OBE attainment export", "Accreditation readiness at all times with zero stress"]
    ]
    add_table_slide(s31, 0.8, 1.9, 11.733, 4.9, tco_headers, tco_rows, [2.3, 3.2, 3.2, 3.033])

    # =========================================================================
    # SLIDE 32: Strategic Vision, Roadmap & Next Steps
    # =========================================================================
    s32 = prs.slides.add_slide(blank_layout)
    set_slide_background(s32)
    add_header(s32, "STRATEGIC HORIZON", "Strategic Vision, Enterprise Roadmap & Next Steps", 
               "Empowering universities with autonomous digital operations, AI-assisted learning, and global compliance", 32)

    c_rd1 = [
        ("Phase 1: Core Deployment (Month 1)", "Data migration, Auth, Master Structure, Admissions, Fees, and Academics."),
        ("Phase 2: Academic & Exams (Month 2)", "Timetables, Biometric Attendance, Exam Scheduling, COE Anonymous Codes."),
        ("Phase 3: Facilities & Logistics (Month 3)", "Hostel matrix, Fleet GPS transit, RFID Library, and Health Clinic."),
        ("Phase 4: Analytics & Full Rollout (Month 4)", "Executive Cockpit, NAAC SSR exporter, and Alumni Network go-live.")
    ]
    add_card(s32, 0.8, 1.9, 3.7, 4.9, "1. Phased Deployment Roadmap", c_rd1, ACCENT_BLUE, "Structured 4-Month Rollout")

    c_rd2 = [
        ("AI Academic Advisor", "Generative AI assistant recommending personalized course electives to students."),
        ("Automated Timetable AI", "Genetic algorithm optimization for campus-wide complex multi-track scheduling."),
        ("Smart Proctoring ML", "Edge-based computer vision detecting candidate gaze and suspicious movements."),
        ("Conversational Helpdesk", "24/7 student service chatbot handling fee, grade, and gate-pass inquiries.")
    ]
    add_card(s32, 4.8, 1.9, 3.7, 4.9, "2. Next-Generation AI Horizons", c_rd2, ACCENT_PURPLE, "Artificial Intelligence in Higher Ed")

    c_rd3 = [
        ("Executive Demonstration", "Tailored sandbox walkthrough for Chancellor, Vice-Chancellor, and Trustees."),
        ("Technical Architecture Sign-Off", "Enterprise IT review of database schema, API security, and network topology."),
        ("Data Migration Workshop", "Hands-on data mapping session utilizing the 10-level DAG templates."),
        ("Formal Engagement Kick-Off", "Finalizing project charter, SLA agreements, and dedicated engineering team.")
    ]
    add_card(s32, 8.8, 1.9, 3.7, 4.9, "3. Recommended Immediate Action", c_rd3, ACCENT_GREEN, "Path to Partnership & Go-Live")

    output_path = "/home/admin/UniversityERP/flow/UniversityERP_Enterprise_Master_Architecture.pptx"
    prs.save(output_path)
    file_size = os.path.getsize(output_path)
    print(f"SUCCESS! Master PowerPoint presentation generated successfully: {output_path}")
    print(f"Total Slides: {len(prs.slides)} | File Size: {file_size / 1024:.1f} KB")

if __name__ == "__main__":
    build_presentation()
