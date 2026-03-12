#!/usr/bin/env python3
"""
Social Media Content Bot
------------------------
Generates a weekly content calendar for Instagram/Facebook with
book quotes, promotions, tips, and engagement posts.

Usage:
    python social_media_bot.py                  # Generate this week's calendar
    python social_media_bot.py --type quote     # Generate a single quote post
    python social_media_bot.py --type botd      # Book of the Day
    python social_media_bot.py --type bundle    # Bundle promo
    python social_media_bot.py --type tip       # Reading tip
    python social_media_bot.py --type review    # Review template
"""

import json
import os
import random
import sys
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CALENDAR_FILE = os.path.join(BASE_DIR, "content_calendar.json")

BOOKS = [
    ("Rich Dad Poor Dad", "Robert T. Kiyosaki", 89, "Personal Finance"),
    ("Atomic Habits", "James Clear", 129, "Self-Help"),
    ("Psychology of Money", "Morgan Housel", 119, "Finance"),
    ("Ikigai", "Hector Garcia & Francesc Miralles", 99, "Self-Help"),
    ("Think and Grow Rich", "Napoleon Hill", 89, "Personal Development"),
    ("The Alchemist", "Paulo Coelho", 119, "Fiction"),
    ("The Secret", "Rhonda Byrne", 89, "Self-Help"),
    ("48 Laws of Power", "Robert Greene", 139, "Strategy"),
    ("It Ends with Us", "Colleen Hoover", 169, "Romance"),
    ("The Silent Patient", "Alex Michaelides", 129, "Thriller"),
    ("A Good Girl's Guide to Murder", "Holly Jackson", 149, "Mystery"),
    ("The Kite Runner", "Khaled Hosseini", 139, "Literary Fiction"),
    ("Haunting Adeline", "H.D. Carlton", 229, "Dark Romance"),
    ("1984", "George Orwell", 89, "Classic"),
    ("The Housemaid", "Freida McFadden", 169, "Thriller"),
    ("Before the Coffee Gets Cold", "Toshikazu Kawaguchi", 129, "Fiction"),
    ("Palace of Illusions", "Chitra Banerjee Divakaruni", 149, "Mythology"),
    ("Who Moved My Cheese", "Spencer Johnson", 89, "Business"),
    ("Attitude Is Everything", "Jeff Keller", 89, "Self-Help"),
    ("Crime and Punishment", "Fyodor Dostoevsky", 179, "Classic"),
]

BUNDLES = [
    {
        "name": "Self-Help Starter Pack",
        "books": ["Rich Dad Poor Dad", "Atomic Habits", "Ikigai"],
        "price": 269,
        "original": 317,
    },
    {
        "name": "Thriller Bundle",
        "books": ["The Silent Patient", "The Housemaid", "A Good Girl's Guide to Murder"],
        "price": 399,
        "original": 447,
    },
    {
        "name": "Classic Literature Set",
        "books": ["1984", "The Alchemist", "The Kite Runner"],
        "price": 299,
        "original": 347,
    },
    {
        "name": "Mindset Collection",
        "books": ["Psychology of Money", "Think and Grow Rich", "Attitude Is Everything"],
        "price": 249,
        "original": 297,
    },
    {
        "name": "Bestseller Box",
        "books": ["It Ends with Us", "Haunting Adeline", "Before the Coffee Gets Cold"],
        "price": 469,
        "original": 527,
    },
]

# ---------------------------------------------------------------------------
# Book quotes library (60 quotes)
# ---------------------------------------------------------------------------

