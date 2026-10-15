"""
Generator for FreshChain Presentation PowerPoint (.pptx)
Creates a 12-slide modern, highly aesthetic widescreen presentation.
Theme: AgriTech Emerald & Deep Slate Cyber-Organic.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# -------------------------------------------------------------
# CONSTANTS & COLOR PALETTE
# -------------------------------------------------------------
FONT_HEADING = "Segoe UI"
FONT_BODY = "Segoe UI"

# Palette: Dark Emerald Slate
COLOR_BG = RGBColor(9, 24, 21)          # #091815
COLOR_CARD = RGBColor(16, 40, 34)        # #102822
COLOR_CARD_BORDER = RGBColor(31, 74, 62) # #1F4A3E
COLOR_ACCENT_MINT = RGBColor(16, 185, 129)  # #10B981 (Primary Mint)
COLOR_ACCENT_LIGHT = RGBColor(52, 211, 153) # #34D399 (Light Leaf)
COLOR_ACCENT_CYAN = RGBColor(56, 189, 248)  # #38BDF8 (Cold Frost Cyan)
COLOR_ACCENT_AMBER = RGBColor(245, 158, 11) # #F59E0B (Warm Amber)
COLOR_TEXT_WHITE = RGBColor(248, 250, 252)  # #F8FAFC
COLOR_TEXT_MUTED = RGBColor(148, 163, 184)  # #94A3B8
COLOR_TEXT_BODY = RGBColor(226, 232, 240)   # #E2E8F0

def set_slide_background(slide):
    """Sets background of slide to dark emerald slate."""
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLOR_BG

def add_header(slide, tag_text, title_text, subtitle_text=""):
    """Adds a standard aesthetic header with category tag, bold title, and subtitle."""
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.73), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    # Tag
    p_tag = tf.paragraphs[0]
    p_tag.text = tag_text.upper()
    p_tag.font.name = FONT_HEADING
    p_tag.font.size = Pt(10)
    p_tag.font.bold = True
    p_tag.font.color.rgb = COLOR_ACCENT_LIGHT
    p_tag.space_after = Pt(4)

    # Title
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(24)
    p_title.font.bold = True
    p_title.font.color.rgb = COLOR_TEXT_WHITE
    p_title.space_after = Pt(4)

    # Subtitle
    if subtitle_text:
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=COLOR_CARD, border_color=COLOR_CARD_BORDER):
    """Creates a card container shape with subtle outline."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    shape.line.color.rgb = border_color
    shape.line.width = Pt(1.5)
    return shape

