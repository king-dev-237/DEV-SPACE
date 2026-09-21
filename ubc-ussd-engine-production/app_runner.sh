#APP_ROOT="$(dirname "$(realpath "$0")")"
APP_ROOT="."
echo $APP_ROOT
PATH="$APP_ROOT/.venv/Scripts:$PATH"
export PATH
PORT=8080
LOG_FILE="app.log"
echo "Starting the application on port $PORT..."
uvicorn main:app --reload --port $PORT >> $LOG_FILE 2>&1 &
APP_PID=$!
echo "Application started with PID $APP_PID. Logs are being written to $LOG_FILE."
echo $APP_PID > app.pid
# Wait for the application to start
sleep 1
# Check if the application is running
if ps -p $APP_PID > /dev/null; then
    echo "Application is running successfully."
else
    echo "Failed to start the application. Check $LOG_FILE for details."
fi

