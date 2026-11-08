#!/bin/bash
# Liga e desliga só o servidor e o painel. Não mexe nas cancelas, no LED nem no buzzer.
#   ./web.sh start | stop | status | log
cd "$(dirname "$0")" || exit 1
export PATH="$HOME/.local/node/bin:$PATH"
PID=web.pid
rodando() { [ -f "$PID" ] && kill -0 "$(cat "$PID")" 2>/dev/null; }
case "$1" in
  start)  if rodando; then echo "já está rodando (pid $(cat $PID))"; else
            nohup node server.js >> web.log 2>&1 & echo $! > "$PID"; sleep 1
            rodando && echo "servidor ligado: http://$(hostname -I | cut -d' ' -f1):3000" || { echo "falhou; veja web.log"; tail -5 web.log; }
          fi ;;
  stop)   if rodando; then kill "$(cat $PID)"; rm -f "$PID"; echo "servidor parado"; else echo "não estava rodando"; fi ;;
  status) rodando && echo "rodando (pid $(cat $PID))" || echo "parado" ;;
  log)    tail -n 30 web.log ;;
  *)      echo "uso: ./web.sh start|stop|status|log" ;;
esac
