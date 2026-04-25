from django.shortcuts import render

FEATURED_ARTICLE = {
    "title": "Best Pricing Strategies for Pilates Studios in 2026",
    "date": "Apr 22, 2026",
    "category": "Featured story",
    "image": (
        "https://images.pexels.com/photos/6311389/pexels-photo-6311389.jpeg"
        "?auto=compress&cs=tinysrgb&w=1400"
    ),
    "excerpt": (
        "A practical editorial look at pricing models, positioning, and packaging for "
        "boutique fitness businesses that want premium margins."
    ),
}

ARTICLES = [
    {
        "title": "6 Principles of Pilates (Complete Guide for 2026)",
        "date": "Apr 17, 2026",
        "image": (
            "https://images.pexels.com/photos/6303444/pexels-photo-6303444.jpeg"
            "?auto=compress&cs=tinysrgb&w=900"
        ),
    },
    {
        "title": "How Much Does It Cost to Open a CrossFit Gym in 2026",
        "date": "Apr 15, 2026",
        "image": (
            "https://images.pexels.com/photos/7901500/pexels-photo-7901500.jpeg"
            "?auto=compress&cs=tinysrgb&w=900"
        ),
    },
    {
        "title": "Top 10 Pilates Studio Design Ideas for 2026",
        "date": "Apr 14, 2026",
        "image": (
            "https://images.pexels.com/photos/6303449/pexels-photo-6303449.jpeg"
            "?auto=compress&cs=tinysrgb&w=900"
        ),
    },
    {
        "title": "Best Mindbody Alternatives in 2026",
        "date": "Apr 10, 2026",
        "image": (
            "https://images.pexels.com/photos/7900679/pexels-photo-7900679.jpeg"
            "?auto=compress&cs=tinysrgb&w=900"
        ),
    },
    {
        "title": "300+ Pole Dance Studio Name Ideas to Inspire Your New Studio",
        "date": "Apr 9, 2026",
        "image": (
            "https://images.pexels.com/photos/6311479/pexels-photo-6311479.jpeg"
            "?auto=compress&cs=tinysrgb&w=900"
        ),
    },
    {
        "title": "How to Get Your First 50 Clients as a Pilates Studio in 2026",
        "date": "Feb 28, 2026",
        "image": (
            "https://images.pexels.com/photos/6303489/pexels-photo-6303489.jpeg"
            "?auto=compress&cs=tinysrgb&w=900"
        ),
    },
]


def home(request):
    context = {
        "featured_article": FEATURED_ARTICLE,
        "articles": ARTICLES,
    }
    return render(request, "blog/home.html", context)
