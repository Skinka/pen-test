# Docker machine for pen test

## Запуск

```
docker run --rm -it -p 80:80 vulnerables/web-dvwa
```

Host: localhost

User: admin

Pass: password


## Установка

```
sudo apt update && sudo apt upgrade 
sudo apt install -y docker.io
sudo systemctl enable docker --now
sudo usermod -aG docker $USER 
docker run --rm -it -p 80:80 vulnerables/web-dvwa
```

## Атака SQL иньекцией

```
sqlmap -h 
sqlmap -u ""
sqlmap -u "" --cookies="PHPID= ; sec" --tables(найти все таблицы)
sqlmap -u "" --cookies="PHPID= ; sec" --schema (схема базы данных) --batch (чтобы автоматически всё шло)
```