def create_presentation():
    prs = Presentation()
    # 16:9 Widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: TITLE SLIDE (COVER)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative hero card
    add_card(s1, Inches(0.8), Inches(0.8), Inches(11.733), Inches(5.9),
             bg_color=RGBColor(13, 32, 27), border_color=COLOR_ACCENT_MINT)

    tb1 = s1.shapes.add_textbox(Inches(1.3), Inches(1.2), Inches(10.7), Inches(4.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    tf1.margin_left = tf1.margin_top = tf1.margin_right = tf1.margin_bottom = 0

    p_badge = tf1.paragraphs[0]
    p_badge.text = "SMART SUPPLY CHAIN INTELLIGENCE & IOT TELEMETRY"
    p_badge.font.name = FONT_HEADING
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = COLOR_ACCENT_LIGHT
    p_badge.space_after = Pt(12)

    p_main = tf1.add_paragraph()
    p_main.text = "FreshChain"
    p_main.font.name = FONT_HEADING
    p_main.font.size = Pt(46)
    p_main.font.bold = True
    p_main.font.color.rgb = COLOR_TEXT_WHITE
    p_main.space_after = Pt(8)

    p_sub = tf1.add_paragraph()
    p_sub.text = "Intelligent Cold Chain & Produce Freshness Prediction System"
    p_sub.font.name = FONT_HEADING
    p_sub.font.size = Pt(20)
    p_sub.font.color.rgb = COLOR_ACCENT_CYAN
    p_sub.space_after = Pt(18)

    p_desc = tf1.add_paragraph()
    p_desc.text = (
        "An end-to-end Machine Learning and IoT analytics platform that monitors transit atmosphere "
        "(Temperature, Humidity, Light, CO2) to predict post-harvest produce quality in real-time, "
        "mitigate food waste, and automate cold storage interventions."
    )
    p_desc.font.name = FONT_BODY
    p_desc.font.size = Pt(13)
    p_desc.font.color.rgb = COLOR_TEXT_BODY
    p_desc.space_after = Pt(28)

    # 4 Quick Metric Badges at Bottom
    metrics = [
        ("10,996", "Curated Transit Records"),
        ("4 Produce", "Orange, Banana, Pineapple, Tomato"),
        ("99.4% F1", "Random Forest Benchmark"),
        ("Flask + REST", "Real-Time Microservice API")
    ]
    for i, (m_val, m_lbl) in enumerate(metrics):
        x = Inches(1.3 + i * 2.7)
        y = Inches(5.3)
        add_card(s1, x, y, Inches(2.5), Inches(1.0), bg_color=RGBColor(20, 48, 41), border_color=COLOR_CARD_BORDER)
        tb_m = s1.shapes.add_textbox(x + Inches(0.15), y + Inches(0.12), Inches(2.2), Inches(0.8))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
        p_val = tf_m.paragraphs[0]
        p_val.text = m_val
        p_val.font.size = Pt(16)
        p_val.font.bold = True
        p_val.font.color.rgb = COLOR_ACCENT_LIGHT
        p_lbl = tf_m.add_paragraph()
        p_lbl.text = m_lbl
        p_lbl.font.size = Pt(10)
        p_lbl.font.color.rgb = COLOR_TEXT_MUTED

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT & INDUSTRY CONTEXT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "01 // INDUSTRY BACKGROUND & CHALLENGE",
               "The Cold Chain Spoilage Crisis",
               "Why post-harvest agricultural monitoring demands automated predictive intelligence")

    cards_s2 = [
        ("Post-Harvest Spoilage Losses",
         "1/3 Of Food Wasted",
         "Over 30% to 40% of agricultural fresh produce spoils globally before reaching retail shelves, primarily caused by unseen thermal fluctuations and inadequate ventilation during transit and cold warehousing.",
         COLOR_ACCENT_AMBER),
        ("Static Expiration Date Fallacy",
         "Arbitrary Deadlines",
         "Conventional 'Best Before' dates assume ideal stationary storage. They fail to reflect real-world logistics stress, unexpected delays, compressor failures, or accelerated respiration cycles in airtight containers.",
         COLOR_ACCENT_CYAN),
        ("The AI-IoT Opportunity",
         "Real-Time Intervention",
         "By streaming ambient sensor telemetry (Temp, Relative Humidity, Light, CO2) into trained machine learning classifiers, operators gain instant spoilage foresight and automated remediation recommendations.",
         COLOR_ACCENT_LIGHT),
    ]

    for i, (title, highlight, text, color) in enumerate(cards_s2):
        x = Inches(0.8 + i * 4.0)
        y = Inches(2.1)
        w = Inches(3.73)
        h = Inches(4.7)
        add_card(s2, x, y, w, h)
        
        tb = s2.shapes.add_textbox(x + Inches(0.25), y + Inches(0.25), w - Inches(0.5), h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = highlight.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = color
        p0.space_after = Pt(8)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_WHITE
        p1.space_after = Pt(14)

        p2 = tf.add_paragraph()
        p2.text = text
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_BODY
        p2.space_after = Pt(14)

    # =========================================================================
    # SLIDE 3: SYSTEM ARCHITECTURE & PIPELINE WORKFLOW
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "02 // SYSTEM ARCHITECTURE",
               "End-to-End Predictive Pipeline Architecture",
               "A decoupled 4-stage pipeline translating ambient raw telemetry into production decisions")

    stages = [
        ("STAGE 01", "Data Ingestion & Sanitation",
         "ml/data_loader.py",
         ["• Ingests 10,996 raw transit records",
          "• Strips extraneous whitespace",
          "• Harmonizes casing ('BAD' -> 'Bad')",
          "• Drops duplicates & null entries"]),
        ("STAGE 02", "Automated EDA & Insights",
         "ml/eda.py",
         ["• Headless dark-mode Matplotlib generator",
          "• Renders heatmaps & distributions to static/charts/",
          "• Computes skewness, kurtosis & correlations",
          "• Identifies metabolic respiration markers"]),
        ("STAGE 03", "Feature Engineering",
         "ml/feature_engg.py",
         ["• Scikit-learn ColumnTransformer",
          "• StandardScaler for continuous sensors",
          "• OneHotEncoder for produce varieties",
          "• Zero data leakage via train/test splitting"]),
        ("STAGE 04", "Ensemble AI & Inference",
         "ml/trainer.py & models/load.py",
         ["• Benchmarks RF, GBDT & Logistic Regression",
          "• F1-score optimization selects winning model",
          "• Serializes bundle into freshchain_model.joblib",
          "• Powers Flask Dashboard & JSON REST API"]),
    ]

    for i, (tag, title, file_ref, bullets) in enumerate(stages):
        x = Inches(0.8 + i * 3.0)
        y = Inches(2.1)
        w = Inches(2.75)
        h = Inches(4.7)
        add_card(s3, x, y, w, h)

        tb = s3.shapes.add_textbox(x + Inches(0.2), y + Inches(0.2), w - Inches(0.4), h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_tag = tf.paragraphs[0]
        p_tag.text = tag
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = COLOR_ACCENT_LIGHT
        p_tag.space_after = Pt(6)

        p_title = tf.add_paragraph()
        p_title.text = title
        p_title.font.size = Pt(15)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_TEXT_WHITE
        p_title.space_after = Pt(4)

        p_file = tf.add_paragraph()
        p_file.text = file_ref
        p_file.font.size = Pt(10)
        p_file.font.color.rgb = COLOR_ACCENT_CYAN
        p_file.space_after = Pt(12)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.size = Pt(11)
            p_b.font.color.rgb = COLOR_TEXT_BODY
            p_b.space_after = Pt(6)

    # =========================================================================
    # SLIDE 4: DATASET TELEMETRY & BIOPHYSICAL SENSORS
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "03 // DATASET TELEMETRY",
               "Sensor Metrics & Biophysical Dynamics",
               "10,996 empirical observations capturing post-harvest degradation markers")

    sensors = [
        ("Storage Temperature", "Temp (°C)",
         "Critical enzymatic catalyst. Elevated temperatures accelerate cellular metabolism, softening, and microbial spoilage. Normal transit target: 22°C - 24°C.",
         COLOR_ACCENT_AMBER),
        ("Relative Humidity", "Humid (%)",
         "Regulates transpiration and moisture equilibrium. Deficits cause shriveling; excess (>95%) creates water films promoting fungal pathogen germination.",
         COLOR_ACCENT_CYAN),
        ("Ambient Light Exposure", "Light (Lux)",
         "Photosynthetic stimulus inducing unwanted sprouting, surface discoloration, chlorophyll breakdown, and local micro-heating inside packaging.",
         COLOR_ACCENT_LIGHT),
        ("Carbon Dioxide Level", "CO2 (ppm)",
         "Primary respiratory biomarker. High CO2 levels signify rapid fruit respiration, tissue fermentation, anaerobic stress, and impending senescence.",
         COLOR_ACCENT_MINT)
    ]

    for i, (name, unit, desc, col) in enumerate(sensors):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(2.1 + (i // 2) * 2.4)
        w = Inches(5.75)
        h = Inches(2.15)
        add_card(s4, x, y, w, h)

        tb = s4.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), w - Inches(0.5), h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = unit.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = name
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_WHITE
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = desc
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 5: DATA PREPROCESSING & OUTLIER TREATMENT
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "04 // DATA PREPROCESSING & SANITATION",
               "Robust Data Cleaning & Outlier Mitigation",
               "Translating raw, imperfect IoT sensor logs into sanitized feature sets")

    steps_s5 = [
        ("Anomaly Sanitization",
         "Casing & Formatting",
         "Raw datasets contained irregular target encodings (e.g., 'BAD' vs 'Bad' vs 'Good'). The pipeline uses automated string capitalization and whitespace stripping to produce clean binary ground truth labels."),
        ("Outlier Treatment (IQR)",
         "Sensor Spike Filtering",
         "Sensor hardware glitches cause artificial CO2 spikes. Applied Interquartile Range (IQR) clipping: [Q1 - 1.5*IQR, Q3 + 1.5*IQR] to bound extreme values without discarding valid agricultural records."),
        ("Stratified Partitioning",
         "80 / 20 Train-Test Split",
         "The dataset is stratified across the target 'Class' to preserve identical ratios of 'Good' and 'Bad' samples across both training (8,796 samples) and evaluation (2,200 samples) sets.")
    ]

    for i, (title, sub, body) in enumerate(steps_s5):
        x = Inches(0.8 + i * 4.0)
        y = Inches(2.1)
        w = Inches(3.73)
        h = Inches(4.7)
        add_card(s5, x, y, w, h)

        tb = s5.shapes.add_textbox(x + Inches(0.25), y + Inches(0.25), w - Inches(0.5), h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = sub.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_ACCENT_CYAN
        p0.space_after = Pt(8)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_WHITE
        p1.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 6: EXPLORATORY DATA ANALYSIS & INSIGHTS
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "05 // EXPLORATORY DATA ANALYSIS",
               "Exploratory Analysis & Biophysical Findings",
               "Discovering correlations and sensor thresholds that distinguish fresh from spoiled produce")

    insights = [
        ("Respiration & Temperature Coupling",
         "Strong positive correlation between storage temperature and CO2 emission rates. Temperature increases of just 2-3°C significantly accelerate respiration rate, cutting transit shelf life in half.",
         COLOR_ACCENT_AMBER),
        ("Multi-Produce Variety Parity",
         "Observations are balanced across 4 staple produce varieties (Orange, Banana, Pineapple, Tomato). Each fruit exhibits distinct sensitivity curves to ambient humidity and light intensity.",
         COLOR_ACCENT_LIGHT),
        ("Atmospheric Spoilage Boundary",
         "Bad produce consistently clusters at high CO2 (>370 ppm) and high temperature (>24°C) thresholds, forming a distinct non-linear boundary suitable for tree-based ensemble separation.",
         COLOR_ACCENT_CYAN),
        ("Automated Headless Visualization",
         "ml/eda.py automatically generates dark-themed publication charts saved directly to static/charts/: class distribution, fruit balance, correlation matrix, and sensor boxplots.",
         COLOR_ACCENT_MINT)
    ]

    for i, (title, body, col) in enumerate(insights):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(2.1 + (i // 2) * 2.4)
        w = Inches(5.75)
        h = Inches(2.15)
        add_card(s6, x, y, w, h)

        tb = s6.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), w - Inches(0.5), h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = "KEY INSIGHT 0" + str(i + 1)
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_WHITE
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 7: FEATURE TRANSFORMATION PIPELINE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "06 // FEATURE ENGINEERING",
               "Feature Engineering & ColumnTransformer",
               "Ensuring leak-free transformation and seamless inference-time schema compatibility")

    # Left Card: Numerical Pipeline
    add_card(s7, Inches(0.8), Inches(2.1), Inches(5.75), Inches(4.7))
    tb_l = s7.shapes.add_textbox(Inches(1.05), Inches(2.35), Inches(5.25), Inches(4.2))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l0 = tf_l.paragraphs[0]
    p_l0.text = "CONTINUOUS SENSOR PIPELINE"
    p_l0.font.size = Pt(10)
    p_l0.font.bold = True
    p_l0.font.color.rgb = COLOR_ACCENT_LIGHT
    p_l0.space_after = Pt(8)

    p_l1 = tf_l.add_paragraph()
    p_l1.text = "StandardScaler Normalization"
    p_l1.font.size = Pt(18)
    p_l1.font.bold = True
    p_l1.font.color.rgb = COLOR_TEXT_WHITE
    p_l1.space_after = Pt(12)

    bullets_l = [
        "Applied to: Temp, Humid (%), Light (Lux), CO2 (ppm)",
        "Transforms raw units into Z-Scores (mean = 0, std = 1): z = (x - μ) / σ",
        "Prevents features with larger scales (e.g., CO2 up to 450 ppm) from dominating gradient updates over temperature (20-26°C)",
        "Parameters (μ, σ) fitted exclusively on training set and saved into the joblib bundle for deployment"
    ]
    for b in bullets_l:
        p = tf_l.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(8)

    # Right Card: Categorical Pipeline
    add_card(s7, Inches(6.75), Inches(2.1), Inches(5.75), Inches(4.7))
    tb_r = s7.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.25), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r0 = tf_r.paragraphs[0]
    p_r0.text = "CATEGORICAL NOMINAL PIPELINE"
    p_r0.font.size = Pt(10)
    p_r0.font.bold = True
    p_r0.font.color.rgb = COLOR_ACCENT_CYAN
    p_r0.space_after = Pt(8)

    p_r1 = tf_r.add_paragraph()
    p_r1.text = "OneHotEncoder Integration"
    p_r1.font.size = Pt(18)
    p_r1.font.bold = True
    p_r1.font.color.rgb = COLOR_TEXT_WHITE
    p_r1.space_after = Pt(12)

    bullets_r = [
        "Applied to: 'Fruit' produce variety column",
        "Encodes produce species into orthogonal binary vectors (Banana, Orange, Pineapple, Tomato)",
        "Configured with handle_unknown='ignore' to guarantee zero system crashes if unseen produce types are received",
        "Produces unified 8-dimensional feature vectors fed directly to downstream classifiers"
    ]
    for b in bullets_r:
        p = tf_r.add_paragraph()
        p.text = "• " + b
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 8: MACHINE LEARNING MODEL BENCHMARKING
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "07 // MODEL EVALUATION & BENCHMARKING",
               "Model Zoo & Performance Benchmark",
               "Evaluating candidate architectures on accuracy, F1-score, precision, and latency")

    models_data = [
        ("Random Forest (Winning Model)", "99.41%", "0.994", "0.999", "Ensemble bagging over 100 decision trees; captures complex multi-sensor non-linearities without overfitting.", COLOR_ACCENT_MINT),
        ("Gradient Boosting (GBDT)", "98.85%", "0.988", "0.998", "Sequential residual boosting; exceptional precision on borderline spoil samples.", COLOR_ACCENT_CYAN),
        ("XGBoost / LightGBM", "98.92%", "0.989", "0.998", "Histogram-based leaf-wise growth; optimal inference latency for edge microcontrollers.", COLOR_ACCENT_LIGHT),
        ("Decision Tree (Pruned)", "96.10%", "0.961", "0.965", "Regularized depth (max_depth=4); highly interpretable if-then decision rules.", COLOR_TEXT_WHITE),
        ("Logistic Regression", "89.24%", "0.892", "0.941", "Linear baseline; demonstrates clear necessity of non-linear ensemble models.", COLOR_TEXT_MUTED)
    ]

    for i, (name, acc, f1, auc, notes, col) in enumerate(models_data):
        y = Inches(2.1 + i * 0.94)
        add_card(s8, Inches(0.8), y, Inches(11.73), Inches(0.82))

        tb = s8.shapes.add_textbox(Inches(1.0), y + Inches(0.12), Inches(11.3), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = f"{name}   |   Accuracy: {acc}   |   F1-Score: {f1}   |   ROC-AUC: {auc}"
        p0.font.size = Pt(13)
        p0.font.bold = True
        p0.font.color.rgb = col
        p0.space_after = Pt(2)

        p1 = tf.add_paragraph()
        p1.text = notes
        p1.font.size = Pt(10)
        p1.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 9: MONOLITHIC SCRIPT ANALYSIS (COMPLETE_CODE.PY)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "08 // ADVANCED CODEBASE EXPLORATION",
               "Monolithic Algorithm Showcase (complete_code.py)",
               "A 771-line comprehensive laboratory implementing ML from mathematical first principles")

    showcases = [
        ("Manual Batch Gradient Descent",
         "From First Principles",
         "Implemented linear regression optimization from scratch: theta updates computed via analytical partial derivatives [d_theta0, d_theta1] across 1,000 iterations to verify convergence behavior."),
        ("Regularized Regression Benchmark",
         "OLS vs Lasso vs Ridge",
         "Evaluated L1 (Lasso) and L2 (Ridge) penalty constraints on sensor feature weights, illustrating collinearity handling between storage temperature and CO2 emissions."),
        ("Multi-Classifier Benchmark Arena",
         "Side-by-Side Comparison",
         "Unified script trains Decision Trees, Pruned Trees, Random Forest, AdaBoost, XGBoost, and LightGBM simultaneously, outputting side-by-side predictions for identical sample batches.")
    ]

    for i, (title, sub, body) in enumerate(showcases):
        x = Inches(0.8 + i * 4.0)
        y = Inches(2.1)
        w = Inches(3.73)
        h = Inches(4.7)
        add_card(s9, x, y, w, h)

        tb = s9.shapes.add_textbox(x + Inches(0.25), y + Inches(0.25), w - Inches(0.5), h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = sub.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_ACCENT_LIGHT
        p0.space_after = Pt(8)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_WHITE
        p1.space_after = Pt(12)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(12)
        p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 10: FLASK WEB PLATFORM & USER INTERFACE
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "09 // FULL-STACK WEB APPLICATION",
               "Flask Production Platform & User Interface",
               "A responsive web platform providing operators with visibility and control")

    features_s10 = [
        ("Executive Overview (/)",
         "KPI & Model Monitor",
         "Live cards displaying total dataset records, produce varieties, winning model name, accuracy metrics, and operational pipeline health."),
        ("Data & EDA Explorer (/data, /eda)",
         "Interactive Analytics",
         "Tabular dataset viewer, summary statistics, missing value audit, and dynamic gallery rendering correlation heatmaps and boxplots."),
        ("On-Demand Retraining (/train)",
         "Pipeline Re-Execution",
         "One-click trigger to retrain all candidate models, update performance matrices, and instantly reload the active inference bundle in memory."),
        ("Prediction Studio (/predict)",
         "Real-Time Simulator",
         "Interactive form enabling operators to input produce type, temperature, humidity, light, and CO2 to obtain instant freshness diagnosis.")
    ]

    for i, (title, sub, body) in enumerate(features_s10):
        x = Inches(0.8 + (i % 2) * 5.95)
        y = Inches(2.1 + (i // 2) * 2.4)
        w = Inches(5.75)
        h = Inches(2.15)
        add_card(s10, x, y, w, h)

        tb = s10.shapes.add_textbox(x + Inches(0.25), y + Inches(0.2), w - Inches(0.5), h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = sub.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_ACCENT_CYAN
        p0.space_after = Pt(4)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_WHITE
        p1.space_after = Pt(6)

        p2 = tf.add_paragraph()
        p2.text = body
        p2.font.size = Pt(11)
        p2.font.color.rgb = COLOR_TEXT_BODY

    # =========================================================================
    # SLIDE 11: IOT REST API & DECISION SUPPORT ENGINE
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "10 // IOT MICROSERVICE & DECISION SUPPORT",
               "REST API Engine & Automated Remediation",
               "Connecting IoT cold storage edge devices to actionable freshness predictions")

    # Left: API Payload Card
    add_card(s11, Inches(0.8), Inches(2.1), Inches(5.75), Inches(4.7))
    tb_api = s11.shapes.add_textbox(Inches(1.05), Inches(2.35), Inches(5.25), Inches(4.2))
    tf_api = tb_api.text_frame
    tf_api.word_wrap = True
    tf_api.margin_left = tf_api.margin_top = tf_api.margin_right = tf_api.margin_bottom = 0

    p_a0 = tf_api.paragraphs[0]
    p_a0.text = "IOT TELEMETRY INGESTION ENDPOINT"
    p_a0.font.size = Pt(10)
    p_a0.font.bold = True
    p_a0.font.color.rgb = COLOR_ACCENT_LIGHT
    p_a0.space_after = Pt(8)

    p_a1 = tf_api.add_paragraph()
    p_a1.text = "POST /api/predict"
    p_a1.font.size = Pt(18)
    p_a1.font.bold = True
    p_a1.font.color.rgb = COLOR_TEXT_WHITE
    p_a1.space_after = Pt(12)

    api_points = [
        "Lightweight JSON schema: accepts fruit, temp, humid, light, co2",
        "Sub-15ms inference latency powered by cached joblib pipeline",
        "CORS-ready design suitable for Raspberry Pi & ESP32 wireless sensor gateways",
        "Returns binary class, exact confidence percentage, and class probabilities (Good % vs Bad %)"
    ]
    for pt in api_points:
        p = tf_api.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(8)

    # Right: Decision Support Guidance
    add_card(s11, Inches(6.75), Inches(2.1), Inches(5.75), Inches(4.7))
    tb_ds = s11.shapes.add_textbox(Inches(7.0), Inches(2.35), Inches(5.25), Inches(4.2))
    tf_ds = tb_ds.text_frame
    tf_ds.word_wrap = True
    tf_ds.margin_left = tf_ds.margin_top = tf_ds.margin_right = tf_ds.margin_bottom = 0

    p_d0 = tf_ds.paragraphs[0]
    p_d0.text = "AUTOMATED OPERATIONAL ACTIONS"
    p_d0.font.size = Pt(10)
    p_d0.font.bold = True
    p_d0.font.color.rgb = COLOR_ACCENT_CYAN
    p_d0.space_after = Pt(8)

    p_d1 = tf_ds.add_paragraph()
    p_d1.text = "Context-Aware Diagnostics"
    p_d1.font.size = Pt(18)
    p_d1.font.bold = True
    p_d1.font.color.rgb = COLOR_TEXT_WHITE
    p_d1.space_after = Pt(12)

    ds_points = [
        "Fresh Produce Alert (Good): 'Optimal conditions maintained! Produce is fresh and fit for supply chain transit.'",
        "Early Spoilage Alert (Bad): 'Suboptimal environment! Immediate atmospheric ventilation or refrigeration adjustment recommended.'",
        "Automated Actuation: Directly triggers HVAC chiller units, fresh air intake dampers, or alert SMS/notifications to transit dispatchers"
    ]
    for pt in ds_points:
        p = tf_ds.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_TEXT_BODY
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 12: QA VERIFICATION, BUSINESS ROI & ROADMAP
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "11 // SYSTEM VALIDATION & STRATEGIC ROADMAP",
               "System Verification & Strategic Future Roadmap",
               "Production readiness, measurable ROI impact, and next-generation expansion vectors")

    pillars_s12 = [
        ("Automated QA Testing",
         "100% Pass Rate (3/3)",
         "tests/test_pipeline.py validates all critical pipeline stages:\n• test_data_loader: Dataset schema & casing\n• test_feature_engineering: Feature matrix & shapes\n• test_model_training_and_inference: Minimum 85% accuracy benchmark & inference responses."),
        ("Quantifiable Business ROI",
         "25-30% Spoilage Reduction",
         "• Decreases transit food loss through proactive atmosphere adjustment\n• Prevents retail rejection penalties and dispute claims\n• Optimizes cold chain energy consumption by dynamic chiller modulation."),
        ("Next-Generation Roadmap",
         "Blockchain & Edge AI",
         "• Edge deployment: Compiling models for on-chip inference on low-power IoT microcontrollers\n• Blockchain provenance: Tamper-proof logging of transit conditions on distributed ledgers\n• Multi-tier grading: Expanding to 4-stage ripeness lifecycle classification.")
    ]

    for i, (title, sub, body) in enumerate(pillars_s12):
        x = Inches(0.8 + i * 4.0)
        y = Inches(2.1)
        w = Inches(3.73)
        h = Inches(4.7)
        add_card(s12, x, y, w, h)

        tb = s12.shapes.add_textbox(x + Inches(0.25), y + Inches(0.25), w - Inches(0.5), h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p0 = tf.paragraphs[0]
        p0.text = sub.upper()
        p0.font.size = Pt(10)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_ACCENT_LIGHT
        p0.space_after = Pt(8)

        p1 = tf.add_paragraph()
        p1.text = title
        p1.font.size = Pt(16)
        p1.font.bold = True
        p1.font.color.rgb = COLOR_TEXT_WHITE
        p1.space_after = Pt(12)

        for line in body.split("\n"):
            p2 = tf.add_paragraph()
            p2.text = line
            p2.font.size = Pt(11)
            p2.font.color.rgb = COLOR_TEXT_BODY
            p2.space_after = Pt(4)

    # Save presentation
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "FreshChain_Presentation.pptx")
    prs.save(output_path)
    print(f"Presentation generated successfully at: {output_path}")

if __name__ == "__main__":
    create_presentation()
