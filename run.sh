if [ $# -eq 0 ]
  then
    echo "No parameters provided. Launching bash"
    echo "...activating conda env..."
    source ./venv/bin/activate
    exec bash
    bash
else
    while test $# -gt 0; do
      case "$1" in
        -h|--help)
          echo "options:"
          echo "-h, --help                show brief help"
          exit 0
          ;;
        *)
          break
          ;;
      esac
    done
fi