BOOK_QUOTES = [
    # Rich Dad Poor Dad
    ("The poor and the middle class work for money. The rich have money work for them.", "Rich Dad Poor Dad"),
    ("It's not how much money you make, but how much money you keep.", "Rich Dad Poor Dad"),
    ("The single most powerful asset we all have is our mind.", "Rich Dad Poor Dad"),
    # Atomic Habits
    ("Every action you take is a vote for the type of person you wish to become.", "Atomic Habits"),
    ("You do not rise to the level of your goals. You fall to the level of your systems.", "Atomic Habits"),
    ("Habits are the compound interest of self-improvement.", "Atomic Habits"),
    # Psychology of Money
    ("Doing well with money has a little to do with how smart you are and a lot to do with how you behave.", "Psychology of Money"),
    ("Wealth is what you don't see.", "Psychology of Money"),
    ("The highest form of wealth is the ability to wake up every morning and say, I can do whatever I want today.", "Psychology of Money"),
    # Ikigai
    ("Only staying active will make you want to live a hundred years.", "Ikigai"),
    ("Our ikigai is different for all of us, but one thing we have in common is that we are all searching for meaning.", "Ikigai"),
    ("There is a tension between what is good for someone and what they want to do.", "Ikigai"),
    # Think and Grow Rich
    ("Whatever the mind can conceive and believe, it can achieve.", "Think and Grow Rich"),
    ("The starting point of all achievement is desire.", "Think and Grow Rich"),
    ("Strength and growth come only through continuous effort and struggle.", "Think and Grow Rich"),
    # The Alchemist
    ("When you want something, all the universe conspires in helping you to achieve it.", "The Alchemist"),
    ("It's the possibility of having a dream come true that makes life interesting.", "The Alchemist"),
    ("People learn, early in their lives, what is their reason for being.", "The Alchemist"),
    # The Secret
    ("Your thoughts become things.", "The Secret"),
    ("Whatever is going on in your mind is what you are attracting.", "The Secret"),
    ("The only reason any person does not have enough money is because they are blocking money from coming to them with their thoughts.", "The Secret"),
    # 48 Laws of Power
    ("When you show yourself to the world and display your talents, you naturally stir all kinds of resentment.", "48 Laws of Power"),
    ("Never waste valuable time, or mental peace of mind, on the affairs of others.", "48 Laws of Power"),
    ("The best deceptions are the ones that seem to give the other person a choice.", "48 Laws of Power"),
    # It Ends with Us
    ("There is no such thing as bad people. We're all just people who sometimes do bad things.", "It Ends with Us"),
    ("Just because someone hurts you doesn't mean you can simply stop loving them.", "It Ends with Us"),
    ("All humans make mistakes. What determines a person's character aren't the mistakes we make. It's how we take those mistakes and turn them into lessons.", "It Ends with Us"),
    # The Silent Patient
    ("But it's hard to see clearly when you're in the middle of a storm.", "The Silent Patient"),
    # The Kite Runner
    ("For you, a thousand times over.", "The Kite Runner"),
    ("There is only one sin. And that is theft. When you tell a lie, you steal someone's right to the truth.", "The Kite Runner"),
    # 1984
    ("Who controls the past controls the future. Who controls the present controls the past.", "1984"),
    ("War is peace. Freedom is slavery. Ignorance is strength.", "1984"),
    ("In a time of deceit telling the truth is a revolutionary act.", "1984"),
    # Before the Coffee Gets Cold
    ("Time waits for no one, but humans have the power to change the meaning of time.", "Before the Coffee Gets Cold"),
    ("The present is all you have. It is not the future that needs changing, but the heart.", "Before the Coffee Gets Cold"),
    # Palace of Illusions
    ("We are the choices we make.", "Palace of Illusions"),
    ("A problem becomes a problem only when you believe it to be so.", "Palace of Illusions"),
    # Who Moved My Cheese
    ("What would you do if you weren't afraid?", "Who Moved My Cheese"),
    ("The quicker you let go of old cheese, the sooner you find new cheese.", "Who Moved My Cheese"),
    ("Movement in a new direction helps you find new cheese.", "Who Moved My Cheese"),
    # Attitude Is Everything
    ("Your attitude determines your altitude.", "Attitude Is Everything"),
    ("You are the only person on earth who can use your ability.", "Attitude Is Everything"),
    # Crime and Punishment
    ("Pain and suffering are always inevitable for a large intelligence and a deep heart.", "Crime and Punishment"),
    ("To go wrong in one's own way is better than to go right in someone else's.", "Crime and Punishment"),
    # Additional inspiring book quotes
    ("A reader lives a thousand lives before he dies. The man who never reads lives only one.", "A Dance with Dragons"),
    ("Books are a uniquely portable magic.", "On Writing"),
    ("I have always imagined that Paradise will be a kind of library.", "Jorge Luis Borges"),
    ("Reading is essential for those who seek to rise above the ordinary.", "Jim Rohn"),
    ("The more that you read, the more things you will know.", "Dr. Seuss"),
    ("A book is a dream that you hold in your hand.", "Neil Gaiman"),
    ("One must always be careful of books and what is inside them.", "Clockwork Angel"),
    ("Reading brings us unknown friends.", "Honore de Balzac"),
    ("Books are mirrors: you only see in them what you already have inside you.", "The Shadow of the Wind"),
    ("There is no friend as loyal as a book.", "Ernest Hemingway"),
    ("Reading is to the mind what exercise is to the body.", "Joseph Addison"),
    ("A great book should leave you with many experiences, and slightly exhausted at the end.", "William Styron"),
    ("Until I feared I would lose it, I never loved to read. One does not love breathing.", "To Kill a Mockingbird"),
    ("I do believe something very magical can happen when you read a good book.", "J.K. Rowling"),
    ("Books are the quietest and most constant of friends.", "Charles W. Eliot"),
    ("Think before you speak. Read before you think.", "Fran Lebowitz"),
    ("Reading furnishes the mind only with materials of knowledge.", "John Locke"),
    ("A book is a gift you can open again and again.", "Garrison Keillor"),
]

