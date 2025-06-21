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

    block = results[0]["BLK_NO"]
    road = results[0]["ROAD_NAME"]
    return f"{block} {road}"
