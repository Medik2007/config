publish() {
    if [[ $1 == 'port' ]]; then
        cmd="cd ~/port/public_html && git pull origin master && python manage.py collectstatic --noinput"
        psd="$HOME/run/publish/portfolio.txt"
    else
        echo "Specify which project to publish"
        return
    fi
    sshpass -f $psd ssh -t cz18090@185.114.247.170 $cmd
}

server() {
    psd="$HOME/run/publish/portfolio.txt"
    sshpass -f $psd ssh cz18090@185.114.247.170
}
