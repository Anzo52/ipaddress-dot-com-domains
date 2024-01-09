import sqlite3


def con_cursor():
    conn = sqlite3.connect("domains.db")
    cursor = conn.cursor()
    return conn, cursor


def create_table(tablename):
    conn, cursor = con_cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tablename} (domain TEXT)")
    conn.commit()
    conn.close()
    return True


def insert_domain(domain):
    conn, cursor = con_cursor()
    cursor.execute("INSERT INTO domains VALUES (?)", (domain,))
    conn.commit()
    conn.close()
    return True


def insert_domain_where(table_to_search, table_to_insert, search_term):
    conn, cursor = con_cursor()
    cursor.execute(
        f"INSERT INTO {table_to_insert} SELECT domain FROM {table_to_search} WHERE domain LIKE '{search_term}' ORDER BY domain ASC"
    )
    conn.commit()
    conn.close()
    return True


def make_table_a_z(letter):
    # make a table called domains_a, domains_b, etc.
    # return True when done
    create_table(f"domains_{letter}")
    return True


def make_table_nums():
    # make a table called domains_nums
    # return True when done
    create_table("domains_nums")
    return True


def get_by_letter(letter):
    # get domains that start with a letter
    # return a list of lists, where each list is a list of domains that start with a letter
    conn, cursor = con_cursor()
    cursor.execute(
        f"SELECT domain FROM domains WHERE domain LIKE '{letter}%' ORDER BY domain ASC"
    )
    domains = cursor.fetchall()
    conn.close()
    return domains


def insert_by_letter(letter):
    # insert domains that start with a letter into domains_a, domains_b, etc.
    # return True when done
    domains = get_by_letter(letter)
    for _ in domains:
        insert_domain_where("domains", f"domains_{letter}", f"{letter}%")
    return True


def get_by_num():
    # get domains that start with a number
    # insert them into domains_nums
    # return True when done
    search_term = r"[0-9]%"
    insert_domain_where("domains", "domains_nums", search_term)
    return True


def drop_table(table_name):
    conn, cursor = con_cursor()
    cursor.execute(f"DROP TABLE {table_name}")
    conn.commit()
    conn.close()
    return True


def drop_tables():
    # drop all tables that aren't "domains"
    # return True when done
    conn, cursor = con_cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    for table in tables:
        if table[0] != "domains":
            drop_table(table[0])
    conn.close()
    return True


def sort_domains_by_first_letter():
    conn = sqlite3.connect('domains.db')
    cursor = conn.cursor()

    # Retrieve all domains
    cursor.execute("SELECT domain FROM domains")
    domains = cursor.fetchall()

    # Process each domain
    for domain in domains:
        first_letter = domain[0][0].lower()  # Assuming domain is non-empty and getting the first letter
        table_name = f"domains_{first_letter}"

        # Create a table for this letter if it doesn't exist
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (domain TEXT)")

        # Insert domain into the appropriate table
        cursor.execute(f"INSERT INTO {table_name} (domain) VALUES (?)", (domain[0],))

    # Commit changes and close connection
    conn.commit()
    conn.close()


def main():
    drop_tables()
    sort_domains_by_first_letter()
    return True


if __name__ == "__main__":
    main()
