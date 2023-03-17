from app.db_migration import init_migration

app = init_migration()
if __name__ == '__main__':
    app.run()