# ---------------------------------------------------------------------------
# Hashtag sets for Indian book sellers
# ---------------------------------------------------------------------------

CORE_HASHTAGS = [
    "#bookstagram", "#bookstagramindia", "#indianbookstagram",
    "#booksofinstagram", "#booklover", "#bookish",
    "#readersofinstagram", "#bibliophile", "#booknerd",
    "#instabooks", "#bookaddict", "#bookworm",
]

SALE_HASHTAGS = [
    "#booksale", "#bookdeal", "#cheapbooks",
    "#affordablebooks", "#booksoffer", "#bookdiscount",
    "#indianbooks", "#buybooks", "#bookshop",
    "#onlinebookstore", "#booksinindia", "#bookshopping",
]

GENRE_HASHTAGS = {
    "Self-Help": ["#selfhelpbooks", "#personalgrowth", "#motivationalbooks", "#selfimprovement"],
    "Fiction": ["#fictionbooks", "#fictionreads", "#bookrecommendations", "#mustread"],
    "Thriller": ["#thrillerbooks", "#mysterybooks", "#suspense", "#pageturner"],
    "Romance": ["#romancebooks", "#romancereads", "#lovetoread", "#bookboyfriend"],
    "Classic": ["#classicbooks", "#classicliterature", "#timelessbooks", "#literaryclassics"],
    "Finance": ["#financebooks", "#moneybooks", "#financialliteracy", "#investinginbooks"],
    "Personal Finance": ["#personalfinance", "#moneymanagement", "#richthinking", "#financialfreedom"],
    "Personal Development": ["#personaldevelopment", "#growthmindset", "#successmindset"],
    "Strategy": ["#strategybooks", "#powerbooks", "#leadership", "#success"],
    "Mystery": ["#mysterybooks", "#whodunit", "#crimefiction", "#mysteryreads"],
    "Dark Romance": ["#darkromance", "#darkromancebooks", "#spicybooks", "#booktok"],
    "Mythology": ["#indianmythology", "#mythologybooks", "#mahabharata", "#indianauthors"],
    "Business": ["#businessbooks", "#entrepreneurbooks", "#startupbooks", "#businessmindset"],
    "Literary Fiction": ["#literaryfiction", "#contemporaryfiction", "#emotionalread"],
}

