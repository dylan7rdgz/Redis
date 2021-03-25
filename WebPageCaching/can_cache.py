def can_cache(conn, request):
    item_id = extract_item_id(request)
    if not item_id or id_dynamic(request):
        return False
    rank = conn.zrank('viewed:', item_id)
    return rank is not None and rank < 10000