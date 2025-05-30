import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

load_dotenv(override=True)
api_key = os.getenv("AZURE_OPENAI_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")


class Webpage:
    def __init__(self, url):
        self.url = url
        self.extract_text_from_url(url)

    def extract_text_from_url(self, url):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")  # Run in headless mode
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            driver.get(url)
            self.body = driver.page_source
            driver.quit()
            soup = BeautifulSoup(self.body, "html.parser")
            self.title = soup.title.string if soup.title else ""
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            self.content = soup.body.get_text(separator="\n", strip=True) if soup.body else ""
            self.links = [a["href"] for a in soup.find_all("a", href=True)]
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")

    def __repr__(self):
        return f"Webpage(url={self.url}, title={self.title})"

    def __str__(self):
        return f"Webpage: {self.title} ({self.url})\nContent: {self.content[:100]}...\nLinks: {len(self.links)} found"


def get_system_prompt():
    return (
        "You are a helpful assistant that extracts links from webpages. "
        "Given a list of links, decide which link is relavant to include "
        "in a brochure about the apartment complex. The pages you select should"
        " be informative and relevant to potential residents, existing residents and applicants."
        " You should respond in JSON as in this example: "
        "{'links': {'type': 'amenities', 'url': 'https://example.com/amenities'},"
        "{'type': 'photo_gallary', 'url': 'https://example.com/gallery'}}"
    )


def get_user_prompt(webpage):
    user_prompt = f"Here is the list of links on the website of {webpage.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the apartment complex, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(webpage.links)
    return user_prompt


def get_links(client, system_prompt, user_prompt):
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    return json.loads(result)


def get_details(client, url):
    result = "Landing page:\n"
    webpage = Webpage(url)
    print(webpage.body[:1000])  # Print first 1000 characters of the body for debugging

    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt(webpage)

    result += url
    result += webpage.content
    links = get_links(client, system_prompt, user_prompt)

    if "links" not in links:
        return "No relevant links found."

    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link['type']}\n"
        result += f"{link['url']}\n"
        result += Webpage(link["url"]).content
    return result


def generate_brochure_with_llm(url):
    client = AzureOpenAI(api_key=api_key, api_version="2023-05-15", azure_endpoint=endpoint)
    system_prompt = (
        "You are a helpful assistant that creates a brochure for an apartment complex. "
        "Given the extracted website content, generate a well-structured, markdown-formatted brochure. "
        "Organize the content into sections: Welcome, Floorplans, Amenities, Neighborhood, Gallery, and Contact. "
        "Do not truncate or duplicate text. Use only the information provided. "
        "Do not invent or add information. Each section should be concise and relevant."
        "Keep relevant full url links in the content, but do not include any links to Terms of Service, Privacy Policy, or email links."
    )
    details = get_details(client, url)
    user_prompt = (
        "Here is the extracted content for the apartment complex website:\n\n"
        f"{details}\n\n"
        "Please generate the property brochure as described."
    )
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content

def stream_brochure(url):
    client = AzureOpenAI(api_key=api_key, api_version="2023-05-15", azure_endpoint=endpoint)
    system_prompt = (
        "You are a helpful assistant that creates a brochure for an apartment complex. "
        "Given the extracted website content, generate a well-structured, markdown-formatted brochure. "
        "Organize the content into sections: Welcome, Floorplans, Amenities, Neighborhood, Gallery, and Contact. "
        "Do not truncate or duplicate text. Use only the information provided. "
        "Do not invent or add information. Each section should be concise and relevant."
        "Keep relevant full url links in the content, but do not include any links to Terms of Service, Privacy Policy, or email links."
    )
    details = get_details(client, url)
    user_prompt = (
        "Here is the extracted content for the apartment complex website:\n\n"
        f"{details}\n\n"
        "Please generate the property brochure as described."
    )
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        stream=True,
    )
    for chunk in response:
        if "choices" in chunk and len(chunk["choices"]) > 0:
            content = chunk["choices"][0].get("delta", {}).get("content", "")
            if content:
                yield content
        else:
            yield ""  # In case of no content, yield empty string
