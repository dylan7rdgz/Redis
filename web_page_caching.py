# 95% of dynamically generated pages do not need to be changed
# and reloaded. So it is a good idea that we cache these 95% of pages
# The callback function is used to generate the web page
# python middle-ware/plugins usually have the form of the foll code:
def cache_request(conn, request, callback):
    if not can_cache(conn, request):
        return callback(request)
    page_key = 'cache:' + hash_request(request)
    content = conn.get(page_key)

    if not content:
        content = callback(request)
        conn.setex(page_key, content, 300)

    return content