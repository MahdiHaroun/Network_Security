import re
import socket
import ssl
import whois
import requests
import tldextract
import dns.resolver
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

# ==============================
# Helper Functions
# ==============================

def check_ip_address(url):
    """Check if URL contains an IP address instead of a domain name."""
    try:
        hostname = urlparse(url).netloc
        socket.inet_aton(hostname)
        return 1
    except socket.error:
        return -1

def url_length(url):
    return 1 if len(url) >= 75 else -1

def shortening_service(url):
    shortening_services = r"bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|bitly|buff\.ly|adf\.ly"
    return 1 if re.search(shortening_services, url) else -1

def having_at_symbol(url):
    return 1 if "@" in url else -1

def double_slash_redirecting(url):
    return 1 if url.count("//") > 1 else -1

def prefix_suffix(url):
    domain = urlparse(url).netloc
    return 1 if "-" in domain else -1

def having_sub_domain(url):
    domain_parts = urlparse(url).netloc.split('.')
    return 1 if len(domain_parts) > 3 else -1

def ssl_final_state(url):
    try:
        hostname = urlparse(url).netloc
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return -1 if cert else 1
    except:
        return 1

def domain_registration_length(domain):
    try:
        w = whois.whois(domain)
        expiration_date = w.expiration_date[0] if isinstance(w.expiration_date, list) else w.expiration_date
        if expiration_date and (expiration_date - datetime.now()).days >= 365:
            return -1
        else:
            return 1
    except:
        return 1

def favicon_check(url, soup):
    try:
        icon_link = soup.find("link", rel=lambda x: x and 'icon' in x.lower())
        if icon_link and urlparse(icon_link.get('href')).netloc != urlparse(url).netloc:
            return 1
        return -1
    except:
        return 1

def port_check(url):
    try:
        hostname = urlparse(url).netloc
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((hostname, 80))
        return -1 if result == 0 else 1
    except:
        return 1

def https_token(url):
    domain = urlparse(url).netloc
    return 1 if "https" in domain.lower() else -1

def request_url(soup, domain):
    total = len(soup.find_all('img'))
    external = sum(1 for img in soup.find_all('img') if domain not in (img.get('src') or ''))
    return 1 if total > 0 and (external / total) > 0.6 else -1

def url_of_anchor(soup, domain):
    anchors = soup.find_all('a', href=True)
    if not anchors:
        return -1
    external = sum(1 for a in anchors if domain not in a['href'])
    return 1 if (external / len(anchors)) > 0.67 else -1

def links_in_tags(soup, domain):
    tags = soup.find_all(['link', 'script'])
    if not tags:
        return -1
    external = sum(1 for t in tags if domain not in (t.get('href') or t.get('src') or ''))
    return 1 if (external / len(tags)) > 0.5 else -1

def sfh_check(soup, domain):
    forms = soup.find_all('form')
    for form in forms:
        action = form.get('action')
        if action and domain not in action:
            return 1
    return -1

def submitting_to_email(soup):
    forms = soup.find_all('form')
    for form in forms:
        if 'mailto:' in (form.get('action') or ''):
            return 1
    return -1

def abnormal_url(url, domain):
    return 1 if domain not in url else -1

def redirect_check(response):
    return 1 if len(response.history) > 2 else -1

def on_mouseover(soup):
    scripts = soup.find_all('script')
    for script in scripts:
        if 'onmouseover' in str(script).lower():
            return 1
    return -1

def right_click(soup):
    scripts = soup.find_all('script')
    for script in scripts:
        if 'event.button==2' in str(script).lower():
            return 1
    return -1

def popup_window(soup):
    scripts = soup.find_all('script')
    for script in scripts:
        if 'window.open' in str(script).lower():
            return 1
    return -1

def iframe_check(soup):
    return 1 if soup.find('iframe') else -1

def age_of_domain(domain):
    """Calculate how old the domain is in days."""
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
        if creation_date:
            return (datetime.now() - creation_date).days
        else:
            return 0
    except:
        return 0

def dns_record(domain):
    try:
        dns.resolver.resolve(domain, 'A')
        return -1
    except:
        return 1

# ==============================
# Main Feature Extraction
# ==============================
def extract_features(url):
    domain = urlparse(url).netloc
    features = {}

    # Request
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
    except:
        soup = BeautifulSoup("", 'html.parser')
        response = None

    # URL-based
    features['having_IP_Address'] = check_ip_address(url)
    features['URL_Length'] = url_length(url)
    features['Shortining_Service'] = shortening_service(url)
    features['having_At_Symbol'] = having_at_symbol(url)
    features['double_slash_redirecting'] = double_slash_redirecting(url)
    features['Prefix_Suffix'] = prefix_suffix(url)
    features['having_Sub_Domain'] = having_sub_domain(url)

    # SSL/Domain
    features['SSLfinal_State'] = ssl_final_state(url)
    features['Domain_registeration_length'] = domain_registration_length(domain)
    features['Favicon'] = favicon_check(url, soup)
    features['port'] = port_check(url)
    features['HTTPS_token'] = https_token(url)

    # Webpage Content
    features['Request_URL'] = request_url(soup, domain)
    features['URL_of_Anchor'] = url_of_anchor(soup, domain)
    features['Links_in_tags'] = links_in_tags(soup, domain)
    features['SFH'] = sfh_check(soup, domain)
    features['Submitting_to_email'] = submitting_to_email(soup)
    features['Abnormal_URL'] = abnormal_url(url, domain)
    features['Redirect'] = redirect_check(response) if response else -1
    features['on_mouseover'] = on_mouseover(soup)
    features['RightClick'] = right_click(soup)
    features['popUpWidnow'] = popup_window(soup)
    features['Iframe'] = iframe_check(soup)

    # Age of Domain (new feature added)
    features['age_of_domain'] = age_of_domain(domain)

    # DNS Record (placed after age_of_domain)
    features['DNSRecord'] = dns_record(domain)

    # Placeholder for unavailable online APIs
    features['web_traffic'] = 0
    features['Page_Rank'] = 0
    features['Google_Index'] = 0
    features['Links_pointing_to_page'] = 0
    features['Statistical_report'] = 0

    return features

# ==============================
# Test Example
# ==============================
url = "https://kleki.com/#966"
data = extract_features(url)

# Ensure correct column order
final_columns = [
    "having_IP_Address","URL_Length","Shortining_Service","having_At_Symbol","double_slash_redirecting",
    "Prefix_Suffix","having_Sub_Domain","SSLfinal_State","Domain_registeration_length","Favicon",
    "port","HTTPS_token","Request_URL","URL_of_Anchor","Links_in_tags","SFH","Submitting_to_email",
    "Abnormal_URL","Redirect","on_mouseover","RightClick","popUpWidnow","Iframe",
    "age_of_domain","DNSRecord","web_traffic","Page_Rank","Google_Index",
    "Links_pointing_to_page","Statistical_report"
]

df = pd.DataFrame([data], columns=final_columns)
df.to_csv("output.csv", index=False)
print("Features extracted and saved to output.csv")
