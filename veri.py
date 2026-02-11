with open('/Users/eylulzor/Downloads/appdb_backup.sql 2', 'r', encoding='utf-8') as file:
    sql_content = file.read()

with open('/Users/eylulzor/Downloads/appdb_backup_clean.sql', 'w', encoding='utf-8') as file:
    file.write(sql_content)

print("Yeni SQL dosyası hazır")
