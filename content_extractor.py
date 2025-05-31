import json
from openai import AzureOpenAI
from webpage import Webpage


def _get_system_prompt():
    return (
        "You are a helpful assistant that extracts links from webpages. "
        "Given a list of links, decide which link is relavant to include "
        "in a brochure about the apartment. The pages you select should"
        " be informative and relevant to potential residents, existing residents and applicants."
        " You should respond in JSON as in this example: "
        "{'links': {'type': 'amenities', 'url': 'https://example.com/amenities'},"
        "{'type': 'photo_gallery', 'url': 'https://example.com/gallery'}}"
    )


def _get_user_prompt(webpage: Webpage):
    user_prompt = f"Here is the list of links on the website of {webpage.url} - "
    user_prompt += "please decide which of these are relevant web links for a brochure about the apartment, respond with the full https URL in JSON format. \
Do not include Terms of Service, Privacy, email links.\n"
    user_prompt += "Links (some might be relative links):\n"
    user_prompt += "\n".join(webpage.links)
    return user_prompt


def _get_links(client: AzureOpenAI, model_name: str, system_prompt: str, user_prompt: str):
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    result = response.choices[0].message.content
    return json.loads(result)


def get_details(client: AzureOpenAI, model_name: str, url: str):
    result = "Landing page:\n"
    webpage = Webpage(url)
    print(webpage.body[:1000])  # Print first 1000 characters of the body for debugging

    system_prompt = _get_system_prompt()
    user_prompt = _get_user_prompt(webpage)

    result += url
    result += webpage.content
    links = _get_links(client, model_name, system_prompt, user_prompt)

    if "links" not in links:
        return "No relevant links found."

    print("Found links:", links)
    for link in links["links"]:
        result += f"\n\n{link["type"]}\n"
        result += f"{link["url"]}\n"
        result += Webpage(link["url"]).content
    return result
