import asyncio
import aiohttp
import re


MODELS_PATTERN = r'/library/[^/"]+'
MODEL_VERSIONS_PATTERN = r'/library/[^:/\s]+:[^"/\s]+'

all_models_url = "https://ollama.com/search"
specific_model_url = "https://ollama.com/library/"


async def get_models(session: aiohttp.ClientSession) -> list:
    """Get names of all models listed at https://ollama.com/search"""
    async with session.get(all_models_url) as r:
        matching_names = re.findall(MODELS_PATTERN, await r.text())
        result = [name.replace("/library/", "") for name in matching_names]
        return result


async def get_model_versions(session: aiohttp.ClientSession, model: str) -> tuple:
    """Get all available version of a specific model at https://ollama.com/library/<model_name>"""
    async with session.get(specific_model_url + model) as r:
        versions = re.findall(MODEL_VERSIONS_PATTERN, await r.text(encoding="latin-1"))
        res = tuple(version.replace("/library/", "") for version in versions)
        return model, res


async def main():
    async with aiohttp.ClientSession() as session:
        models = await get_models(session)
        tasks = [
            asyncio.create_task(get_model_versions(session, name)) for name in models
        ]
        for res in await asyncio.gather(*tasks):
            print(f"{res[0].capitalize()} - {res[1]}")


if __name__ == "__main__":
    asyncio.run(main())
