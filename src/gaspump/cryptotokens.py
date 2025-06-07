import aiohttp

from ..config import API_URL


async def get_crypto_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{API_URL}/tokens/list?sorting_field=created_at&limit=1"
        ) as response:
            return await response.json()


async def get_dev_suplai_crypto_data(token_address: str):
    base_url1 = f"{API_URL}/transactions/list?limit=100&offset=0&token_address="
    base_url2 = f"{API_URL}/holders/list?token_address="
    url1 = base_url1 + f"{token_address}"
    url2 = base_url2 + f"{token_address}&limit=1"
    transactions = None
    holders = None
    async with aiohttp.ClientSession() as session:
        async with session.get(url1) as response:
            transactions = await response.json()

    async with aiohttp.ClientSession() as session:
        async with session.get(url2) as response:
            holders = await response.json()

    if transactions[-1]["transaction_info"] == {}:
        ton_deployed = 0
        jettons = 0
    else:
        ton_deployed = (
            int(transactions[-1]["transaction_info"]["ton_amount"]) / 1000000000
        )
        jettons = (
            int(transactions[-1]["transaction_info"]["jetton_amount"]) / 1000000000
        )

    percent = (
        jettons
        / (
            (
                int(holders["holders"][0]["balance"])
                + float(holders["curve_info"]["balance"]) * 1000000000
            )
            / 1000000000
        )
    ) * 100

    return {"ton_deployed": ton_deployed, "jettons": jettons, "percent": percent}


async def get_created_tokens(creator_id):
    base_url = f"{API_URL}/tokens/user-list?telegram_id="
    url = base_url + f"{creator_id}&limit=100&offset=0"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            tokens = await response.json()

    dedust = 0
    for token in tokens:
        if token["is_full"]:
            dedust = dedust + 1

    return {"tokens": len(tokens), "dedust": dedust}
