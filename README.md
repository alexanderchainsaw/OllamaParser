# OllamaParser
A very simple script to parse main page of Ollama (https://ollama.com/search) for the names of most popular models,
and then get available versions of each model
```python
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
```

### Usage

Run the file
```bash
uv run ollama_parser.py
```
And you should see something like this:
```bash
Deepseek-r1 - ('deepseek-r1:1.5b', 'deepseek-r1:7b', 'deepseek-r1:8b', 'deepseek-r1:14b', 'deepseek-r1:32b', 'deepseek-r1:70b', 'deepseek-r1:671b')
Llama3.3 - ('llama3.3:70b',)
Phi4 - ('phi4:14b',)
Llama3.2 - ('llama3.2:1b', 'llama3.2:3b')
Llama3.1 - ('llama3.1:8b', 'llama3.1:70b', 'llama3.1:405b')
Nomic-embed-text - ('nomic-embed-text:latest',)
Mistral - ('mistral:7b',)
Llama3 - ('llama3:8b', 'llama3:70b')
Qwen2.5 - ('qwen2.5:0.5b', 'qwen2.5:1.5b', 'qwen2.5:3b', 'qwen2.5:7b', 'qwen2.5:14b', 'qwen2.5:32b', 'qwen2.5:72b')
Qwen - ('qwen:0.5b', 'qwen:1.8b', 'qwen:4b', 'qwen:7b', 'qwen:14b', 'qwen:32b', 'qwen:72b', 'qwen:110b')
Gemma - ('gemma:2b', 'gemma:7b')
Qwen2 - ('qwen2:0.5b', 'qwen2:1.5b', 'qwen2:7b', 'qwen2:72b')
Llava - ('llava:7b', 'llava:13b', 'llava:34b')
Llama2 - ('llama2:7b', 'llama2:13b', 'llama2:70b')
Qwen2.5-coder - ('qwen2.5-coder:0.5b', 'qwen2.5-coder:1.5b', 'qwen2.5-coder:3b', 'qwen2.5-coder:7b', 'qwen2.5-coder:14b', 'qwen2.5-coder:32b')
Phi3 - ('phi3:3.8b', 'phi3:14b', 'phi3:mini', 'phi3:medium', 'phi3:latest', 'phi3:mini)', 'phi3:medium)', 'phi3:latest')
Gemma2 - ('gemma2:2b', 'gemma2:9b', 'gemma2:27b')
Codellama - ('codellama:7b', 'codellama:13b', 'codellama:34b', 'codellama:70b', 'codellama:7b', 'codellama:13b', 'codellama:34b', 'codellama:70b', 'codellama:7b)', 'codellama:13b)', 'codellama:34b)', 'codellama:70b)')
Mxbai-embed-large - ('mxbai-embed-large:335m',)
Tinyllama - ('tinyllama:1.1b',)
Llama3.2-vision - ('llama3.2-vision:11b', 'llama3.2-vision:90b')
Mistral-nemo - ('mistral-nemo:12b',)
Starcoder2 - ('starcoder2:3b', 'starcoder2:7b', 'starcoder2:15b')
Snowflake-arctic-embed - ('snowflake-arctic-embed:22m', 'snowflake-arctic-embed:33m', 'snowflake-arctic-embed:110m', 'snowflake-arctic-embed:137m', 'snowflake-arctic-embed:335m')
Deepseek-coder-v2 - ('deepseek-coder-v2:16b', 'deepseek-coder-v2:236b')
Deepseek-v3 - ('deepseek-v3:671b',)
Llama2-uncensored - ('llama2-uncensored:7b', 'llama2-uncensored:70b')
Deepseek-coder - ('deepseek-coder:1.3b', 'deepseek-coder:6.7b', 'deepseek-coder:33b')
Mixtral - ('mixtral:8x7b', 'mixtral:8x22b')
Dolphin-mixtral - ('dolphin-mixtral:8x7b', 'dolphin-mixtral:8x22b')
Openthinker - ('openthinker:7b', 'openthinker:32b')
Codegemma - ('codegemma:2b', 'codegemma:7b')
Phi - ('phi:2.7b',)
Bge-m3 - ('bge-m3:567m',)
Wizardlm2 - ('wizardlm2:7b', 'wizardlm2:8x22b')
Llava-llama3 - ('llava-llama3:8b',)
Minicpm-v - ('minicpm-v:8b',)
Dolphin-mistral - ('dolphin-mistral:7b',)
All-minilm - ('all-minilm:22m', 'all-minilm:33m')
Dolphin-llama3 - ('dolphin-llama3:8b', 'dolphin-llama3:70b')
Command-r - ('command-r:35b',)
Orca-mini - ('orca-mini:3b', 'orca-mini:7b', 'orca-mini:13b', 'orca-mini:70b')
Yi - ('yi:6b', 'yi:9b', 'yi:34b')
Smollm2 - ('smollm2:135m', 'smollm2:360m', 'smollm2:1.7b')
Hermes3 - ('hermes3:3b', 'hermes3:8b', 'hermes3:70b', 'hermes3:405b')
Phi3.5 - ('phi3.5:3.8b',)
Zephyr - ('zephyr:7b', 'zephyr:141b', 'mixtral:8x22b', 'mixtral:8x22b).')
Codestral - ('codestral:22b',)
Dolphin3 - ('dolphin3:8b',)
Mistral-small - ('mistral-small:22b', 'mistral-small:24b')
Granite-code - ('granite-code:3b', 'granite-code:8b', 'granite-code:20b', 'granite-code:34b')
Starcoder - ('starcoder:1b', 'starcoder:3b', 'starcoder:7b', 'starcoder:15b')
Wizard-vicuna-uncensored - ('wizard-vicuna-uncensored:7b', 'wizard-vicuna-uncensored:13b', 'wizard-vicuna-uncensored:30b')
Smollm - ('smollm:135m', 'smollm:360m', 'smollm:1.7b')
Vicuna - ('vicuna:7b', 'vicuna:13b', 'vicuna:33b')
Mistral-openorca - ('mistral-openorca:7b',)
Olmo2 - ('olmo2:7b', 'olmo2:13b')
Qwq - ('qwq:32b',)
Llama2-chinese - ('llama2-chinese:7b', 'llama2-chinese:13b')
Openchat - ('openchat:7b',)
Codegeex4 - ('codegeex4:9b',)
Aya - ('aya:8b', 'aya:35b')
Codeqwen - ('codeqwen:7b',)
Deepseek-llm - ('deepseek-llm:7b', 'deepseek-llm:67b')
Mistral-large - ('mistral-large:123b',)
Nous-hermes2 - ('nous-hermes2:10.7b', 'nous-hermes2:34b')
Deepseek-v2 - ('deepseek-v2:16b', 'deepseek-v2:236b')
Glm4 - ('glm4:9b',)
Stable-code - ('stable-code:3b',)
Openhermes - ('openhermes:latest',)
Command-r-plus - ('command-r-plus:104b',)
Qwen2-math - ('qwen2-math:1.5b', 'qwen2-math:7b', 'qwen2-math:72b')
Tinydolphin - ('tinydolphin:1.1b',)
Wizardcoder - ('wizardcoder:33b',)
Moondream - ('moondream:1.8b',)
Bakllava - ('bakllava:7b',)
Stablelm2 - ('stablelm2:1.6b', 'stablelm2:12b')
Neural-chat - ('neural-chat:7b',)
Reflection - ('reflection:70b',)
Wizard-math - ('wizard-math:7b', 'wizard-math:13b', 'wizard-math:70b')
Llama3-gradient - ('llama3-gradient:1048k', 'llama3-gradient:8b', 'llama3-gradient:70b')
Llama3-chatqa - ('llama3-chatqa:8b', 'llama3-chatqa:70b')
Sqlcoder - ('sqlcoder:7b', 'sqlcoder:15b')
Xwinlm - ('xwinlm:7b', 'xwinlm:13b')
Dolphincoder - ('dolphincoder:7b', 'dolphincoder:15b')
Bge-large - ('bge-large:335m',)
Nous-hermes - ('nous-hermes:7b', 'nous-hermes:13b')
Phind-codellama - ('phind-codellama:34b',)
Yarn-llama2 - ('yarn-llama2:7b', 'yarn-llama2:13b')
Llava-phi3 - ('llava-phi3:3.8b',)
Solar - ('solar:10.7b',)
Starling-lm - ('starling-lm:7b',)
Wizardlm - ('wizardlm:13b-fp16', 'wizardlm:13b-fp16', 'wizardlm:13b-fp16', 'wizardlm:13b-fp16', 'wizardlm:13b-fp16', 'wizardlm:13b-fp16')
Athene-v2 - ('athene-v2:72b',)
Granite3.1-dense - ('granite3.1-dense:2b', 'granite3.1-dense:8b')
Yi-coder - ('yi-coder:1.5b', 'yi-coder:9b')
Internlm2 - ('internlm2:1m', 'internlm2:1.8b', 'internlm2:7b', 'internlm2:20b')
Samantha-mistral - ('samantha-mistral:7b',)
Falcon - ('falcon:7b', 'falcon:40b', 'falcon:180b', 'falcon:7b', 'falcon:40b', 'falcon:180b', 'falcon:180b', 'falcon:7b)', 'falcon:40b)', 'falcon:180b)', 'falcon:180b)')
Nemotron-mini - ('nemotron-mini:4b',)
Nemotron - ('nemotron:70b',)
Dolphin-phi - ('dolphin-phi:2.7b',)
Orca2 - ('orca2:7b', 'orca2:13b')
Wizardlm-uncensored - ('wizardlm-uncensored:13b',)
Stable-beluga - ('stable-beluga:7b', 'stable-beluga:13b', 'stable-beluga:70b')
Deepscaler - ('deepscaler:1.5b',)
Granite3-dense - ('granite3-dense:2b', 'granite3-dense:8b')
Llama3-groq-tool-use - ('llama3-groq-tool-use:8b', 'llama3-groq-tool-use:70b')
Medllama2 - ('medllama2:7b',)
Meditron - ('meditron:7b', 'meditron:70b')
Llama-pro - ('llama-pro:latest',)
Yarn-mistral - ('yarn-mistral:7b',)
Smallthinker - ('smallthinker:3b',)
Aya-expanse - ('aya-expanse:8b', 'aya-expanse:32b')
Deepseek-v2.5 - ('deepseek-v2.5:236b',)
Granite3-moe - ('granite3-moe:1b', 'granite3-moe:3b')
Nexusraven - ('nexusraven:13b',)
Codeup - ('codeup:13b',)
Paraphrase-multilingual - ('paraphrase-multilingual:278m',)
Falcon3 - ('falcon3:1b', 'falcon3:3b', 'falcon3:7b', 'falcon3:10b')
Nous-hermes2-mixtral - ('nous-hermes2-mixtral:8x7b',)
Everythinglm - ('everythinglm:13b',)
Shieldgemma - ('shieldgemma:2b', 'shieldgemma:9b', 'shieldgemma:27b')
Granite3.1-moe - ('granite3.1-moe:1b', 'granite3.1-moe:3b')
Falcon2 - ('falcon2:11b',)
Magicoder - ('magicoder:7b',)
Mathstral - ('mathstral:7b',)
Stablelm-zephyr - ('stablelm-zephyr:3b',)
Marco-o1 - ('marco-o1:7b',)
Codebooga - ('codebooga:34b',)
Snowflake-arctic-embed2 - ('snowflake-arctic-embed2:568m',)
Reader-lm - ('reader-lm:0.5b', 'reader-lm:1.5b')
Solar-pro - ('solar-pro:22b',)
Duckdb-nsql - ('duckdb-nsql:7b',)
Mistrallite - ('mistrallite:7b',)
Wizard-vicuna - ('wizard-vicuna:13b',)
Llama-guard3 - ('llama-guard3:1b', 'llama-guard3:8b')
Megadolphin - ('megadolphin:120b',)
Nuextract - ('nuextract:3.8b',)
Exaone3.5 - ('exaone3.5:2.4b', 'exaone3.5:7.8b', 'exaone3.5:32b')
Opencoder - ('opencoder:1.5b', 'opencoder:8b')
Notux - ('notux:8x7b',)
Open-orca-platypus2 - ('open-orca-platypus2:13b',)
Notus - ('notus:7b',)
Goliath - ('goliath:latest',)
Bespoke-minicheck - ('bespoke-minicheck:7b',)
Command-r7b - ('command-r7b:7b',)
Firefunction-v2 - ('firefunction-v2:70b',)
Dbrx - ('dbrx:132b',)
Tulu3 - ('tulu3:8b', 'tulu3:70b')
Granite-embedding - ('granite-embedding:30m', 'granite-embedding:278m')
Granite3-guardian - ('granite3-guardian:2b', 'granite3-guardian:8b')
Alfred - ('alfred:40b',)
Sailor2 - ('sailor2:1b', 'sailor2:8b', 'sailor2:20b')
R1-1776 - ('r1-1776:70b', 'r1-1776:671b')

```