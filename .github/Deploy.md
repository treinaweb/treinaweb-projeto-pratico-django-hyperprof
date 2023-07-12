# Passo a passo de Deploy em uma VPS

## Criar usuário e banco de dados no MySQL

Primeiro, acesse o MySQL com o usuário root:

```bash
mysql -u root -p
```

Crie um novo usuário que será usado para acessar o banco de dados:

```sql
CREATE USER 'hyperprof'@'localhost' IDENTIFIED WITH mysql_native_password 'QAN!uny0zgm-avg4uyu';
```

Crie um novo banco de dados:

```sql
CREATE DATABASE hyperprof;
```

Conceda privilégios ao novo usuário para acessar o banco de dados:

```sql
GRANT ALL PRIVILEGES ON hyperprof.* TO 'hyperprof'@'localhost';
```

Saia do MySQL:

```sql
exit
```

## Instalar o Ngix

Atualize o índice de pacotes e instale o Nginx:

```bash
sudo apt update
sudo apt install nginx
```

## Preparar o ambiente da aplicação

Entre na pasta onde iremos colocar a aplicação:

```bash
cd /var/www
```

Clone o repositório da aplicação:

```bash
sudo git clone https://github.com/treinaweb/treinaweb-projeto-pratico-django-hyperprof.git
```

Altere o nome da pasta para `hyperprof`:

```bash
sudo mv treinaweb-projeto-pratico-django-hyperprof hyperprof
```

Altere o dono da pasta para o usuário atual:

```bash
sudo chown -R $USER hyperprof
```

Entre na pasta da aplicação:

```bash
cd hyperprof
```

Instale o `python3-venv`:

```bash
sudo apt install python3-venv
```

Crie e ative um ambiente virtual para a aplicação:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale os pacotes necessários para o build da lib `mysqlclient`:

```bash
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config
```

Instale os pacotes necessários para a aplicação:

```bash
pip install -r requirements.txt
```

Crie um arquivo `.env` com as configurações da aplicação:

```bash
cp .env.example .env
```

Lembre-se de alterar as configurações no arquivo `.env`.

Execute as migrações do banco de dados:

```bash
python manage.py migrate
```

Envie os arquivos estáticos para o S3:

```bash
python manage.py collectstatic
```

## Configurar serviço do Gunicorn

Instale o Gunicorn:

```bash
pip install gunicorn
```

Crie um arquivo de serviço para o Gunicorn:

```bash
sudo nano /etc/systemd/system/hyperprof.service
```

Cole o seguinte conteúdo no arquivo:

```
[Unit]
Description=Hyperprof Gunicorn daemon
After=network.target

[Service]
User=treinaweb
Group=www-data
WorkingDirectory=/var/www/hyperprof
ExecStart=/var/www/hyperprof/.venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/hyperprof/hyperprof.sock setup.wsgi:application


[Install]
WantedBy=multi-user.target
```

Inicie o serviço do Gunicorn:

```bash
sudo systemctl start hyperprof
```

Habilite o serviço do Gunicorn para iniciar na inicialização do sistema:

```bash
sudo systemctl enable hyperprof
```

## Configurar o Nginx

Crie um arquivo de configuração para o Nginx:

```bash
sudo nano /etc/nginx/sites-available/<nome-do-dominio>
```

Lembre-se de alterar o `<nome-do-dominio>` para o domínio que você irá usar. Exemplo: `hyperprof.com`.

Cole o seguinte conteúdo no arquivo:

```
server {
	listen 80;
        server_name <nome-do-dominio>;

        location / {
                include proxy_params;
                proxy_pass http://unix:/var/www/hyperprof/hyperprof.sock;
        }
}
```

Novamente, lembre-se de alterar o `<nome-do-dominio>` para o domínio que você irá usar. Exemplo: `hyperprof.com`.

Crie um link simbólico para o arquivo de configuração:

```bash
sudo ln -s /etc/nginx/sites-available/<nome-do-dominio> /etc/nginx/sites-enabled
```

Teste a configuração do Nginx:

```bash
sudo nginx -t
```

Reinicie o Nginx:

```bash
sudo systemctl restart nginx
```

## Adicionar certificado SSL

Instale o Certbot:

```bash
sudo snap install --classic certbot
```

Execute o Certbot:

```bash
sudo certbot --nginx -d <nome-do-dominio>
```

Novamente, lembre-se de alterar o `<nome-do-dominio>` para o domínio que você irá usar. Exemplo: `hyperprof.com`.

Responda as perguntas do Certbot e pronto, seu site já está disponível com HTTPS. Por fim reinicie o Nginx:

```bash
sudo systemctl restart nginx
```