ENGAGEMENT_HASHTAGS = [
    "#whatareyoureading", "#currentlyreading", "#tbr",
    "#bookhaul", "#newbooks", "#bookreview",
    "#readingcommunity", "#readinglist", "#readmore",
]

# Optimal posting times for India (IST)
BEST_TIMES = {
    "morning": "8:00 AM IST",
    "afternoon": "1:00 PM IST",
    "evening": "6:30 PM IST",
    "night": "9:00 PM IST",
}

# ---------------------------------------------------------------------------
# Post generators
# ---------------------------------------------------------------------------

def _pick_hashtags(genre: str = None, extra: list = None, count: int = 25) -> list[str]:
    """Assemble a hashtag set, capped at `count`."""
    tags = list(CORE_HASHTAGS)
    if genre and genre in GENRE_HASHTAGS:
        tags += GENRE_HASHTAGS[genre]
    if extra:
        tags += extra
    tags += random.sample(ENGAGEMENT_HASHTAGS, min(3, len(ENGAGEMENT_HASHTAGS)))
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            unique.append(t)
    return unique[:count]


def generate_quote_post() -> dict:
    """Create a book-quote post."""
    quote, source = random.choice(BOOK_QUOTES)
    hashtags = _pick_hashtags(extra=["#bookquotes", "#quotestoliveby", "#dailyquote"])
    return {
        "post_type": "book_quote",
        "caption": f'"{quote}"\n\n— {source}\n\nDouble-tap if this resonates with you! Which book quote changed YOUR life? Tell us below.\n\nShop this book & more at our store. Link in bio.',
        "hashtags": hashtags,
        "suggested_image_description": (
            f"Aesthetic flat-lay of the book '{source}' on a wooden table with "
            "a coffee cup and reading glasses. The quote is overlaid in elegant "
            "serif font on a muted background. Warm, cozy lighting."
        ),
        "best_time_to_post": BEST_TIMES["evening"],
    }


def generate_book_of_the_day() -> dict:
    """Create a 'Book of the Day' feature post."""
    title, author, price, genre = random.choice(BOOKS)
    hashtags = _pick_hashtags(genre=genre, extra=["#bookoftheday", "#botd", "#bookrecommendation"])
    return {
        "post_type": "book_of_the_day",
        "caption": (
            f"BOOK OF THE DAY\n\n"
            f"{title} by {author}\n\n"
            f"Genre: {genre}\n"
            f"Price: Just Rs.{price}/-\n\n"
            f"Why you'll love it: A must-read for anyone who loves {genre.lower()} books. "
            f"This one will stay with you long after the last page.\n\n"
            f"Free bookmark with every order!\n"
            f"Order now — link in bio.\n\n"
            f"Have you read this? Rate it out of 5 in the comments!"
        ),
        "hashtags": hashtags,
        "suggested_image_description": (
            f"Clean product photo of '{title}' by {author} standing upright "
            "against a pastel background. A small plant and fairy lights in "
            "the background. Price tag overlay in the corner."
        ),
        "best_time_to_post": BEST_TIMES["morning"],
    }


def generate_bundle_promo() -> dict:
    """Create a bundle promotion post."""
    bundle = random.choice(BUNDLES)
    savings = bundle["original"] - bundle["price"]
    book_list = "\n".join(f"  {b}" for b in bundle["books"])
    hashtags = _pick_hashtags(extra=SALE_HASHTAGS[:4] + ["#bookbundle", "#bundledeal"])
    return {
        "post_type": "bundle_promotion",
        "caption": (
            f"BUNDLE DEAL\n\n"
            f"{bundle['name']}\n\n"
            f"What's inside:\n{book_list}\n\n"
            f"Bundle Price: Rs.{bundle['price']}/- (Save Rs.{savings}!)\n"
            f"MRP: Rs.{bundle['original']}/-\n\n"
            f"Perfect gift for a book lover — or treat yourself!\n"
            f"Limited stock. DM to order or use the link in bio.\n\n"
            f"Tag a friend who needs this bundle!"
        ),
        "hashtags": hashtags,
        "suggested_image_description": (
            f"Styled flat-lay of the three books in the '{bundle['name']}' "
            "arranged in a fan shape on a marble surface. A 'SAVE' badge "
            f"showing Rs.{savings} off. Gift wrap ribbon in the corner."
        ),
        "best_time_to_post": BEST_TIMES["afternoon"],
    }


