def check_token(conn, token):
    return conn.hget('login:', token)