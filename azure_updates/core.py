import logging
from dataclasses import dataclass

import httpx
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


@dataclass
class AzureUpdate:
    id: str
    product_categories: list[str]
    tags: list[str]
    products: list[str]
    general_availability_date: str | None
    preview_availability_date: str | None
    private_preview_availability_date: str | None
    title: str
    description: str
    links: list[str]
    status: str
    created: str
    modified: str
    availabilities: list[str]


def call_azure_updates_api(top: int = 10) -> dict:
    with httpx.Client() as client:
        response = client.get(
            url=f"https://www.microsoft.com/releasecommunications/api/v2/azure?$count=true&includeFacets=true&top={top}&skip=0&orderby=modified%20desc"
        )
        response.raise_for_status()
        return response.json()


def parse_azure_updates(response_json: dict) -> list[AzureUpdate]:
    azure_updates = []
    for update in response_json["value"]:
        soup = BeautifulSoup(update["description"].replace("\n", ""), "html.parser")
        # Extract all links from the description
        links = []
        for link in soup.find_all("a", href=True):
            links.append(link["href"])

        # Add the parsed AzureUpdate object to the list
        azure_updates.append(
            AzureUpdate(
                id=update["id"],
                product_categories=update["productCategories"],
                tags=update["tags"],
                products=update["products"],
                general_availability_date=update["generalAvailabilityDate"],
                preview_availability_date=update["previewAvailabilityDate"],
                private_preview_availability_date=update["privatePreviewAvailabilityDate"],
                title=update["title"],
                description=soup.get_text().strip(),
                links=links,
                status=update["status"],
                created=update["created"],
                modified=update["modified"],
                availabilities=update["availabilities"],
            )
        )
    return azure_updates


def write_azure_updates_to_file(updates: list[AzureUpdate], filename: str):
    with open(filename, "w") as file:
        file.write(
            "---\n"
            "theme: seriph\n"
            "background: https://cover.sli.dev\n"
            "title: Azure Updates\n"
            "info: |\n"
            "  ## Azure Updates\n"
            "  Presentation slides for Azure Updates\n"
            "  Learn more at [Azure Updates](https://azure.microsoft.com/en-us/updates/)\n"
            "class: text-center\n"
            "drawings:\n"
            "  persist: false\n"
            "mdc: true\n"
            "---\n\n"
            "# Azure Updates\n\n"
        )
        for update in updates:
            file.write(f"{'-' * 3}\n\n")
            file.write(f"# Title: {update.title}\n")
            file.write(f"- Product Categories: {', '.join(update.product_categories)}\n")
            file.write(f"- Created: {update.created}\n")
            file.write(f"- Description: {update.description}\n\n")
            file.write(f"- Links: {', '.join(update.links)}\n")
            # Comment
            # id: str
            # product_categories: list[str]
            # tags: list[str]
            # products: list[str]
            # general_availability_date: str | None
            # preview_availability_date: str | None
            # private_preview_availability_date: str | None
            # title: str
            # description: str
            # links: list[str]
            # status: str
            # created: str
            # modified: str
            # availabilities: list[str]
            file.write(
                "<!--"
                f"ID: {update.id}\n\n"
                f"Product Categories: {update.product_categories}\n\n"
                f"Tags: {update.tags}\n\n"
                f"Products: {update.products}\n\n"
                f"General Availability Date: {update.general_availability_date}\n\n"
                f"Preview Availability Date: {update.preview_availability_date}\n\n"
                f"Private Preview Availability Date: {update.private_preview_availability_date}\n\n"
                f"Title: {update.title}\n\n"
                f"Description: {update.description}\n\n"
                f"Links: {update.links}\n\n"
                f"Status: {update.status}\n\n"
                f"Created: {update.created}\n\n"
                f"Modified: {update.modified}\n\n"
                f"Availabilities: {update.availabilities}\n\n"
                "-->\n\n"
            )


if __name__ == "__main__":
    response_json = call_azure_updates_api(top=100)
    azure_updates = parse_azure_updates(response_json)
    write_azure_updates_to_file(azure_updates, "docs/slides.md")