def generate_reading_tip() -> dict:
    """Create a reading tip / recommendation post."""
    tips = [
        ("5 Books That Will Change Your Mindset in 2026",
         "1. Atomic Habits\n2. Psychology of Money\n3. Think and Grow Rich\n4. Ikigai\n5. Attitude Is Everything\n\nAll available at unbeatable prices. Start your transformation today!"),
        ("How to Build a Reading Habit",
         "1. Start with just 10 pages a day\n2. Read before bed instead of scrolling\n3. Keep a book on your desk always\n4. Join a reading challenge\n5. Reward yourself after finishing each book\n\nWhich tip will you try first?"),
        ("Books vs Phone: The 30-Day Challenge",
         "Replace 30 minutes of screen time with reading for 30 days. Here's what happens:\n\nWeek 1: You feel restless\nWeek 2: You start enjoying it\nWeek 3: You look forward to it\nWeek 4: You can't stop\n\nWho's in? Comment 'I'M IN' below!"),
        ("The 5 Genres Every Reader Should Explore",
         "1. Self-Help: Build better habits\n2. Thriller: Keep your mind sharp\n3. Classic Literature: Timeless wisdom\n4. Finance: Grow your wealth\n5. Fiction: Expand your imagination\n\nWe have bestsellers in ALL genres. Check our collection!"),
        ("Why Reading Physical Books Beats Kindle",
         "1. The smell of new pages\n2. No screen fatigue\n3. Better memory retention\n4. The joy of a bookshelf\n5. You can lend them to friends\n\nNothing beats holding a real book. Agree? Tell us your favorite thing about physical books!"),
    ]
    title, body = random.choice(tips)
    hashtags = _pick_hashtags(extra=["#readingtips", "#booktips", "#readinghabits", "#bookloversofinstagram"])
    return {
        "post_type": "reading_tip",
        "caption": f"{title}\n\n{body}",
        "hashtags": hashtags,
        "suggested_image_description": (
            f"Carousel or infographic post with the title '{title}' on the first slide. "
            "Clean design with book illustrations, numbered tips on each slide. "
            "Brand colors with readable fonts. Last slide has a CTA."
        ),
        "best_time_to_post": BEST_TIMES["night"],
    }


def generate_review_template() -> dict:
    """Create a customer review / testimonial template post."""
    title, author, price, genre = random.choice(BOOKS)
    templates = [
        (
            f"READER REVIEW\n\n"
            f"'{title}' by {author}\n\n"
            f"'This book completely changed the way I think about {genre.lower()}. "
            f"Finished it in 2 days. Must read!' — Verified Buyer\n\n"
            f"Rating: 4.8/5\n"
            f"Price: Rs.{price}/-\n\n"
            f"Have you read this? Drop your mini-review below!"
        ),
        (
            f"WHAT OUR READERS SAY\n\n"
            f"Book: {title}\n"
            f"Author: {author}\n\n"
            f"'Ordered on Monday, received by Wednesday. The book quality is amazing "
            f"and the price is the best I found anywhere!' — Happy Customer\n\n"
            f"Fast delivery. Best prices. Real books.\n"
            f"Order yours today — link in bio."
        ),
    ]
    caption = random.choice(templates)
    hashtags = _pick_hashtags(genre=genre, extra=["#bookreview", "#customerreview", "#happycustomer"])
    return {
        "post_type": "customer_review",
        "caption": caption,
        "hashtags": hashtags,
        "suggested_image_description": (
            f"Customer testimonial design with a 5-star rating graphic. "
            f"Photo of '{title}' with a review quote overlay. "
            "Clean white background with brand accent colors."
        ),
        "best_time_to_post": BEST_TIMES["afternoon"],
    }


