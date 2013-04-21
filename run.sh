kill `pgrep uwsgi` 
 
uwsgi --socket :3061 --wsgi-file ./web.py --daemonize /usr/share/nginx/html/eartubes/logs/eartubes.log --callable=app

