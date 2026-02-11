# Bu script, ham SQL yedeğini okuyup karakter kodlamasını (utf-8) 
# düzelterek temiz bir kopya oluşturur.
with open('/Users/eylulzor/Downloads/appdb_backup.sql 2', 'r', encoding='utf-8') as file:
    sql_content = file.read()
# Temizlenmiş veriyi yeni bir dosyaya yazar
with open('/Users/eylulzor/Downloads/appdb_backup_clean.sql', 'w', encoding='utf-8') as file:
    file.write(sql_content)

print("Yeni SQL dosyası hazır")
