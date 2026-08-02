AUTHOR = 'Alejandro Ucan-Puc'
SITENAME = 'Alejandro Ucan-Puc'
SITETITLE = 'Alejandro Ucan-Puc'
SITESUBTITLE = 'Research | Teaching | Outreach'
SITEURL = ""
THEME = "themes/cebong"
SITETAGLINE = "Research | Teaching | Outreach"
SITE_DOMAINS = [
    "Mathematics",
    "Data Science",
    "Topology",
    "Artificial Intelligence",
]
FOOTERTEXT = ""
CSS_FILE = "main.css"
SITE_DESCRIPTION = (
    "Personal academic website of Alejandro Ucan-Puc featuring research, "
    "teaching, seminar activities, and outreach in mathematics and data science."
)
SEO_DEFAULT_IMAGE = "/images/site/avatar-520.jpg"
SEO_ORG_NAME = "Tecnologico de Monterrey"
SEO_ORG_URL = "https://tec.mx"
SEO_PERSON_EMAIL = "alejandro.ucan-puc@tec.mx"
SEO_PERSON_DISCORD = "alejandroucanpuc"

PATH = "content"
STATIC_PATHS = ["images", "extra"]
EXTRA_PATH_METADATA = {
    "extra/favicon.ico": {"path": "favicon.ico"},
    "extra/favicon-16x16.png": {"path": "favicon-16x16.png"},
    "extra/favicon-32x32.png": {"path": "favicon-32x32.png"},
    "extra/apple-touch-icon.png": {"path": "apple-touch-icon.png"},
}

TIMEZONE = 'America/Monterrey'

DEFAULT_LANG = 'en'
MAIN_MENU = True

DISPLAY_PAGES_ON_MENU = False
MENUITEMS = [
    ("About me", "/"),
    ("Research", "/pages/research/"),
    ("Repositories", "/pages/repositories/"),
    ("Courses", "/pages/courses/"),
    ("Seminar", "/pages/seminar/"),
    ("Blog", "/pages/social/"),
    ("Contact", "/pages/contact/"),
    ("Español", "/es/"),
]

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
FEED_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Sidebar links
LINKS = [
    ("Research", "/pages/research/"),
    ("Repositories", "/pages/repositories/"),
    ("Courses", "/pages/courses/"),
    ("Seminar", "/pages/seminar/"),
    ("Blog", "/pages/social/"),
    ("Contact", "/pages/contact/"),
]
LINKS_IN_NEW_TAB = "external"

# Social widget
SOCIAL = [
    ("ORCID", "https://orcid.org/0000-0002-0037-9394"),
    ("Instagram", "https://instagram.com/i.rracionalx"),
]

DEFAULT_PAGINATION = 10
GOOGLE_ANALYTICS = "G-5HZK1LYQBX"

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
