import traceback

print('Running tools runtime checks...')

# Test save_to_txt
try:
    from tools import save_to_txt
    r = save_to_txt('test data from tools_test', filename='tools_test_output.txt')
    print('save_to_txt OK ->', r)
except Exception as e:
    print('save_to_txt ERROR')
    traceback.print_exc()

# Test imports from langchain_community
try:
    from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
    from langchain_community.utilities import WikipediaAPIWrapper
    print('Imported langchain_community classes OK')
except Exception as e:
    print('langchain_community import ERROR')
    traceback.print_exc()
    DuckDuckGoSearchRun = None
    WikipediaQueryRun = None
    WikipediaAPIWrapper = None

# Test DuckDuckGoSearchRun
if DuckDuckGoSearchRun:
    try:
        search = DuckDuckGoSearchRun()
        res = search.run('meaning of life')
        print('DuckDuckGoSearchRun.run result type:', type(res))
        if isinstance(res, (list, tuple)):
            print('First item keys/repr:', repr(res[0])[:200])
        else:
            print('Result repr:', repr(res)[:200])
    except Exception as e:
        print('DuckDuckGoSearchRun.run ERROR')
        traceback.print_exc()

# Test WikipediaQueryRun
if WikipediaQueryRun and WikipediaAPIWrapper:
    try:
        api = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=200)
        wiki = WikipediaQueryRun(api_wrapper=api)
        wres = wiki.run('meaning of life')
        print('WikipediaQueryRun.run result type:', type(wres))
        print('WikipediaQueryRun.run repr:', repr(wres)[:400])
    except Exception as e:
        print('WikipediaQueryRun.run ERROR')
        traceback.print_exc()

print('tools_test finished')
