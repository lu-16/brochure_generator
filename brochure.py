from content_extractor import get_details
from llm import LLM


def _get_system_prompt():
    return (
        "You are a helpful assistant that creates a brochure for an apartment. "
        "Given the extracted website content, generate a well-structured, markdown-formatted brochure. "
        "Organize the content into sections: Welcome, Floorplans, Amenities, Neighborhood, Gallery, and Contact. "
        "Do not truncate or duplicate text. Use only the information provided. "
        "Do not invent or add information. Each section should be concise and relevant."
        "Keep relevant full url links in the content, but do not include any links to Terms of Service, Privacy Policy, or email links."
        "Do not include any images or photos in the markdown output. Do not use markdown image syntax or embed any images."
    )


def _get_user_prompt(details):
    return (
        "Here is the extracted content for the apartment website:\n\n"
        f"{details}\n\n"
        "Please generate the property brochure as described."
    )


def generate_brochure(url: str) -> str:
    llm = LLM()
    client, model_name = llm.client, llm.model
    system_prompt = _get_system_prompt()
    details = get_details(client, model_name, url)
    user_prompt = _get_user_prompt(details)
    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
