import duckduckpy


def run_query(search_terms):

    # Issue the request, given the details above.
    response = duckduckpy.query(search_terms, container='dict')
    search_results = response

    # With the response now in play, build up a Python list.
    # results = []
    # print(search_results)
    # for result in search_results:
    #     results.append({
    #         'result': search_results.related_topics[result].result,
    #         'link': result['first_url'],
    #         'text': result['text']})
    return search_results


def main():
    print("Duck duck search")
    query_str = input("Enter a query to search for: ")
    results = run_query(query_str)
    print(type(results))
    print(len(results))
    for i, x in enumerate(results):

        print(results['related_topics'][i])
        # print(results.related_topics[x])

    print(results)


if __name__ == '__main__':
    main()
