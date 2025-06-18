from requests import get


def get_address(postal_code: str) -> str:
    response = get(
        f"https://www.onemap.gov.sg/api/common/elastic/search?searchVal={postal_code}&returnGeom=N&getAddrDetails=Y"
    )

    if not response.ok:
        return ""

    data = response.json()
    results: list = data["results"]

    if not results:
        return ""

    return results[0]["ADDRESS"]
