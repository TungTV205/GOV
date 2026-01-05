import os
import psycopg2
from psycopg2 import sql

DSN = os.getenv("PG_DSN", "host=localhost dbname=Gov user=postgres password=tungpostgresql123 port=5432")
SCHEMA = os.getenv("PG_SCHEMA", "stats")

# Map information_schema.columns.data_type -> cast type
TYPE_CAST = {
    "real": "real",
    "double precision": "double precision",
    "numeric": "numeric",
    "decimal": "numeric",  # nếu gặp 'decimal' thì cast về numeric
}

def main():
    conn = psycopg2.connect(DSN)
    total = 0

    with conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = %s
                  AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """, (SCHEMA,))
            tables = [r[0] for r in cur.fetchall()]

            for table in tables:
                cur.execute("""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = %s
                      AND table_name = %s
                    ORDER BY ordinal_position
                """, (SCHEMA, table))

                cols = [(c, TYPE_CAST[t]) for (c, t) in cur.fetchall() if t in TYPE_CAST]
                if not cols:
                    continue

                set_exprs = []
                where_exprs = []

                for col_name, cast_type in cols:
                    c = sql.Identifier(col_name)
                    nan_literal = sql.SQL("'NaN'::{}").format(sql.SQL(cast_type))

                    set_exprs.append(
                        sql.SQL("{c} = CASE WHEN {c} = {nan} THEN NULL ELSE {c} END")
                        .format(c=c, nan=nan_literal)
                    )
                    where_exprs.append(
                        sql.SQL("{c} = {nan}").format(c=c, nan=nan_literal)
                    )

                stmt = sql.SQL("UPDATE {sch}.{tbl} SET {sets} WHERE {wheres};").format(
                    sch=sql.Identifier(SCHEMA),
                    tbl=sql.Identifier(table),
                    sets=sql.SQL(", ").join(set_exprs),
                    wheres=sql.SQL(" OR ").join(where_exprs),
                )

                cur.execute(stmt)
                print(f"{SCHEMA}.{table}: updated {cur.rowcount} row(s)")
                total += max(cur.rowcount, 0)

    conn.close()
    print(f"Done. Total updated rows: {total}")

if __name__ == "__main__":
    main()