# Map of post types to generators
POST_GENERATORS = {
    "quote": generate_quote_post,
    "botd": generate_book_of_the_day,
    "bundle": generate_bundle_promo,
    "tip": generate_reading_tip,
    "review": generate_review_template,
}


# ---------------------------------------------------------------------------
# Weekly calendar
# ---------------------------------------------------------------------------

def generate_weekly_calendar() -> dict:
    """
    Build a 7-day content calendar with 2 posts per day.

    Schedule pattern per day:
        Morning post  – rotates through: botd, quote, bundle, tip, review, quote, botd
        Evening post  – rotates through: quote, tip, review, bundle, botd, bundle, review
    """
    morning_rotation = ["botd", "quote", "bundle", "tip", "review", "quote", "botd"]
    evening_rotation = ["quote", "tip", "review", "bundle", "botd", "bundle", "review"]

    today = datetime.now().date()
    calendar = {
        "generated_at": datetime.now().isoformat(),
        "week_start": today.isoformat(),
        "week_end": (today + timedelta(days=6)).isoformat(),
        "days": [],
    }

    for day_offset in range(7):
        date = today + timedelta(days=day_offset)
        day_name = date.strftime("%A")

        morning_type = morning_rotation[day_offset]
        evening_type = evening_rotation[day_offset]

        morning_post = POST_GENERATORS[morning_type]()
        morning_post["scheduled_date"] = date.isoformat()
        morning_post["time_slot"] = "morning"

        evening_post = POST_GENERATORS[evening_type]()
        evening_post["scheduled_date"] = date.isoformat()
        evening_post["time_slot"] = "evening"

        calendar["days"].append({
            "date": date.isoformat(),
            "day": day_name,
            "posts": [morning_post, evening_post],
        })

    return calendar


# ---------------------------------------------------------------------------
# Console report
# ---------------------------------------------------------------------------

def print_calendar(calendar: dict) -> None:
    """Pretty-print the content calendar."""
    print("=" * 72)
    print(f"  WEEKLY CONTENT CALENDAR")
    print(f"  {calendar['week_start']} to {calendar['week_end']}")
    print("=" * 72)

    for day in calendar["days"]:
        print(f"\n--- {day['day']}, {day['date']} ---")
        for i, post in enumerate(day["posts"], 1):
            slot = post.get("time_slot", "").upper()
            print(f"\n  Post {i} ({slot}) | Type: {post['post_type']}")
            print(f"  Time: {post['best_time_to_post']}")
            # Show first 120 chars of caption
            preview = post["caption"][:120].replace("\n", " ") + "..."
            print(f"  Caption preview: {preview}")
            print(f"  Hashtags: {len(post['hashtags'])} tags")

    print(f"\n{'=' * 72}")
    print(f"Total posts planned: {sum(len(d['posts']) for d in calendar['days'])}")
    print(f"Calendar saved to {CALENDAR_FILE}")
    print("=" * 72)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    # Single post generation mode
    if "--type" in sys.argv:
        idx = sys.argv.index("--type")
        if idx + 1 < len(sys.argv):
            ptype = sys.argv[idx + 1]
            if ptype in POST_GENERATORS:
                post = POST_GENERATORS[ptype]()
                print(json.dumps(post, indent=2, ensure_ascii=False))
                return
            else:
                print(f"Unknown post type: {ptype}")
                print(f"Available: {', '.join(POST_GENERATORS.keys())}")
                sys.exit(1)

    # Default: generate weekly calendar
    calendar = generate_weekly_calendar()

    # Save to file
    with open(CALENDAR_FILE, "w", encoding="utf-8") as fh:
        json.dump(calendar, fh, indent=2, ensure_ascii=False)

    print_calendar(calendar)


if __name__ == "__main__":
    main()
