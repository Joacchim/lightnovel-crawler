# -*- coding: utf-8 -*-
"""
To search for novels in selected sources
"""
import logging
import os
from concurrent import futures

from progress.bar import IncrementalBar
from slugify import slugify

from ..sources import crawler_list

logger = logging.getLogger(__name__)


def get_search_result(user_input, link, app):
    try:
        crawler = crawler_list[link]
        instance = crawler()
        instance.home_url = link.strip('/')
        results = instance.search_novel(user_input)
        logger.debug(results)
        logger.info('%d results from %s', len(results), link)
        return results
    except Exception:
        import traceback
        logger.debug(traceback.format_exc())
    finally:
        app.progress += 1
    # end try
    return []
# end def


def process_results(results):
    combined = dict()
    for result in results:
        key = slugify(result['title'])
        if len(key) <= 1:
            continue
        elif key not in combined:
            combined[key] = []
        # end if
        combined[key].append(result)
    # end for

    processed = []
    for key, value in combined.items():
        value.sort(key=lambda x: x['url'])
        processed.append({
            'id': key,
            'title': value[0]['title'],
            'novels': value
        })
    # end for

    processed.sort(key=lambda x: -len(x['novels']))

    return processed[:15]  # Control the number of results
# end def


def search_novels(app):
    executor = futures.ThreadPoolExecutor(10)

    # Add future tasks
    checked = {}
    futures_to_check = []
    app.progress = 0
    for link in app.crawler_links:
        crawler = crawler_list[link]
        if crawler in checked:
            logger.info('A crawler for "%s" already exists', link)
            continue
        # end if
        checked[crawler] = True
        future = executor.submit(
            get_search_result,
            app.user_input,
            link,
            app
        )
        futures_to_check.append(future)
    # end for

    bar = IncrementalBar('Searching', max=len(futures_to_check))
    bar.start()

    if os.getenv('debug_mode') == 'yes':
        bar.next = lambda: None  # Hide in debug mode
    # end if

    # Resolve future tasks
    combined_results = []
    for future in futures_to_check:
        combined_results += future.result()
        bar.next()
    # end for

    # Process combined search results
    app.search_results = process_results(combined_results)
    bar.clearln()
    bar.finish()
    print('Found %d results' % len(app.search_results))

    executor.shutdown()
# end def
