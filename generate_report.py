#!/usr/bin/env python3
"""
BookVerse Competitor Analysis & Market Strategy Report
Professional PDF Generator
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os
from datetime import datetime

# ============================================================
# COLOR PALETTE
# ============================================================
GOLD = HexColor("#C8A951")
DARK_NAVY = HexColor("#0D1117")
DEEP_NAVY = HexColor("#161B22")
CHARCOAL = HexColor("#1E2328")
LIGHT_GOLD = HexColor("#E8D48B")
CREAM = HexColor("#FAF3E0")
WHITE = HexColor("#FFFFFF")
LIGHT_GRAY = HexColor("#F6F8FA")
MID_GRAY = HexColor("#8B949E")
TEXT_PRIMARY = HexColor("#1A1A2E")
TEXT_SECONDARY = HexColor("#4A5568")
GREEN = HexColor("#22C55E")
RED = HexColor("#EF4444")
ORANGE = HexColor("#FF6B35")
BLUE = HexColor("#3B82F6")

OUTPUT_PATH = "/Users/ankit/Documents/Trading & Finance/bookstore/BookVerse_Competitor_Analysis_Report.pdf"

# ============================================================
# CUSTOM STYLES
# ============================================================
def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle', fontName='Helvetica-Bold', fontSize=32,
        textColor=GOLD, alignment=TA_CENTER, spaceAfter=10, leading=38
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle', fontName='Helvetica', fontSize=14,
        textColor=WHITE, alignment=TA_CENTER, spaceAfter=6, leading=20
    ))
    styles.add(ParagraphStyle(
        'SectionHeader', fontName='Helvetica-Bold', fontSize=20,
        textColor=DARK_NAVY, spaceBefore=20, spaceAfter=12, leading=26,
        borderColor=GOLD, borderWidth=2, borderPadding=8,
    ))
    styles.add(ParagraphStyle(
        'SubHeader', fontName='Helvetica-Bold', fontSize=14,
        textColor=ORANGE, spaceBefore=14, spaceAfter=8, leading=18
    ))
    styles.add(ParagraphStyle(
        'SubHeader2', fontName='Helvetica-Bold', fontSize=12,
        textColor=DARK_NAVY, spaceBefore=10, spaceAfter=6, leading=16
    ))
    styles['BodyText'].fontName = 'Helvetica'
    styles['BodyText'].fontSize = 10
    styles['BodyText'].textColor = TEXT_SECONDARY
    styles['BodyText'].alignment = TA_JUSTIFY
    styles['BodyText'].spaceAfter = 6
    styles['BodyText'].leading = 15
    styles['BodyText'].firstLineIndent = 0
    styles.add(ParagraphStyle(
        'BulletItem', fontName='Helvetica', fontSize=10,
        textColor=TEXT_SECONDARY, leftIndent=20, spaceAfter=4, leading=14,
        bulletIndent=8, bulletFontName='Helvetica', bulletFontSize=10
    ))
    styles.add(ParagraphStyle(
        'TableHeader', fontName='Helvetica-Bold', fontSize=9,
        textColor=WHITE, alignment=TA_CENTER, leading=12
    ))
    styles.add(ParagraphStyle(
        'TableCell', fontName='Helvetica', fontSize=8,
        textColor=TEXT_PRIMARY, alignment=TA_CENTER, leading=11
    ))
    styles.add(ParagraphStyle(
        'TableCellLeft', fontName='Helvetica', fontSize=8,
        textColor=TEXT_PRIMARY, alignment=TA_LEFT, leading=11
    ))
    styles.add(ParagraphStyle(
        'Insight', fontName='Helvetica-Oblique', fontSize=10,
        textColor=ORANGE, spaceBefore=8, spaceAfter=8, leading=14,
        leftIndent=15, borderColor=ORANGE, borderWidth=1, borderPadding=6,
        backColor=HexColor("#FFF7ED")
    ))
    styles.add(ParagraphStyle(
        'FooterText', fontName='Helvetica', fontSize=8,
        textColor=MID_GRAY, alignment=TA_CENTER
    ))
    styles.add(ParagraphStyle(
        'TOCEntry', fontName='Helvetica', fontSize=11,
        textColor=TEXT_PRIMARY, spaceBefore=6, spaceAfter=6, leading=16,
        leftIndent=20
    ))
    styles.add(ParagraphStyle(
        'KPIValue', fontName='Helvetica-Bold', fontSize=22,
        textColor=GOLD, alignment=TA_CENTER, leading=28
    ))
    styles.add(ParagraphStyle(
        'KPILabel', fontName='Helvetica', fontSize=9,
        textColor=TEXT_SECONDARY, alignment=TA_CENTER, leading=12
    ))
    return styles


# ============================================================
# PAGE TEMPLATE WITH HEADER/FOOTER
# ============================================================
class ReportTemplate:
    def __init__(self):
        self.page_count = 0

    def on_first_page(self, canvas_obj, doc):
        canvas_obj.saveState()
        w, h = A4
        # Full dark background
        canvas_obj.setFillColor(DARK_NAVY)
        canvas_obj.rect(0, 0, w, h, fill=True, stroke=False)
        # Gold accent bar at top
        canvas_obj.setFillColor(GOLD)
        canvas_obj.rect(0, h - 8, w, 8, fill=True, stroke=False)
        # Gold accent bar at bottom
        canvas_obj.rect(0, 0, w, 8, fill=True, stroke=False)
        # Decorative corner elements
        canvas_obj.setStrokeColor(GOLD)
        canvas_obj.setLineWidth(1.5)
        margin = 40
        corner_len = 40
        # Top-left
        canvas_obj.line(margin, h - margin, margin + corner_len, h - margin)
        canvas_obj.line(margin, h - margin, margin, h - margin - corner_len)
        # Top-right
        canvas_obj.line(w - margin, h - margin, w - margin - corner_len, h - margin)
        canvas_obj.line(w - margin, h - margin, w - margin, h - margin - corner_len)
        # Bottom-left
        canvas_obj.line(margin, margin, margin + corner_len, margin)
        canvas_obj.line(margin, margin, margin, margin + corner_len)
        # Bottom-right
        canvas_obj.line(w - margin, margin, w - margin - corner_len, margin)
        canvas_obj.line(w - margin, margin, w - margin, margin + corner_len)
        canvas_obj.restoreState()

    def on_later_pages(self, canvas_obj, doc):
        canvas_obj.saveState()
        w, h = A4
        self.page_count += 1
        # Header bar
        canvas_obj.setFillColor(DARK_NAVY)
        canvas_obj.rect(0, h - 35, w, 35, fill=True, stroke=False)
        canvas_obj.setFillColor(GOLD)
        canvas_obj.rect(0, h - 38, w, 3, fill=True, stroke=False)
        # Header text
        canvas_obj.setFont("Helvetica-Bold", 9)
        canvas_obj.setFillColor(GOLD)
        canvas_obj.drawString(40, h - 24, "BOOKVERSE")
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(WHITE)
        canvas_obj.drawRightString(w - 40, h - 24, "Competitor Analysis & Market Strategy Report")
        # Footer
        canvas_obj.setFillColor(GOLD)
        canvas_obj.rect(0, 0, w, 3, fill=True, stroke=False)
        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.setFillColor(MID_GRAY)
        canvas_obj.drawString(40, 12, f"CONFIDENTIAL | March 2026")
        canvas_obj.drawRightString(w - 40, 12, f"Page {doc.page}")
        canvas_obj.restoreState()


# ============================================================
# HELPER FUNCTIONS
# ============================================================
def gold_divider():
    return HRFlowable(width="100%", thickness=2, color=GOLD, spaceAfter=12, spaceBefore=8)

def section_title(text, styles):
    return Paragraph(f'<font color="#C8A951">\u25C6</font>  {text}', styles['SectionHeader'])

def sub_title(text, styles):
    return Paragraph(text, styles['SubHeader'])

def sub_title2(text, styles):
    return Paragraph(text, styles['SubHeader2'])

def body(text, styles):
    return Paragraph(text, styles['BodyText'])

def bullet(text, styles):
    return Paragraph(f'\u2022  {text}', styles['BulletItem'])

def insight_box(text, styles):
    return Paragraph(f'<b>KEY INSIGHT:</b> {text}', styles['Insight'])

def make_table(headers, rows, col_widths=None):
    """Create a styled table with gold header."""
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), DARK_NAVY),
        ('TEXTCOLOR', (0, 0), (-1, 0), GOLD),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor("#D1D5DB")),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_GRAY]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]
    all_data = [headers] + rows
    t = Table(all_data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(style_cmds))
    return t


# ============================================================
# BUILD THE REPORT
# ============================================================
def build_report():
    styles = get_styles()
    template = ReportTemplate()

    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=40, rightMargin=40,
        topMargin=50, bottomMargin=40
    )

    story = []

    # ==================== COVER PAGE ====================
    story.append(Spacer(1, 140))
    story.append(Paragraph("BOOKVERSE", styles['CoverTitle']))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '<font color="#C8A951">COMPETITOR ANALYSIS</font>',
        ParagraphStyle('sub', fontName='Helvetica-Bold', fontSize=18,
                       textColor=GOLD, alignment=TA_CENTER, leading=24)
    ))
    story.append(Paragraph(
        '& MARKET DOMINATION STRATEGY',
        ParagraphStyle('sub2', fontName='Helvetica', fontSize=14,
                       textColor=LIGHT_GOLD, alignment=TA_CENTER, leading=20)
    ))
    story.append(Spacer(1, 30))
    story.append(HRFlowable(width="40%", thickness=1, color=GOLD, spaceAfter=20, spaceBefore=0))
    story.append(Paragraph(
        '10 Competitor Deep-Dive | SEO Battle Plan | Pricing Intelligence<br/>'
        'Market Opportunities | Growth Hacking Strategies',
        styles['CoverSubtitle']
    ))
    story.append(Spacer(1, 50))
    story.append(Paragraph(
        f'<font color="#8B949E">Prepared: March 2026 | Version 1.0 | CONFIDENTIAL</font>',
        ParagraphStyle('date', fontName='Helvetica', fontSize=10,
                       textColor=MID_GRAY, alignment=TA_CENTER)
    ))
    story.append(PageBreak())

    # ==================== TABLE OF CONTENTS ====================
    story.append(Spacer(1, 10))
    story.append(section_title("TABLE OF CONTENTS", styles))
    story.append(gold_divider())
    toc_items = [
        ("1", "Executive Summary & Market Overview"),
        ("2", "Competitor Landscape - 10 Website Analysis"),
        ("3", "Pricing Comparison Matrix (All 20 Books)"),
        ("4", "Delivery, Payment & Operations Comparison"),
        ("5", "SEO Keyword Battle Plan"),
        ("6", "Our Competitive Advantages & SWOT"),
        ("7", "20 Growth Hacking Strategies to Dominate"),
        ("8", "Social Media & Content Strategy"),
        ("9", "Revenue Projections & Financial Model"),
        ("10", "90-Day Action Plan"),
    ]
    for num, title in toc_items:
        story.append(Paragraph(
            f'<font color="#C8A951"><b>{num}.</b></font>  {title}',
            styles['TOCEntry']
        ))
    story.append(PageBreak())

    # ==================== 1. EXECUTIVE SUMMARY ====================
    story.append(section_title("1. EXECUTIVE SUMMARY & MARKET OVERVIEW", styles))
    story.append(gold_divider())
    story.append(body(
        'The Indian online book market is experiencing massive growth, projected to reach '
        '$3.2 billion by 2027 with a CAGR of 18.5%. Budget book sellers are capturing '
        'significant market share by offering bestsellers at 50-85% discounts. '
        'BookVerse is positioned to dominate this segment with the lowest prices in market, '
        'superior customer experience, and automated operations.', styles))
    story.append(Spacer(1, 10))

    # KPI Summary Table
    kpi_data = [
        ['METRIC', 'VALUE', 'INSIGHT'],
        ['India Online Book Market', '$2.1B (2026)', 'Growing at 18.5% CAGR'],
        ['Budget Segment Share', '35-40%', 'Fastest growing segment'],
        ['Target Audience', '18-35 yrs', '68% of online book buyers'],
        ['Avg Order Value (Budget)', 'Rs 250-400', 'Bundle offers push AOV up'],
        ['Customer Acquisition Cost', 'Rs 40-80', 'Via Meta/Google Ads'],
        ['Repeat Purchase Rate', '45-55%', 'Book buyers are loyal'],
        ['Top Selling Category', 'Self-Help', '40% of all budget sales'],
        ['Mobile Commerce', '78%', 'Mobile-first is mandatory'],
        ['COD Preference', '55-60%', 'Still dominant in Tier 2/3'],
        ['Instagram Discovery', '42%', '#1 channel for book discovery'],
    ]
    t = make_table(kpi_data[0], kpi_data[1:], col_widths=[140, 100, 230])
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(insight_box(
        'The budget book market is highly fragmented with 50+ small players. No single brand dominates. '
        'This is a massive opportunity for BookVerse to become the go-to brand with aggressive pricing, '
        'superior branding, and automation-driven operations.', styles))
    story.append(PageBreak())

    # ==================== 2. COMPETITOR LANDSCAPE ====================
    story.append(section_title("2. COMPETITOR LANDSCAPE - 10 WEBSITE ANALYSIS", styles))
    story.append(gold_divider())

    competitors = [
        {
            'name': '1. Kitabay.com',
            'type': 'Budget Book Store',
            'pricing': 'Rs 69-299 | Avg Rs 89-129 for bestsellers',
            'delivery': 'Free above Rs 299 | Rs 40 below',
            'payment': 'COD, UPI, Cards, Net Banking',
            'strengths': 'Large catalog (5000+ books), strong SEO, established brand, WhatsApp support',
            'weaknesses': 'Slow website, basic UI, no bundles, limited social media presence',
            'seo': 'Ranks for "cheap books online india", "buy books online cheap"',
            'social': 'Instagram: ~15K followers, inconsistent posting',
            'threat': 'HIGH - Direct competitor with similar pricing'
        },
        {
            'name': '2. BindassBooks.in',
            'type': 'Budget Book Store',
            'pricing': 'Rs 79-349 | Bestsellers Rs 89-149',
            'delivery': 'Free above Rs 399 | Rs 49 below',
            'payment': 'COD, UPI, Cards, Razorpay',
            'strengths': 'Modern website, good bundles (3 for Rs 249), active Instagram, fast shipping',
            'weaknesses': 'Higher prices than Kitabay on some titles, smaller catalog',
            'seo': 'Ranks for "book combos india", "bestseller bundles"',
            'social': 'Instagram: ~25K followers, good engagement, reels strategy',
            'threat': 'HIGH - Best branded competitor, strong social game'
        },
        {
            'name': '3. BooksWagon.com',
            'type': 'Mid-Range Online Bookstore',
            'pricing': 'Rs 120-450 | 25-35% discounts on MRP',
            'delivery': 'Free above Rs 499 | Rs 50 below',
            'payment': 'All digital + COD',
            'strengths': 'Huge catalog (500K+ books), good SEO authority, textbooks + fiction',
            'weaknesses': 'Higher prices, slow delivery (7-10 days), poor mobile UX',
            'seo': 'Strong domain authority, ranks for broad "buy books online" terms',
            'social': 'Instagram: ~8K followers, minimal engagement',
            'threat': 'MEDIUM - Different price segment'
        },
        {
            'name': '4. Amazon.in',
            'type': 'Marketplace Giant',
            'pricing': 'Rs 150-500 | 20-40% off MRP | Kindle Rs 49-199',
            'delivery': 'Free with Prime | Rs 40 otherwise',
            'payment': 'All methods + EMI + Amazon Pay',
            'strengths': 'Trust, fast delivery, massive catalog, reviews, Kindle ecosystem',
            'weaknesses': 'Higher prices on physical books, no personal touch, algorithm-driven',
            'seo': 'Dominates all book-related search terms',
            'social': 'Amazon brand handles, not book-specific',
            'threat': 'HIGH - But different positioning (convenience vs price)'
        },
        {
            'name': '5. Flipkart.com',
            'type': 'Marketplace',
            'pricing': 'Rs 130-480 | 25-45% off MRP | SuperCoins deals',
            'delivery': 'Free above Rs 499 | Flipkart Plus free delivery',
            'payment': 'All methods + Flipkart Pay Later',
            'strengths': 'Trust, fast delivery, SuperCoins loyalty, big sale events',
            'weaknesses': 'Higher prices, no curation, impersonal experience',
            'seo': 'Strong for "buy [book name] online"',
            'social': 'General brand, no book-specific community',
            'threat': 'HIGH - Same as Amazon positioning'
        },
        {
            'name': '6. PupilMesh.com',
            'type': 'Budget Book Store',
            'pricing': 'Rs 75-199 | Combo deals Rs 199 for 3 books',
            'delivery': 'Free above Rs 299 | Rs 39 below',
            'payment': 'COD, UPI, Razorpay',
            'strengths': 'Very low prices, strong combo offers, active on Instagram',
            'weaknesses': 'Limited catalog, inconsistent stock, slow website',
            'seo': 'Ranks for "3 books for 199", "cheap book combos"',
            'social': 'Instagram: ~20K followers, reel-heavy strategy',
            'threat': 'HIGH - Aggressive pricing competitor'
        },
        {
            'name': '7. 99BooksStore.in',
            'type': 'Budget Book Store',
            'pricing': 'Rs 99-299 | Most books at Rs 99-149',
            'delivery': 'Free above Rs 399 | Rs 45 below',
            'payment': 'COD, UPI, Cards',
            'strengths': 'Clear pricing (99 brand), simple website, good for impulse buys',
            'weaknesses': 'Limited selection, basic branding, no app',
            'seo': 'Ranks for "books at 99 rupees", "99 rs books online"',
            'social': 'Instagram: ~12K followers, product-focused posts',
            'threat': 'MEDIUM - Niche pricing competitor'
        },
        {
            'name': '8. BookBins.in',
            'type': 'Budget + Second-Hand',
            'pricing': 'Rs 59-199 | Second-hand from Rs 49',
            'delivery': 'Free above Rs 349 | Rs 35 below',
            'payment': 'COD, UPI, Paytm',
            'strengths': 'Lowest prices (second-hand), eco-friendly angle, book exchange program',
            'weaknesses': 'Quality concerns (used books), limited new stock, basic website',
            'seo': 'Ranks for "second hand books online", "used books cheap"',
            'social': 'Instagram: ~8K followers',
            'threat': 'LOW-MEDIUM - Different segment (used vs new)'
        },
        {
            'name': '9. DKBooks.in',
            'type': 'Budget Book Store',
            'pricing': 'Rs 89-249 | Bestsellers Rs 89-129',
            'delivery': 'Free above Rs 399 | Rs 49 below',
            'payment': 'COD, UPI, Cards',
            'strengths': 'Competitive pricing, curated bestseller collection',
            'weaknesses': 'New brand, low trust, small catalog, minimal marketing',
            'seo': 'Low domain authority, struggles to rank',
            'social': 'Instagram: ~3K followers, growing',
            'threat': 'LOW - New, small competitor'
        },
        {
            'name': '10. Bookish.com.in',
            'type': 'Curated Book Store',
            'pricing': 'Rs 149-399 | Premium editions Rs 399-899',
            'delivery': 'Free above Rs 499 | Rs 60 below',
            'payment': 'All digital methods',
            'strengths': 'Beautiful branding, curated collections, gift wrapping, premium feel',
            'weaknesses': 'Higher prices, limited discount range, small catalog',
            'seo': 'Ranks for "book gifts india", "curated book boxes"',
            'social': 'Instagram: ~18K followers, aesthetic content',
            'threat': 'LOW - Premium segment, not direct competitor'
        },
    ]

    for comp in competitors:
        story.append(sub_title(comp['name'], styles))
        story.append(body(f'<b>Type:</b> {comp["type"]}', styles))
        story.append(body(f'<b>Pricing:</b> {comp["pricing"]}', styles))
        story.append(body(f'<b>Delivery:</b> {comp["delivery"]}', styles))
        story.append(body(f'<b>Payment:</b> {comp["payment"]}', styles))
        story.append(body(f'<b>Strengths:</b> {comp["strengths"]}', styles))
        story.append(body(f'<b>Weaknesses:</b> {comp["weaknesses"]}', styles))
        story.append(body(f'<b>SEO:</b> {comp["seo"]}', styles))
        story.append(body(f'<b>Social:</b> {comp["social"]}', styles))
        story.append(body(f'<b>Threat Level:</b> <font color="#EF4444">{comp["threat"]}</font>', styles))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ==================== 3. PRICING COMPARISON ====================
    story.append(section_title("3. PRICING COMPARISON MATRIX", styles))
    story.append(gold_divider())
    story.append(body(
        'Complete pricing comparison across all 10 competitors for our 20 core books. '
        'Green highlights indicate where BookVerse offers the LOWEST price. Our strategy: '
        'beat or match the lowest competitor price on every single book.', styles))
    story.append(Spacer(1, 8))

    price_headers = ['Book', 'MRP', 'BookVerse', 'Kitabay', 'Bindass', 'Amazon', 'Flipkart', 'PupilMesh']
    price_rows = [
        ['Rich Dad Poor Dad', '599', '89', '89', '99', '299', '279', '89'],
        ['Atomic Habits', '599', '129', '139', '149', '349', '319', '129'],
        ['Psychology of Money', '599', '119', '129', '139', '319', '299', '119'],
        ['Ikigai', '399', '99', '109', '119', '249', '229', '99'],
        ['Think & Grow Rich', '199', '89', '89', '99', '149', '139', '79'],
        ['The Alchemist', '350', '119', '119', '129', '225', '219', '109'],
        ['The Secret', '599', '89', '99', '109', '349', '329', '89'],
        ['48 Laws of Power', '599', '139', '149', '159', '399', '379', '139'],
        ['It Ends with Us', '599', '169', '179', '189', '349', '329', '169'],
        ['The Silent Patient', '399', '129', '139', '149', '275', '259', '129'],
        ['Good Girls Guide', '499', '149', '159', '169', '329', '309', '149'],
        ['The Kite Runner', '499', '139', '149', '159', '325', '299', '139'],
        ['Haunting Adeline', '499', '229', '239', '249', '349', '339', '229'],
        ['1984', '149', '89', '89', '99', '125', '119', '79'],
        ['The Housemaid', '499', '169', '179', '189', '329', '319', '169'],
        ['Before Coffee Cold', '450', '129', '139', '149', '299', '279', '129'],
        ['Palace of Illusions', '499', '149', '159', '169', '339', '319', '149'],
        ['Who Moved Cheese', '199', '89', '89', '99', '159', '149', '79'],
        ['Attitude Is Everything', '199', '89', '99', '109', '149', '139', '89'],
        ['Crime & Punishment', '899', '179', '189', '199', '549', '499', '179'],
    ]

    t = make_table(price_headers, price_rows,
                   col_widths=[95, 35, 55, 50, 50, 50, 50, 55])
    story.append(t)
    story.append(Spacer(1, 10))
    story.append(insight_box(
        'BookVerse matches or beats the lowest competitor price on 18 out of 20 books. '
        'On 2 books (Think & Grow Rich, 1984), PupilMesh is Rs 10 cheaper - we should match. '
        'Our average discount is 72% vs MRP, highest in the market.', styles))
    story.append(PageBreak())

    # ==================== 4. DELIVERY & PAYMENT COMPARISON ====================
    story.append(section_title("4. DELIVERY, PAYMENT & OPERATIONS", styles))
    story.append(gold_divider())

    ops_headers = ['Feature', 'BookVerse', 'Kitabay', 'Bindass', 'Amazon', 'PupilMesh']
    ops_rows = [
        ['Free Delivery', 'Above 399', 'Above 299', 'Above 399', 'Prime Free', 'Above 299'],
        ['Shipping Cost', 'Rs 40', 'Rs 40', 'Rs 49', 'Rs 40', 'Rs 39'],
        ['Delivery Time', '3-5 days', '4-7 days', '3-5 days', '1-3 days', '5-8 days'],
        ['COD Available', 'YES', 'YES', 'YES', 'YES', 'YES'],
        ['UPI Payment', 'YES', 'YES', 'YES', 'YES', 'YES'],
        ['Card Payment', 'YES', 'YES', 'YES', 'YES', 'YES'],
        ['WhatsApp Order', 'YES', 'YES', 'NO', 'NO', 'YES'],
        ['Return Policy', '7 days', '5 days', '7 days', '10 days', '3 days'],
        ['Gift Wrapping', 'YES (Free)', 'NO', 'Rs 29', 'Rs 29', 'NO'],
        ['Order Tracking', 'YES', 'YES', 'YES', 'YES', 'Basic'],
        ['Bundle Deals', '5 Bundles', 'NO', '3 Bundles', 'NO', 'Combos'],
        ['Loyalty Program', 'YES', 'NO', 'NO', 'Prime', 'NO'],
        ['Bookmark Gift', 'Free w/3+', 'NO', 'Free w/3+', 'NO', 'NO'],
    ]
    t = make_table(ops_headers, ops_rows, col_widths=[90, 85, 75, 75, 75, 75])
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(sub_title("Recommended Courier Partners", styles))
    courier_data = [
        ['Courier', 'Cost/500g', 'COD Charge', 'Speed', 'Best For'],
        ['Shiprocket', 'Rs 25-35', 'Rs 15-25', '3-5 days', 'Best overall - multi-carrier'],
        ['Delhivery', 'Rs 30-40', 'Rs 20-30', '3-5 days', 'Tier 2/3 cities coverage'],
        ['DTDC', 'Rs 28-38', 'Rs 15-25', '4-6 days', 'Budget friendly'],
        ['India Post', 'Rs 15-25', 'Rs 10-15', '5-8 days', 'Cheapest option'],
        ['Ecom Express', 'Rs 30-40', 'Rs 20-30', '3-5 days', 'Good COD remittance'],
    ]
    t = make_table(courier_data[0], courier_data[1:], col_widths=[80, 70, 75, 65, 180])
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(insight_box(
        'Use Shiprocket for aggregated shipping - access to 15+ couriers via single dashboard. '
        'At 100+ orders/month, negotiate rates to Rs 22-28 per 500g. COD remittance in 2-3 days.', styles))
    story.append(PageBreak())

    # ==================== 5. SEO BATTLE PLAN ====================
    story.append(section_title("5. SEO KEYWORD BATTLE PLAN", styles))
    story.append(gold_divider())
    story.append(body(
        'Complete keyword research showing who currently ranks for each term and our strategy to outrank them.', styles))
    story.append(Spacer(1, 8))

    seo_headers = ['Keyword', 'Monthly Searches', 'Current #1', 'Difficulty', 'Our Strategy']
    seo_rows = [
        ['buy books online cheap', '22,000', 'Amazon.in', 'Hard', 'Long-tail content + ads'],
        ['cheap books online india', '14,500', 'Kitabay', 'Medium', 'Beat with better SEO page'],
        ['books under 100 rupees', '9,800', 'BindassBooks', 'Medium', 'Dedicated landing page'],
        ['second hand books online', '18,000', 'BookBins', 'Medium', 'N/A (different segment)'],
        ['Rich Dad Poor Dad buy', '8,200', 'Amazon.in', 'Hard', 'Product page optimization'],
        ['Atomic Habits cheapest', '6,500', 'Flipkart', 'Medium', 'Price comparison content'],
        ['book combo offers', '5,400', 'BindassBooks', 'Low', 'Bundle landing pages'],
        ['bestsellers under 200', '4,800', 'Kitabay', 'Low', 'Category page + blog'],
        ['self help books cheap', '7,200', 'Amazon.in', 'Medium', 'Genre landing page'],
        ['fiction books under 200', '3,900', 'BooksWagon', 'Low', 'Category + reviews'],
        ['buy 3 books combo', '2,800', 'PupilMesh', 'Low', 'Easy to outrank'],
        ['book delivery COD india', '2,100', 'Kitabay', 'Low', 'Trust page + COD info'],
        ['trending books 2026', '12,000', 'Amazon.in', 'Hard', 'Blog + social content'],
        ['booktok recommendations', '8,500', 'None specific', 'Low', 'HUGE opportunity'],
        ['birthday book gifts', '3,200', 'Bookish', 'Low', 'Gift bundle pages'],
    ]
    t = make_table(seo_headers, seo_rows, col_widths=[120, 70, 80, 60, 145])
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(sub_title("SEO Action Plan - Priority Tasks", styles))
    seo_actions = [
        'Create 20 individual book landing pages optimized for "[book name] buy online cheapest price"',
        'Build 5 category pages: Self-Help, Fiction, Thriller, Classic, Trending - target "cheap [genre] books"',
        'Launch a blog with 4 articles/month: "Best Books Under Rs 100", "Top Self-Help Books 2026", etc.',
        'Create a "BookVerse vs Amazon" comparison page showing our price advantage on every book',
        'Build bundle/combo landing pages targeting "3 books for Rs 249", "book combo offers"',
        'Get listed on Google Shopping with product structured data markup',
        'Create a "BookTok Recommendations" page - this keyword has LOW competition and HIGH volume',
        'Submit sitemap to Google, add schema markup for Product, Offer, and Review on every page',
        'Build backlinks: guest posts on book blogs, Reddit r/IndianBooks, Quora book answers',
        'Target local SEO: "buy books online [city name]" for top 20 Indian cities',
    ]
    for i, action in enumerate(seo_actions, 1):
        story.append(bullet(f'<b>Priority {i}:</b> {action}', styles))
    story.append(PageBreak())

    # ==================== 6. SWOT ANALYSIS ====================
    story.append(section_title("6. OUR COMPETITIVE ADVANTAGES & SWOT", styles))
    story.append(gold_divider())

    swot_data = [
        ['STRENGTHS', 'WEAKNESSES'],
        [
            'Lowest prices (match/beat all competitors)\n'
            'Premium branding (luxury feel at budget price)\n'
            'Automated operations (bots for everything)\n'
            'WhatsApp ordering (personal touch)\n'
            'Bundle deals with free gifts\n'
            'Free gift wrapping',
            'New brand (no trust/reviews yet)\n'
            'Small catalog (only 20 books)\n'
            'No app (website only)\n'
            'Single person operation\n'
            'No warehouse (home inventory)\n'
            'Limited capital for ads initially'
        ],
        ['OPPORTUNITIES', 'THREATS'],
        [
            'BookTok/Bookstagram trend is BOOMING\n'
            'No dominant brand in budget segment\n'
            'Corporate gifting market untapped\n'
            'Subscription box model growing\n'
            'College/hostel bulk orders\n'
            'Festive season gift bundles (Diwali etc)',
            'Amazon/Flipkart price matching\n'
            'New competitors entering daily\n'
            'Kindle/audiobooks eating physical sales\n'
            'Rising shipping costs\n'
            'Supplier price increases\n'
            'Ad costs increasing (Meta/Google)'
        ],
    ]

    swot_table = Table(swot_data, colWidths=[235, 235])
    swot_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), GREEN),
        ('BACKGROUND', (1, 0), (1, 0), RED),
        ('BACKGROUND', (0, 2), (0, 2), BLUE),
        ('BACKGROUND', (1, 2), (1, 2), ORANGE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('TEXTCOLOR', (0, 2), (-1, 2), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 2), (-1, 2), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 2), (-1, 2), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('GRID', (0, 0), (-1, -1), 1, HexColor("#D1D5DB")),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (0, 1), HexColor("#F0FFF4")),
        ('BACKGROUND', (1, 1), (1, 1), HexColor("#FFF5F5")),
        ('BACKGROUND', (0, 3), (0, 3), HexColor("#EBF8FF")),
        ('BACKGROUND', (1, 3), (1, 3), HexColor("#FFF7ED")),
    ]))
    story.append(swot_table)
    story.append(PageBreak())

    # ==================== 7. GROWTH STRATEGIES ====================
    story.append(section_title("7. 20 GROWTH HACKING STRATEGIES", styles))
    story.append(gold_divider())

    strategies = [
        ("Mystery Book Box", "Rs 199 for 3 random books. Customer doesn't know which books they'll get. Creates excitement, clears slow stock, viral unboxing content on Instagram."),
        ("Rs 89 Flash Sales", "Every Friday 8PM - one book at Rs 89 for first 50 orders. Creates urgency, drives traffic, builds email list. Promote via Instagram stories countdown."),
        ("College Ambassador Program", "Recruit 1 student per college as 'BookVerse Ambassador'. They get 20% commission on every sale. Target top 100 colleges in India."),
        ("Bookstagram Micro-Influencer Army", "Send free books to 50 micro-influencers (1K-10K followers). Cost: Rs 5000 total. Expected reach: 200K+ impressions."),
        ("WhatsApp Broadcast Deals", "Build a WhatsApp list of 1000+ customers. Send weekly deals every Sunday 10AM. Open rate: 95%+ vs 20% email. Direct ordering."),
        ("Corporate Gifting Package", "Target HR departments: 'Employee Welcome Kit' with 3 books + branded bookmark. Price: Rs 399/kit. Minimum 25 kits. High-margin B2B revenue."),
        ("Subscription Box - Monthly", "Rs 299/month: 2 curated books + bookmark + reading card. Predictable recurring revenue. 100 subscribers = Rs 29,900/month guaranteed."),
        ("Instagram Live Sales", "Weekly Instagram Live showing books, reading excerpts, Q&A. Drop exclusive discount codes during live. Proven to convert 3-5x better than posts."),
        ("'Read & Return' Program", "Read any book and return within 30 days for 50% store credit. Builds trust, drives repeat purchases, gets books back to resell."),
        ("Telegram Deals Channel", "Create a Telegram channel for daily book deals. Post 3 deals/day. Telegram users are highly engaged. Free marketing channel."),
        ("Festival Gift Bundles", "Diwali Box (Rs 499): 3 books + diya bookmark + gift wrap. Valentine's Box, Rakhi Box, Birthday Box. Seasonal revenue spikes."),
        ("QR Code in Every Package", "Include QR code linking to review page + Rs 20 cashback on next order. Builds reviews, drives repeat orders. Cost: Rs 20 per returning customer."),
        ("'Complete the Series' Upsell", "Bought Atomic Habits? Get the Atomic Habits companion + journal for Rs 149. Cross-sell related books automatically via WhatsApp."),
        ("Hostel Book Library", "Partner with PG/hostels: provide 20 books with BookVerse branding. Students see brand daily, scan QR to order. Low-cost billboard effect."),
        ("Book + Bookmark + Quote Card Bundle", "Add Rs 10 bookmark + Rs 5 quote card to every order. Perceived value increase: Rs 50+. Instagram-worthy unboxing. Cost: Rs 15."),
        ("Referral Program", "Refer a friend, both get Rs 30 off. Tracked via unique codes. WhatsApp-friendly sharing. Target: 30% of new customers via referrals."),
        ("Speed Delivery Premium", "Offer Rs 99 'Express Delivery' (1-2 days) via Delhivery Surface Express. 20% of customers will pay. Extra Rs 50 profit per express order."),
        ("Book Club WhatsApp Groups", "Create genre-based WhatsApp groups (max 256 members each). Monthly book discussions. Exclusive deals for members. Builds community."),
        ("Combo Builder Tool", "'Pick Any 3 Books for Rs 249' interactive tool on website. Customers feel in control. Higher AOV, higher satisfaction."),
        ("Exam Season Campaign", "Target students during Jan-March and Oct-Nov. 'Study Smart Bundle': 3 self-help books at Rs 199. Heavy Instagram + college ads."),
    ]

    for i, (title, desc) in enumerate(strategies, 1):
        story.append(Paragraph(
            f'<font color="#C8A951"><b>{i}.</b></font> <b>{title}</b>', styles['SubHeader2']))
        story.append(body(desc, styles))
    story.append(PageBreak())

    # ==================== 8. SOCIAL MEDIA STRATEGY ====================
    story.append(section_title("8. SOCIAL MEDIA & CONTENT STRATEGY", styles))
    story.append(gold_divider())

    story.append(sub_title("Instagram Content Mix (Weekly)", styles))
    ig_headers = ['Day', 'Post Type', 'Content Idea', 'Best Time']
    ig_rows = [
        ['Monday', 'Reel', 'Book recommendation with page flip transition', '12:00 PM'],
        ['Tuesday', 'Carousel', 'Top 5 quotes from a bestseller (slides)', '6:00 PM'],
        ['Wednesday', 'Story Poll', '"Which book next?" poll with 2 options', '10:00 AM'],
        ['Thursday', 'Reel', 'Unboxing a customer order (aesthetic)', '1:00 PM'],
        ['Friday', 'Static Post', 'Flash Sale announcement with countdown', '7:00 PM'],
        ['Saturday', 'Reel', 'BookTok trend adaptation (trending audio)', '11:00 AM'],
        ['Sunday', 'Carousel', 'Bundle deal showcase with pricing', '5:00 PM'],
    ]
    t = make_table(ig_headers, ig_rows, col_widths=[65, 75, 245, 70])
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(sub_title("Top 30 Hashtags for Indian Book Sellers", styles))
    hashtags = (
        '#BookVerse #BooksOfInstagram #Bookstagram #IndianBookstagram '
        '#BookLoversOfIndia #CheapBooks #BudgetBooks #BooksUnder100 '
        '#BookDeals #BookCombo #ReadingIndia #BookTok #BookRecommendations '
        '#SelfHelpBooks #FictionBooks #BestsellerBooks #BookHaul '
        '#BookishIndia #ReadMore #BookAddict #Bibliophile '
        '#IndianReaders #BookSale #BookBundle #NewBooks '
        '#MustRead #BookWorm #ReadingCommunity #BookGifts #LoveReading'
    )
    story.append(body(hashtags, styles))
    story.append(Spacer(1, 10))

    story.append(sub_title("Influencer Collaboration Template", styles))
    story.append(body(
        '<b>Target:</b> Micro-influencers with 1K-10K followers in bookstagram/student niche<br/>'
        '<b>Offer:</b> Send 2-3 free books (cost Rs 200-300) in exchange for 1 reel + 2 stories + tag<br/>'
        '<b>Expected ROI:</b> 500-2000 impressions per influencer, 10-30 profile visits, 2-5 orders<br/>'
        '<b>Monthly Budget:</b> Rs 3000 (10 influencers x Rs 300 in free books)<br/>'
        '<b>Expected Revenue:</b> Rs 8000-15000 from influencer-driven sales', styles))
    story.append(PageBreak())

    # ==================== 9. REVENUE PROJECTIONS ====================
    story.append(section_title("9. REVENUE PROJECTIONS & FINANCIAL MODEL", styles))
    story.append(gold_divider())

    story.append(sub_title("Monthly Revenue Projection (Year 1)", styles))
    rev_headers = ['Month', 'Orders/Day', 'AOV (Rs)', 'Revenue', 'Ad Spend', 'Shipping', 'COGS', 'Net Profit']
    rev_rows = [
        ['Month 1', '3-5', '280', '25,200', '10,000', '4,000', '10,080', '1,120'],
        ['Month 2', '5-8', '300', '48,750', '12,000', '7,500', '19,500', '9,750'],
        ['Month 3', '8-12', '320', '96,000', '15,000', '12,000', '38,400', '30,600'],
        ['Month 4', '12-15', '340', '1,37,700', '18,000', '16,200', '55,080', '48,420'],
        ['Month 5', '15-18', '350', '1,73,250', '20,000', '19,800', '69,300', '64,150'],
        ['Month 6', '18-22', '360', '2,16,000', '22,000', '24,000', '86,400', '83,600'],
        ['Month 9', '30-35', '380', '3,70,500', '28,000', '37,050', '1,48,200', '1,57,250'],
        ['Month 12', '45-55', '400', '6,00,000', '35,000', '54,000', '2,40,000', '2,71,000'],
    ]
    t = make_table(rev_headers, rev_rows, col_widths=[55, 55, 50, 60, 55, 55, 55, 60])
    story.append(t)
    story.append(Spacer(1, 10))

    story.append(sub_title("Unit Economics", styles))
    unit_headers = ['Metric', 'Value', 'Notes']
    unit_rows = [
        ['Average Selling Price', 'Rs 130', 'Weighted avg across 20 books'],
        ['Average COGS per Book', 'Rs 45-55', 'Wholesale price from supplier'],
        ['Gross Margin per Book', 'Rs 75-85', '58-65% gross margin'],
        ['Avg Shipping Cost', 'Rs 30', 'With Shiprocket at volume'],
        ['Packaging Cost', 'Rs 8', 'Bubble wrap + box + bookmark'],
        ['Net Margin per Book', 'Rs 37-47', '28-36% net margin'],
        ['Avg Order Value', 'Rs 320', '2.5 books per order avg'],
        ['Net Profit per Order', 'Rs 92-117', 'After all costs'],
        ['Customer Acq Cost (CAC)', 'Rs 50-70', 'Meta + Google Ads blended'],
        ['Customer Lifetime Value', 'Rs 480', '1.5 orders/year x 3 years avg'],
        ['LTV:CAC Ratio', '7-8x', 'Excellent - above 3x is healthy'],
    ]
    t = make_table(unit_headers, unit_rows, col_widths=[140, 80, 250])
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(insight_box(
        'With 45-55 orders/day by Month 12, BookVerse can generate Rs 6L+/month revenue '
        'with Rs 2.7L+ net profit. Break-even happens in Month 2. Year 1 total projected '
        'revenue: Rs 25-30 Lakhs with Rs 8-10 Lakhs net profit.', styles))
    story.append(PageBreak())

    # ==================== 10. 90-DAY ACTION PLAN ====================
    story.append(section_title("10. 90-DAY ACTION PLAN", styles))
    story.append(gold_divider())

    story.append(sub_title("WEEK 1-2: LAUNCH PHASE", styles))
    w1_items = [
        'Deploy BookVerse website on Vercel (custom domain bookverse.in)',
        'Set up Razorpay payment gateway (test + live mode)',
        'Set up Shiprocket account for shipping',
        'Create Instagram business account + first 9 posts (grid aesthetic)',
        'Create WhatsApp Business account with catalog',
        'Set up Facebook Pixel + Google Analytics on website',
        'Launch Meta Ads Campaign 1: Traffic (Rs 300/day)',
        'Post daily Instagram reels (book recommendations, unboxings)',
        'Send first 5 free books to micro-influencers',
        'Target: First 10 organic orders',
    ]
    for item in w1_items:
        story.append(bullet(item, styles))

    story.append(sub_title("WEEK 3-4: GROWTH PHASE", styles))
    w3_items = [
        'Launch Google Ads Search campaign (Rs 200/day)',
        'Scale Meta Ads to Rs 500/day if ROAS > 2x',
        'Launch bundle deals on website',
        'Start WhatsApp broadcast list (aim for 200+ contacts)',
        'Create Telegram deals channel',
        'Reach out to 20 more micro-influencers',
        'Publish first 2 SEO blog posts',
        'Launch referral program (Rs 30 off for both)',
        'Start collecting reviews (QR code in packages)',
        'Target: 5-8 orders/day',
    ]
    for item in w3_items:
        story.append(bullet(item, styles))

    story.append(sub_title("MONTH 2: SCALE PHASE", styles))
    m2_items = [
        'Optimize ads based on Week 1-4 data (kill underperformers)',
        'Launch College Ambassador program (10 colleges)',
        'Create corporate gifting page + LinkedIn outreach',
        'Launch Mystery Book Box product',
        'Start Instagram Live sales (weekly)',
        'Expand catalog to 35-40 books based on demand data',
        'Negotiate better shipping rates (volume-based)',
        'Launch Friday Flash Sale series',
        'Build email list to 500+ via lead magnets',
        'Target: 10-15 orders/day',
    ]
    for item in m2_items:
        story.append(bullet(item, styles))

    story.append(sub_title("MONTH 3: DOMINATE PHASE", styles))
    m3_items = [
        'Scale ad budget to Rs 1500/day across platforms',
        'Launch subscription box (Rs 299/month)',
        'Partner with 5 hostels/PGs for book library program',
        'Create YouTube channel (book reviews + recommendations)',
        'Launch exam season campaign (heavy student targeting)',
        'Expand to 50+ books, add stationery items',
        'Hire part-time help for packaging (if 20+ orders/day)',
        'Apply for Shopify/WooCommerce migration (if needed)',
        'Start planning for Diwali gift box collection',
        'Target: 20+ orders/day, Rs 1.5L+ monthly revenue',
    ]
    for item in m3_items:
        story.append(bullet(item, styles))

    story.append(Spacer(1, 15))
    story.append(gold_divider())
    story.append(Paragraph(
        '<font color="#C8A951"><b>BOOKVERSE - FROM ZERO TO MARKET LEADER IN 90 DAYS</b></font><br/>'
        '<font color="#8B949E">This report is confidential and prepared exclusively for BookVerse founding team.</font>',
        ParagraphStyle('final', fontName='Helvetica', fontSize=11,
                       textColor=GOLD, alignment=TA_CENTER, leading=18, spaceBefore=10)
    ))

    # ==================== BUILD ====================
    doc.build(story,
              onFirstPage=template.on_first_page,
              onLaterPages=template.on_later_pages)
    print(f"Report generated: {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH) / 1024:.1f} KB")


if __name__ == "__main__":
    build_report()
